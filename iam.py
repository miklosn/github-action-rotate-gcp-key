from datetime import datetime, timedelta, timezone
import google.auth
from googleapiclient import discovery

credentials, project = google.auth.default()
service = discovery.build(serviceName="iam", version="v1", credentials=credentials)


def create_key(project_id, service_account):
    full_name = "projects/{0}/serviceAccounts/{1}".format(project_id,
                                                          service_account)
    body = {"privateKeyType": "TYPE_GOOGLE_CREDENTIALS_FILE", "keyAlgorithm": "KEY_ALG_RSA_2048"}
    keys = service.projects().serviceAccounts().keys()
    request = keys.create(name=full_name, body=body)
    data = request.execute()
    key_base64 = data["privateKeyData"]
    key_name = data["name"]
    return (key_base64, key_name)


def delete_key(key_id):
    keys = service.projects().serviceAccounts().keys()
    request = keys.delete(name=key_id)
    return request.execute()


def list_keys(project_id, service_account):
    full_name = "projects/{0}/serviceAccounts/{1}".format(project_id,
                                                          service_account)
    keys = service.projects().serviceAccounts().keys()
    request = keys.list(name=full_name, keyTypes="USER_MANAGED")
    response = request.execute()
    return response["keys"]


def old_enough(item):
    delete_before = datetime.now(timezone.utc) - timedelta(minutes=5)
    d = datetime.fromisoformat(item["validAfterTime"])
    return d < delete_before
