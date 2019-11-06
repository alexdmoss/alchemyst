import yaml
from alchemyst.api.clients.storage_client import get


with open('app-config.yaml') as app_cfg_file:
    app_cfg = yaml.load(app_cfg_file, Loader=yaml.FullLoader)
    asset_bucket = app_cfg['bucket']


def get_document_from_gcs(id):
    return get(bucket_name=asset_bucket, file='docs/' + str(id) + '.html')
