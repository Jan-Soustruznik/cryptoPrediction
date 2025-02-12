import argparse
import os
import dropbox
import requests


def get_access_token(app_key, app_secret, refresh_token):
    """refresh acess token by refresh token"""
    response = requests.post("https://api.dropbox.com/oauth2/token", data={
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": app_key,
        "client_secret": app_secret
    })
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to refresh access token: {response.text}")

def upload_folder(dbx, local_source, remote_dest):
    """
    Rekurzivně nahraje obsah lokální složky na Dropbox.
    """
    for root, dirs, files in os.walk(local_source):
        for filename in files:
            local_path = os.path.join(root, filename)
            # Vypočítá relativní cestu vůči zdrojové složce
            relative_path = os.path.relpath(local_path, local_source)
            # Vytvoří cílovou cestu na Dropboxu (v UNIX stylu)
            dropbox_path = os.path.join(remote_dest, relative_path).replace(os.path.sep, "/")
            with open(local_path, 'rb') as f:
                data = f.read()
            try:
                dbx.files_upload(data, dropbox_path, mode=dropbox.files.WriteMode("overwrite"))
                print(f"Uploaded: {local_path} -> {dropbox_path}")
            except Exception as e:
                print(f"Failed to upload {local_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Nahraje složku na Dropbox")
    parser.add_argument("--app_key", required=True, help="Dropbox App Key")
    parser.add_argument("--app_secret", required=True, help="Dropbox App Secret")
    parser.add_argument("--refresh_token", required=True, help="Dropbox Refresh Token")
    parser.add_argument("--source", required=True, help="Lokální folder to download")
    parser.add_argument("--dest", required=True, help="path to folder in Dropbox")
    args = parser.parse_args()

    access_token = get_access_token(args.app_key, args.app_secret, args.refresh_token)
    dbx = dropbox.Dropbox(access_token)
    upload_folder(dbx, args.source, args.dest)

if __name__ == "__main__":
    main()
