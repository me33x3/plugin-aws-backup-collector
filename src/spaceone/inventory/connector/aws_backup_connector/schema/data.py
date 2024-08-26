import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, FloatType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


class BackupPlan(AWSCloudService):
    arn = StringType(deserialize_from="BackupPlanArn")
    name = StringType(deserialize_from="BackupPlanName")
    backup_plan_id = StringType(default="")

    def reference(self):
        return {
            "resource_id": self.arn,
            # "external_link": f"https://console.aws.amazon.com/backup/?region={self.region_name}"
        }
