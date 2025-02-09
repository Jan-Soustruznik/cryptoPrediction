import argparse
import os
import dropbox

def download_folder(dbx, remote_path, local_dest):
    try:
        os.makedirs(local_dest, exist_ok=True)
        result = dbx.files_list_folder(remote_path)
        for entry in result.entries:
            # Zpracování souborů
            if isinstance(entry, dropbox.files.FileMetadata):
                _, res = dbx.files_download(entry.path_lower)
                local_file_path = os.path.join(local_dest, os.path.basename(entry.path_lower))
                with open(local_file_path, 'wb') as f:
                    f.write(res.content)
                print(f"Downloaded: {entry.path_lower} -> {local_file_path}")
            # Rekurzivně pro podsložky
            elif isinstance(entry, dropbox.files.FolderMetadata):
                new_local_dest = os.path.join(local_dest, entry.name)
                download_folder(dbx, entry.path_lower, new_local_dest)
    except Exception as e:
        print(f"Error downloading folder from Dropbox: {e}")

def main():
    parser = argparse.ArgumentParser(description="Stáhne složku z Dropboxu")
    parser.add_argument("--token", required=True, help="Dropbox API token")
    parser.add_argument("--path", required=True, help="Cesta ke složce na Dropboxu (např. /data)")
    parser.add_argument("--dest", required=True, help="Lokální cesta, kam se data uloží")
    args = parser.parse_args()

    dbx = dropbox.Dropbox(args.token)
    download_folder(dbx, args.path, args.dest)

if __name__ == "__main__":
    main()
