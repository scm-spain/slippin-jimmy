from injector import inject

import os.path


class EmrDeploy(object):
    """Execute all the deploy process inside an EMR cluster"""

    @inject(emr_cluster='emr_cluster', hdfs='hdfs', filesystem='filesystem')
    def __init__(self, emr_cluster, hdfs, filesystem):
        """
        Initialize the class
        :param emr_cluster: EmrCluster
        :param hdfs: HDFSFilesystem
        :param filesystem: Filesystem
        """
        super(EmrDeploy, self).__init__()
        self.__emr_cluster = emr_cluster
        self.__filesystem = filesystem
        self.__hdfs = hdfs

        self._base_remote_dir = '/tmp/workflows'

    def run_properties_file(self, properties_file, cluster_id):
        """
        Try to execute the given properties file in the selected cluster. It returns the job id so can check the output log in Oozie
        :param properties_file: string
        :param cluster_id: string
        :return: string
        """
        remote_properties_path = os.path.join(self._base_remote_dir, os.path.basename(properties_file))

        self.__emr_cluster.open_sftp(cluster_id).put(properties_file, remote_properties_path)

        job_id = self.__emr_cluster.exec_command('oozie job -run -config ' + remote_properties_path, cluster_id,
                                                 stop_on_error=True)

        self.__emr_cluster.exec_command('rm ' + remote_properties_path, cluster_id)

        return job_id

    def upload_code(self, wf_folder, cluster_id, hdfs_deploy_folder, workflow_name=None):
        """
        Upload given workflow code to HDFS connecting to given cluster
        :param wf_folder: string
        :param cluster_id: string
        :param hdfs_deploy_folder: string
        :param workflow_name: string
        :return: boolean
        """
        basename = wf_folder.strip(os.sep).split(os.sep)[-1] if not workflow_name else workflow_name

        tar_file = self.__filesystem.generate_tar_file(wf_folder, basename)

        remote_file = os.path.join(self._base_remote_dir, basename + '.tar.gz')

        sftp_client = self.__emr_cluster.open_sftp(cluster_id)
        self.__emr_cluster.exec_command('rm -Rf ' + self._base_remote_dir, cluster_id)

        try:
            sftp_client.mkdir(self._base_remote_dir)
            sftp_client.put(tar_file, remote_file)
        except IOError:
            return False

        self.__emr_cluster.exec_command('tar --directory ' + self._base_remote_dir + ' -zxf ' + remote_file, cluster_id)

        self.__hdfs.rmdir(hdfs_deploy_folder, cluster_id)
        self.__hdfs.mkdir(hdfs_deploy_folder, cluster_id)
        self.__hdfs.put(os.path.join(self._base_remote_dir, basename, '*'), hdfs_deploy_folder, cluster_id)

        return True
