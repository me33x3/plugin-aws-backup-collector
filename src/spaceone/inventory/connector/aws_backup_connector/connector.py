import time
import logging
from typing import List
from spaceone.core import utils
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

from spaceone.inventory.connector.aws_backup_connector.schema.data import Backup, Rule
from spaceone.inventory.connector.aws_backup_connector.schema.resource import BackupJobResource, BackupJobResponse
from spaceone.inventory.connector.aws_backup_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel
from spaceone.inventory.libs.schema.resource import CloudWatchModel
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


class BackupConnector(SchematicAWSConnector):
    response_schema = BackupJobResponse
    service_name = 'backup'
    cloud_service_group = 'Backup'
    cloud_service_type = 'BackupJob'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[BackupJobResource]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Backup")
        resources = []
        start_time = time.time()

        resources.extend(self.set_cloud_service_types())

        for region_name in self.region_names:
            try:
                self.reset_region(region_name)

                for data in self.request_data():
                    if getattr(data, 'resource_type', None) and data.resource_type == 'inventory.ErrorResource':
                        # Error Resource
                        resources.append(data)
                    else:
                        backup_plan_resource = {
                            'name': data.name,
                            'data': data,
                            'account': self.account_id,
                            'region_code': region_name,
                            'reference': ReferenceModel(data.reference())
                        }

                        resources.append(self.response_schema({'resource': BackupJobResource(backup_plan_resource)}))
            except Exception as e:
                error_resource_response = self.generate_error(region_name, '', e)
                resources.append(error_resource_response)

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: Backup ({time.time() - start_time} sec)')
        return resources

    def request_data(self) -> List[Backup]:
        now = datetime.utcnow()
        start_time = now - timedelta(hours=24)

        response = self.client.list_backup_jobs(ByCreatedAfter=start_time, ByCreatedBefore=now)

        for raw in response.get('BackupJobs', []):
            try:
                backup_job_id = raw.get('BackupJobId')

                raw.update({
                    # 'backup_plan_id': backup_job_id,
                    # 'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, backup_plan_id),
                })

                # self.get_backup_plan(backup_job_id)

                yield Backup(raw, strict=False)
            except Exception as e:
                resource_id = raw.get('BackupPlanName', '')
                error_resource_response = self.generate_error('global', resource_id, e)
                yield error_resource_response
