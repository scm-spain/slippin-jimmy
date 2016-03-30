from botocore.exceptions import WaiterError
from injector import inject


class RunJobFlow(object):
    """Run a job flow based on a given configuration"""

    @inject(aws_emr_client='aws_emr_client', logger='logger', job_flow_configuration='job_flow_configuration')
    def __init__(self, aws_emr_client, logger, job_flow_configuration):
        """
        Initialize the class
        :param aws_emr_client: EMR.client
        :param logger: Logging
        """
        super(RunJobFlow, self).__init__()
        self.__aws_emr_client = aws_emr_client
        self.__logger = logger
        self.__job_flow_configuration = job_flow_configuration

    def run_cluster(self, cluster_configuration):
        """
        Launch a cluster based on given configuration
        :param cluster_configuration: string
        """
        aws_arguments = self.__job_flow_configuration.convert_to_arguments(cluster_configuration)

        self.__logger.debug('Launching cluster with given configuration')
        response = self.__aws_emr_client.run_job_flow(**aws_arguments)
        self.__logger.info('Cluster launched with ID: {cluster_id}'.format(cluster_id=response['JobFlowId']))
        try:
            waiter = self.__aws_emr_client.get_waiter('cluster_running')
            self.__logger.info('Waiting for cluster to be ready')
            waiter.wait(ClusterId=response['JobFlowId'])
            self.__logger.info('Cluster up and running ID: {cluster_id}'.format(cluster_id=response['JobFlowId']))
        except WaiterError:
            self.__logger.error('Cluster creation failed')