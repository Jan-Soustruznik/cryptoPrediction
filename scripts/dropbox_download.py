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

def download_folder(dbx, remote_path, local_dest):
    try:
        os.makedirs(local_dest, exist_ok=True)
        result = dbx.files_list_folder(remote_path)
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                _, res = dbx.files_download(entry.path_lower)
                local_file_path = os.path.join(local_dest, os.path.basename(entry.path_lower))
                with open(local_file_path, 'wb') as f:
                    f.write(res.content)
                print(f"Downloaded: {entry.path_lower} -> {local_file_path}")
            elif isinstance(entry, dropbox.files.FolderMetadata):
                new_local_dest = os.path.join(local_dest, entry.name)
                download_folder(dbx, entry.path_lower, new_local_dest)
    except Exception as e:
        print(f"Error downloading folder from Dropbox: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download folder from Dropbox")
    parser.add_argument("--app_key", required=True, help="Dropbox App Key")
    parser.add_argument("--app_secret", required=True, help="Dropbox App Secret")
    parser.add_argument("--refresh_token", required=True, help="Dropbox Refresh Token")
    parser.add_argument("--path", required=True, help="path to folder in Dropbox")
    parser.add_argument("--dest", required=True, help="local path")
    args = parser.parse_args()

    access_token = get_access_token(args.app_key, args.app_secret, args.refresh_token)
    dbx = dropbox.Dropbox(access_token)
    download_folder(dbx, args.path, args.dest)

if __name__ == "__main__":
    main()