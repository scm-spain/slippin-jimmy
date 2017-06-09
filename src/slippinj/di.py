import ConfigParser
import logging
from argparse import Namespace

import paramiko
from boto3.session import Session
from injector import Module, provides, inject, InstanceProvider, singleton
from openpyxl import Workbook

from .cli.interactive.cluster_id import ClusterId
from .cli.interactive.configuration_file import ConfigurationFile
from .cli.interactive.default_configuration import DefaultConfiguration
from .cli.interactive.properties_file import PropertiesFile
from .cli.objects.wf_configuration_object import WfConfigurationObject
from .cli.scripts.tables_configuration.incremental_tables_configuration import IncrementalTablesConfiguration
from .cli.scripts.tables_configuration.other_tables_configuration import OtherTablesConfiguration
from .cli.scripts.tables_configuration.tables_configuration import TablesConfiguration
from .cli.workflow_configuration import WorkflowConfiguration
from .databases.db_factory import DBFactory
from .databases.drivers.sqlserver import Sqlserver
from .databases.drivers.postgresql import Postgresql
from .databases.drivers.mysql import Mysql
from .databases.drivers.oracle import Oracle
from .emr.cluster import EmrCluster
from .emr.deploy import EmrDeploy
from .emr.job_flow.configuration import JobFlowConfigurationParser
from .emr.job_flow.run import RunJobFlow
from .filesystem.excel_writer import ExcelWriter
from .filesystem.filesystem import Filesystem
from .filesystem.hdfs import HDFSFilesystem
from .filesystem.yaml_configuration import YamlConfiguration, WorkflowsYamlConfigurationWriter
from .generator.hive_templates import HiveTemplatesRender
from .generator.templates_lib import TemplatesLib
from .generator.wf_templates import WfTemplatesRender
from .provision.client import AnsibleClient


@inject(_args=Namespace)
class DIModule(Module):
    def configure(self, binder):
        binder.bind('ansible_client', to=AnsibleClient)
        binder.bind('args', to=InstanceProvider(self._args), scope=singleton)
        binder.bind('emr_cluster', to=EmrCluster)
        binder.bind('emr_deploy', to=EmrDeploy)
        binder.bind('excel_writer', to=ExcelWriter, scope=singleton)
        binder.bind('filesystem', to=Filesystem, scope=singleton)
        binder.bind('hdfs', to=HDFSFilesystem)
        binder.bind('hive_templates_render', to=HiveTemplatesRender)
        binder.bind('interactive_cluster_id', to=ClusterId, scope=singleton)
        binder.bind('interactive_configuration_file', to=ConfigurationFile, scope=singleton)
        binder.bind('interactive_default_configuration', to=DefaultConfiguration)
        binder.bind('interactive_properties_file', to=PropertiesFile)
        binder.bind('job_flow', to=RunJobFlow)
        binder.bind('job_flow_configuration', to=JobFlowConfigurationParser)
        binder.bind('object_configuration', to=WfConfigurationObject, scope=singleton)
        binder.bind('templates_lib', to=TemplatesLib)
        binder.bind('wf_configuration', to=WorkflowConfiguration)
        binder.bind('wf_templates_render', to=WfTemplatesRender)
        binder.bind('yaml_configuration', to=YamlConfiguration)
        binder.bind('yaml_configuration_writer', to=WorkflowsYamlConfigurationWriter)

    @provides('ssh_lib_client')
    def ssh_client(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        return ssh_client

    @provides('workbook')
    def workbook(self):
        return Workbook(write_only=True)

    @provides('configuration_parser')
    def config_parser(self):
        return ConfigParser.SafeConfigParser()

    @provides('logger', scope=singleton)
    def logger(self):
        logger = logging.getLogger('slippinj')

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)

        return logger


@inject(_profile=str)
class AwsClientModule(Module):
    @provides('aws_emr_client')
    def aws_emr_client(self):
        aws_profile = 'default' if False == self._profile else self._profile
        aws_session = Session(profile_name=aws_profile)
        return aws_session.client('emr')


class DatabaseDriversModule(Module):
    def configure(self, binder):
        binder.bind('db_factory', to=DBFactory, scope=singleton)
        binder.bind('database_driver_sqlserver', to=Sqlserver, scope=singleton)
        binder.bind('database_driver_postgresql', to=Postgresql, scope=singleton)
        binder.bind('database_driver_mysql', to=Mysql, scope=singleton)
        binder.bind('database_driver_oracle', to=Oracle, scope=singleton)


class TablesConfigurationModule(Module):
    def configure(self, binder):
        binder.bind('tables_configuration', to=TablesConfiguration, scope=singleton)
        binder.bind('incremental_tables_configuration', to=IncrementalTablesConfiguration, scope=singleton)
        binder.bind('other_tables_configuration', to=OtherTablesConfiguration, scope=singleton)
