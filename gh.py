import requests
from base64 import b64encode
from nacl import encoding, public


def get_pub_key(owner_repo, github_token):
    response = requests.get(
        f'https://api.github.com/repos/{owner_repo}/actions/secrets/public-key',
        headers={'Authorization': f"token {github_token}"}
    )
    response.raise_for_status()

    public_key_info = response.json()
    public_key = public_key_info['key']
    public_key_id = public_key_info['key_id']

    return (public_key, public_key_id)


def encrypt(public_key: str, secret_value: str) -> str:
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def upload_secret(owner_repo, key_name, encrypted_value, pub_key_id, github_token):
    updated_secret = requests.put(
        f'https://api.github.com/repos/{owner_repo}/actions/secrets/{key_name}',
        json={
            'encrypted_value': encrypted_value,
            'key_id': pub_key_id
        },
        headers={'Authorization': f"token {github_token}"}
    )
    updated_secret.raise_for_status()


def update_gh_secret(repo_name, secret_name, data, gh_token):
    pub_key = get_pub_key(repo_name, gh_token)
    encrypted = encrypt(pub_key[0], data)
    upload_secret(repo_name, secret_name, encrypted, pub_key[1], gh_token)
