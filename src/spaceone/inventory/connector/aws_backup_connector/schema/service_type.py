import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.dynamic_widget import ChartWidget, CardWidget
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, SearchField, EnumDyField, SizeField, ListDyField
from spaceone.inventory.libs.schema.resource import CloudServiceTypeResource, CloudServiceTypeResponse, CloudServiceTypeMeta
from spaceone.inventory.conf.cloud_service_conf import *

current_dir = os.path.abspath(os.path.dirname(__file__))

bp_total_count_conf = os.path.join(current_dir, 'widget/bp_total_count.yaml')

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
        TextDyField.data_source('ID', 'data.backup_plan_id'),
        TextDyField.data_source('Last Execution Date', 'data.last_execution_date'),
    ],
    search=[
        SearchField.set(name='ID', key='data.backup_plan_id'),
    ],
    widget=[
        CardWidget.set(**get_data_from_yaml(bp_total_count_conf)),
    ]
)

CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_bp}),
]
