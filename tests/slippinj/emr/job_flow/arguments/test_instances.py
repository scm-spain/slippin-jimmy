from slippinj.emr.job_flow.arguments.instances import InstancesArgument


class TestInstancesArgument(object):
    def test_parse_successfully_run(self):
        configuration = {
            'availability_zone': 'eu-west-1',
            'ec2_key_name': 'my_key',
            'keep_alive': True,
            'termination_protected': True,
            'subnet_id': 'testing',
            'master': {
                'security_group': 'sg-1',
                'instance_type': 'm1.medium'
            },
            'core': {
                'instance_type': 'm2.xlarge',
                'secutiry_group': 'sg-1',
                'instance_count': 2
            },
            'task': {
                'instance_type': 'c1.medium',
                'instance_count': 1
            },
        }

        expected = {
            'Instances': {
                'Ec2KeyName': 'my_key',
                'KeepJobFlowAliveWhenNoSteps': True,
                'TerminationProtected': True,
                'Ec2SubnetId': 'testing',
                'EmrManagedMasterSecurityGroup': 'sg-1',
                'EmrManagedSlaveSecurityGroup': 'sg-1',
                'InstanceGroups': [
                    {
                        'InstanceCount': 2,
                        'InstanceRole': 'CORE',
                        'InstanceType': 'm2.xlarge',
                        'Market': 'ON_DEMAND',
                        'Name': 'core'
                    },
                    {
                        'InstanceCount': 1,
                        'InstanceRole': 'MASTER',
                        'InstanceType': 'm1.medium',
                        'Market': 'ON_DEMAND',
                        'Name': 'master'
                    },
                    {
                        'InstanceCount': 1,
                        'InstanceRole': 'TASK',
                        'InstanceType': 'c1.medium',
                        'Market': 'ON_DEMAND',
                        'Name': 'task'
                    },
                ]
            }
        }

        assert expected == InstancesArgument().parse(configuration)
