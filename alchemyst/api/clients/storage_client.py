from google.cloud import storage


def get(bucket_name="", file=""):
    bucket = _storage_client().get_bucket(bucket_name)
    try:
        return bucket.get_blob(file).download_as_string().decode("utf8")
    except Exception:  # noqa: BLE001
        return None


def _storage_client():
    return storage.Client()
