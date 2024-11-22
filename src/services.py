import logging
import os
from zipfile import ZipFile


class FileService:
    """
    Service for working with files
    """

    @staticmethod
    def unzip_file(
        archive_path: str,
        file_to_extract: str,
    ) -> str:
        with ZipFile(archive_path, "r") as zip_ref:
            if file_to_extract in zip_ref.namelist():
                with zip_ref.open(file_to_extract) as file:
                    return file.read().decode("utf-8")
            else:
                logging.warning(f"File {file_to_extract} not found in archive")

    @staticmethod
    def write_file(
        file_path: str,
        text: str,
    ) -> None:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)
        else:
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(text)
