import logging
import os
import iam
import gh

PROJECT_ID = os.environ["PROJECT_ID"]
SERVICE_ACCOUNT = os.environ["SERVICE_ACCOUNT"]

gh_token = os.environ["PERSONAL_ACCESS_TOKEN"]
secret_name = os.environ["GITHUB_SECRET_NAME"]
owner_repository = os.environ["OWNER_REPOSITORY"]

logging.basicConfig(format='%(levelname)s %(message)s', level=logging.INFO)

# create new key
(new_key_base64, new_key_name) = iam.create_key(PROJECT_ID, SERVICE_ACCOUNT)
logging.info("Created new key {}".format(new_key_name))

# list of keys to delete. we keep the currently created key and also skip keys newer than 1 minute (race condition)
keys = iam.list_keys(PROJECT_ID, SERVICE_ACCOUNT)
keys_to_delete = list(map(lambda item: item["name"], filter(lambda item: item["name"] != new_key_name, filter(iam.old_enough, keys))))

# update secrets in all repos
for repo in [x.strip() for x in owner_repository.split(',')]:
    gh.update_gh_secret(repo, secret_name, new_key_base64, gh_token)
    logging.info("Updated gh secret in {}".format(repo))

# delete old service account keys
for key in keys_to_delete:
    iam.delete_key(key)
    logging.info("Deleted key {}".format(key))

