import time
import logging
from typing import List
from spaceone.core import utils
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

from spaceone.inventory.connector.aws_backup_connector.schema.data import BackupPlan, Rule, Selection, Job
from spaceone.inventory.connector.aws_backup_connector.schema.resource import BackupPlanResource, BackupPlanResponse
from spaceone.inventory.connector.aws_backup_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel
from spaceone.inventory.libs.schema.resource import CloudWatchModel
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


class BackupConnector(SchematicAWSConnector):
    service_name = 'backup'
    cloud_service_group = 'Backup'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Backup")
        resources = []
        start_time = time.time()

        resources.extend(self.set_cloud_service_types())

        collect_resources = [
            {
                'request_method': self.request_backup_plan_data,
                'resource': BackupPlanResource,
                'response_schema': BackupPlanResponse
            },
        ]

        for region_name in self.region_names:
            try:
                self.reset_region(region_name)

                for collect_resource in collect_resources:
                    resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

                # for data in self.request_data(region_name):
                #     if getattr(data, 'resource_type', None) and data.resource_type == 'inventory.ErrorResource':
                #         # Error Resource
                #         resources.append(data)
                #     else:
                #         backup_job_resource = {
                #             'name': data.name,
                #             'data': data,
                #             'account': self.account_id,
                #             'region_code': region_name,
                #             'reference': ReferenceModel(data.reference())
                #         }
                #
                #         resources.append(self.response_schema({'resource': BackupJobResource(backup_job_resource)}))
            except Exception as e:
                error_resource_response = self.generate_error(region_name, '', e)
                resources.append(error_resource_response)

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: Backup ({time.time() - start_time} sec)')
        return resources


    def request_backup_plan_data(self, region_name) -> List[BackupPlan]:
        self.cloud_service_type = 'BackupPlan'
        cloudtrail_resource_type = 'AWS::Backup::BackupPlan'

        response = self.client.list_backup_plans()

        for raw in response.get('BackupPlansList', []):
            try:
                backup_plan_id = raw['BackupPlanId']

                raw.update({'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, backup_plan_id)})

                rules = self.get_backup_rules(backup_plan_id)
                raw.update({'rules': rules})

                selections = self.get_backup_selections(backup_plan_id)
                raw.update({'selections': selections})

                jobs = []
                for rule in rules:
                    target_backup_vault_name = rule['target_backup_vault_name']
                    jobs.extend(self.get_backup_jobs(backup_plan_id, target_backup_vault_name))
                raw.update({'jobs': jobs})

                backup_plan_vo = BackupPlan(raw, strict=False)
                yield {
                    'name': backup_plan_vo.name,
                    'data': backup_plan_vo,
                    'account': self.account_id,
                }
            except Exception as e:
                resource_id = raw.get('BackupPlanId', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}


    def get_backup_rules(self, backup_plan_id):
        try:
            response = self.client.get_backup_plan(BackupPlanId=backup_plan_id)

            backup_plan = response.get('BackupPlan')
            rules = []

            for raw in backup_plan.get('Rules', []):
                raw.update({
                    'delete_after_days': raw.get('Lifecycle').get('DeleteAfterDays'),
                    'move_to_cold_storage_after_days': raw.get('Lifecycle').get('MoveToColdStorageAfterDays'),
                })
                rules.append(Rule(raw, strict=False))
            return rules
        except Exception as e:
            _LOGGER.error(f'[Backup {backup_plan_id}: Get Backup Rules] {e}')
            return None


    def get_backup_selections(self, backup_plan_id):
        try:
            response = self.client.list_backup_selections(BackupPlanId=backup_plan_id)

            selections = []
            for raw in response.get('BackupSelectionsList', []):
                selections.append(Selection(raw, strict=False))
            return selections
        except Exception as e:
            _LOGGER.error(f'[Backup {backup_plan_id}: Get Backup Selections] {e}')
            return None


    def get_backup_jobs(self, backup_plan_id, backup_vault_name):
        try:
            now = datetime.utcnow()
            start_time = now - timedelta(hours=24)

            response = self.client.list_backup_jobs(ByBackupVaultName=backup_vault_name, ByCreatedAfter=start_time, ByCreatedBefore=now)

            jobs = []
            for raw in response.get('BackupJobs', []):
                jobs.append(Job(raw, strict=False))
            return jobs
        except Exception as e:
            _LOGGER.error(f'[Backup {backup_plan_id}: Get Backup Jobs] {e}')
            return None