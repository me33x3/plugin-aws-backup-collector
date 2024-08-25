from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_backup_connector.schema.data import Backup
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

metadata = CloudServiceMeta.set_layouts(layouts=[])


class BackupResource(CloudServiceResource):
    cloud_service_group = StringType(default='Backup')


class BackupResource(BackupResource):
    cloud_service_type = StringType(default='BackupPlan')
    data = ModelType(Backup)
    _metadata = ModelType(CloudServiceMeta, default=metadata, serialized_name='metadata')


class BackupResponse(CloudServiceResponse):
    resource = PolyModelType(BackupResource)
