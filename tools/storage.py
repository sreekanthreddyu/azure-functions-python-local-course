from __future__ import annotations

import argparse
from pathlib import Path

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient


CONNECTION_STRING = "UseDevelopmentStorage=true"


def upload(file_path: Path, blob_name: str | None) -> None:
    service = BlobServiceClient.from_connection_string(
        CONNECTION_STRING,
        api_version="2026-06-06",
    )
    container = service.get_container_client("landing")
    try:
        container.create_container()
    except ResourceExistsError:
        pass

    name = blob_name or file_path.name
    with file_path.open("rb") as source:
        container.upload_blob(name=name, data=source, overwrite=True)
    print(f"Uploaded landing/{name}")


def list_blobs() -> None:
    service = BlobServiceClient.from_connection_string(
        CONNECTION_STRING,
        api_version="2026-06-06",
    )
    for container in service.list_containers():
        container_name = container["name"]
        print(f"[{container_name}]")
        for blob in service.get_container_client(container_name).list_blobs():
            print(f"  {blob.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Work with the local Azurite account.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    upload_parser = subparsers.add_parser("upload")
    upload_parser.add_argument("file", type=Path)
    upload_parser.add_argument("--name")
    subparsers.add_parser("list")

    args = parser.parse_args()
    if args.command == "upload":
        upload(args.file, args.name)
    else:
        list_blobs()


if __name__ == "__main__":
    main()
