import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, ListType, FloatType
from spaceone.inventory.libs.schema.resource import AWSCloudService

_LOGGER = logging.getLogger(__name__)


'''
VERSIONING
'''
class Rule(Model):
    name = StringType(default="")


class Backup(AWSCloudService):
    arn = StringType(deserialize_from="RecoveryPointArn")
    name = StringType(deserialize_from="ResourceName")
    state = StringType(deserialize_from="State")
    status_message = StringType(deserialize_from="StatusMessage")
    resource_type = StringType(deserialize_from="ResourceType")

    def reference(self):
        return {
            "resource_id": self.arn,
            # "external_link": f"https://console.aws.amazon.com/backup/?region={self.region_name}"
        }
