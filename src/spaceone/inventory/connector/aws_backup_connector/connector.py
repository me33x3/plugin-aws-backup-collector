import time
import logging
from typing import List
from spaceone.core import utils
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

from spaceone.inventory.connector.aws_backup_connector.schema.data import BackupPlan
from spaceone.inventory.connector.aws_backup_connector.schema.resource import BackupPlanResource, BackupPlanResponse
from spaceone.inventory.connector.aws_backup_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel
from spaceone.inventory.libs.schema.resource import CloudWatchModel
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


class BackupConnector(SchematicAWSConnector):
    response_schema = BackupPlanResponse
    service_name = 'backup'
    cloud_service_group = 'Backup'
    cloud_service_type = 'BackupPlan'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[BackupPlanResource]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Backup")
        resources = []
        start_time = time.time()

        try:
            resources.extend(self.set_cloud_service_types())

            for data in self.request_data():
                if getattr(data, 'resource_type', None) and data.resource_type == 'inventory.ErrorResource':
                    # Error Resource
                    resources.append(data)
                else:
                    backup_plan_resource = {
                        'name': data.name,
                        'data': data,
                        'account': self.account_id,
                        'reference': ReferenceModel(data.reference())
                    }

                    resources.append(self.response_schema({'resource': BackupPlanResource(backup_plan_resource)}))

        except Exception as e:
            resource_id = ''
            resources.append(self.generate_error('global', resource_id, e))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: Backup ({time.time() - start_time} sec)')
        return resources

    def request_data(self) -> List[BackupPlan]:
        cloudtrail_resource_type = 'AWS::Backup::BackupPlan'
        response = self.client.list_backup_plans()

        backup_plans = []
        for raw in response.get('BackupPlansList', []):
            backup_plan_name = raw.get('BackupPlanName')
            try:
                raw.update({
                    'backup_plan_id': raw.get('BackupPlanId'),
                })

                yield BackupPlan(raw, strict=False)
            except Exception as e:
                resource_id = raw.get('BackupPlanName', '')
                error_resource_response = self.generate_error('global', resource_id, e)
                yield error_resource_response

    def get_backup_plan(self, backup_plan_id):
        return