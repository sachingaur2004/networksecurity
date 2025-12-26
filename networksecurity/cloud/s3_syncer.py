import os
import shutil

class S3Sync:
    def sync_folder_to_s3(self, folder: str, aws_bucket_url: str):
        """
        Dummy implementation for now.
        This prevents FastAPI from crashing.
        """
        print(f"[INFO] Syncing {folder} to {aws_bucket_url}")
