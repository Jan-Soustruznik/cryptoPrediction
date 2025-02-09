import argparse
import os
import dropbox

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
    parser.add_argument("--token", required=True, help="Dropbox API token")
    parser.add_argument("--source", required=True, help="Lokální složka ke nahrání")
    parser.add_argument("--dest", required=True, help="Cílová cesta na Dropboxu (např. /data)")
    args = parser.parse_args()

    dbx = dropbox.Dropbox(args.token)
    upload_folder(dbx, args.source, args.dest)

if __name__ == "__main__":
    main()
