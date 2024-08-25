import time
import logging
from typing import List
from spaceone.core import utils
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

from spaceone.inventory.connector.aws_backup_connector.schema.data import Backup
from spaceone.inventory.connector.aws_backup_connector.schema.resource import BackupResource, BackupResponse
from spaceone.inventory.connector.aws_backup_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel
from spaceone.inventory.libs.schema.resource import CloudWatchModel
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


class BackupConnector(SchematicAWSConnector):
    response_schema = BackupResponse
    service_name = 'backup'
    cloud_service_group = 'Backup'
    cloud_service_type = 'BackupPlan'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[BackupResource]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Backup")
        resources = []
        start_time = time.time()

        try:
            resources.extend(self.set_cloud_service_types())

            data = self.request_data()

            print(data)
        except Exception as e:
            resource_id = ''
            resources.append(self.generate_error('global', resource_id, e))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: Backup ({time.time() - start_time} sec)')
        return resources

    def request_data(self) -> List[Backup]:
        cloudtrail_resource_type = 'AWS::Backup::BackupPlan'
        response = self.client.list_backup_plans()

        yield response
