from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_backup_connector.schema.data import BackupPlan
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

metadata = CloudServiceMeta.set_layouts(layouts=[])


class BackupResource(CloudServiceResource):
    cloud_service_group = StringType(default='Backup')


class BackupPlanResource(BackupResource):
    cloud_service_type = StringType(default='BackupPlan')
    data = ModelType(BackupPlan)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class BackupPlanResponse(CloudServiceResponse):
    resource = PolyModelType(BackupPlanResource)
