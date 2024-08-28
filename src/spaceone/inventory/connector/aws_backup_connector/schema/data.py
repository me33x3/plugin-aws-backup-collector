import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, FloatType, DateTimeType, BooleanType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


'''
Rule
'''
class Rule(Model):
    rule_id = StringType(deserialize_from="RuleId")
    rule_name = StringType(deserialize_from="RuleName")
    target_backup_vault_name = StringType(deserialize_from="TargetBackupVaultName")
    schedule_expression = StringType(deserialize_from="ScheduleExpression")
    schedule_expression_timezone = StringType(deserialize_from="ScheduleExpressionTimezone")
    delete_after_days = IntType()
    move_to_cold_storage_after_days = IntType()
    enable_continuous_backup = BooleanType(deserialize_from="EnableContinuousBackup")


'''
Selection
'''
class Selection(Model):
    selection_id = StringType(deserialize_from="SelectionId")
    selection_name = StringType(deserialize_from="SelectionName")
    iam_role_arn = StringType(deserialize_from="IamRoleArn")
    creation_date = DateTimeType(deserialize_from="CreationDate")


'''
Job
'''
class Job(Model):
    backup_job_id = StringType(deserialize_from="BackupJobId")
    parent_job_id = StringType(deserialize_from="ParentJobId")
    backup_vault_name = StringType(deserialize_from="BackupVaultName")
    backup_type = StringType(deserialize_from="BackupType")
    backup_size_in_bytes = IntType(deserialize_from="BackupSizeInBytes")
    resource_name = StringType(deserialize_from="ResourceName")
    resource_type = StringType(deserialize_from="ResourceType")
    resource_arn = StringType(deserialize_from="ResourceArn")
    recovery_point_arn = StringType(deserialize_from="RecoveryPointArn")
    creation_date = DateTimeType(deserialize_from="CreationDate")
    completion_date = DateTimeType(deserialize_from="CompletionDate")
    state = StringType(deserialize_from="State")
    status_message = StringType(deserialize_from="StatusMessage")
    message_category = StringType(deserialize_from="MessageCategory")


class BackupPlan(AWSCloudService):
    arn = StringType(deserialize_from="BackupPlanArn")
    name = StringType(deserialize_from="BackupPlanName")
    backup_plan_id = StringType(deserialize_from="BackupPlanId")
    rules = ListType(ModelType(Rule), default=[])
    selections = ListType(ModelType(Selection), default=[])
    jobs = ListType(ModelType(Job), default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            # "external_link": f"https://console.aws.amazon.com/backup/?region={self.region_name}"
        }