from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.connector.aws_backup_connector.schema.data import BackupPlan
from spaceone.inventory.libs.schema.resource import CloudServiceResource, CloudServiceResponse, CloudServiceMeta
from spaceone.inventory.libs.schema.dynamic_field import TextDyField, ListDyField, EnumDyField, SizeField
from spaceone.inventory.libs.schema.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, SimpleTableDynamicLayout

bp = ItemDynamicLayout.set_fields('Backup Plan', fields=[
    TextDyField.data_source('ID', 'data.backup_plan_id'),
    TextDyField.data_source('Name', 'data.name'),
    TextDyField.data_source('Last Execution Date', 'data.last_execution_date'),
])

rules = TableDynamicLayout.set_fields('Backup Rules', 'data.rules', fields=[
    TextDyField.data_source('Rule ID', 'rule_id'),
    TextDyField.data_source('Rule Name', 'rule_name'),
    TextDyField.data_source('Backup Vault', 'target_backup_vault_name'),
    TextDyField.data_source('Backup Schedule', 'schedule_expression'),
    TextDyField.data_source('Total Retention Period', 'delete_after_days'),
])


selections = TableDynamicLayout.set_fields('Resource Assignments', 'data.selections', fields=[
    TextDyField.data_source('Name', 'selection_name'),
    TextDyField.data_source('IAM Role ARN', 'iam_role_arn'),
    TextDyField.data_source('Creation Time', 'creation_date'),
])


jobs = TableDynamicLayout.set_fields('Backup Jobs', 'data.jobs', fields=[
    TextDyField.data_source('Job ID', 'backup_job_id'),
    TextDyField.data_source('Resource Name', 'resource_name'),
    EnumDyField.data_source('Status', 'state', default_badge={
        'coral.600': ['FAILED'], 'green.600': ['COMPLETED']}),
    TextDyField.data_source('Message Category', 'message_category'),
    TextDyField.data_source('Resource Type', 'resource_type'),
    TextDyField.data_source('Backup Type', 'backup_type'),
    TextDyField.data_source('Backup Size', 'backup_size_in_bytes'),
    TextDyField.data_source('Backup Vault', 'backup_vault_name'),
    TextDyField.data_source('Completion Date', 'completion_date'),
])


bp_metadata = CloudServiceMeta.set_layouts(layouts=[bp, rules, selections, jobs])


class BackupResource(CloudServiceResource):
    cloud_service_group = StringType(default='Backup')


class BackupPlanResource(BackupResource):
    cloud_service_type = StringType(default='BackupPlan')
    data = ModelType(BackupPlan)
    _metadata = ModelType(CloudServiceMeta, default=bp_metadata, serialized_name='metadata')


class BackupPlanResponse(CloudServiceResponse):
    resource = PolyModelType(BackupPlanResource)
