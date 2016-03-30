class InstancesArgument(object):
    """Parse the instances argument"""

    def __init__(self):
        """
        Initialize the class
        """
        super(InstancesArgument, self).__init__()

    def __get_instances_groups(self, configuration):
        groups = []

        for instance_type in sorted(configuration):
            if type(configuration[instance_type]) is dict:
                groups.append({
                    'Name': instance_type,
                    'Market': 'ON_DEMAND',
                    'InstanceRole': instance_type.upper(),
                    'InstanceType': configuration[instance_type]['instance_type'],
                    'InstanceCount': 1 if 'instance_count' not in configuration[instance_type] else
                    configuration[instance_type]['instance_count']
                })

        return groups

    def parse(self, configuration):
        """
        Parse instances key from the configuration file and return it formatted
        :param configuration: dict
        :return: dict
        """
        return {
            'Instances': {
                'Ec2KeyName': configuration['ec2_key_name'],
                'KeepJobFlowAliveWhenNoSteps': configuration['keep_alive'],
                'TerminationProtected': configuration['termination_protected'],
                'Ec2SubnetId': configuration['subnet_id'],
                'EmrManagedMasterSecurityGroup': configuration['master']['security_group'],
                'EmrManagedSlaveSecurityGroup': configuration['core']['secutiry_group'],
                'InstanceGroups': self.__get_instances_groups(configuration)
            }
        }
