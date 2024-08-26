import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, EnumDyField, SizeField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

# bucket_total_count_conf = os.path.join(current_dir, 'widget/bucket_total_count.yaml')
# object_total_count_conf = os.path.join(current_dir, 'widget/object_total_count.yaml')
# object_total_size_conf = os.path.join(current_dir, 'widget/object_total_size.yaml')
# bucket_count_by_region_conf = os.path.join(current_dir, 'widget/bucket_count_by_region.yaml')
# object_count_by_region_conf = os.path.join(current_dir, 'widget/object_count_by_region.yaml')
# object_total_size_by_region_conf = os.path.join(current_dir, 'widget/object_total_size_by_region.yaml')
# bucket_count_by_account_conf = os.path.join(current_dir, 'widget/bucket_count_by_account.yaml')
# object_count_by_account_conf = os.path.join(current_dir, 'widget/object_count_by_account.yaml')
# object_total_size_by_account_conf = os.path.join(current_dir, 'widget/object_total_size_by_account.yaml')

cst_bp = CloudServiceTypeResource()
cst_bp.name = 'BackupPlan'
cst_bp.provider = 'aws'
cst_bp.group = 'Backup'
cst_bp.labels = ['Backup']
cst_bp.is_primary = True
cst_bp.is_major = True
cst_bp.service_code = 'AmazonBackup'
cst_bp.tags = {
    'spaceone:icon': '',
}

cst_bp._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
    ],
    search=[
    ],
    widget=[
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_bp}),
]
