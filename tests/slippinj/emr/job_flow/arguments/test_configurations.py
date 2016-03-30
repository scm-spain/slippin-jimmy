from slippinj.emr.job_flow.arguments.configurations import ConfigurationsArgument


class TestConfigurationsArgument(object):
    def test_parse_successfully_run(self):
        configuration = [
            {
                'classification': 'oozie-env',
                'configurations': [
                    {
                        'classification': 'export',
                        'properties': {
                            'OOZIE_URL': 'http://localhost:11000/oozie'
                        }
                    }
                ]
            },
            {
                'classification': 'oozie-site',
                'properties': {
                    'oozie.services.ext': 'org.apache.oozie.service.JMSAccessorService,org.apache.oozie.service.JMSTopicService,org.apache.oozie.service.EventHandlerService,org.apache.oozie.sla.service.SLAService',
                    'oozie.service.EventHandlerService.event.listeners': 'org.apache.oozie.jms.JMSJobEventListener,org.apache.oozie.sla.listener.SLAJobEventListener,org.apache.oozie.jms.JMSSLAEventListener,org.apache.oozie.sla.listener.SLAEmailEventListener',
                    'oozie.service.SchemaService.wf.ext.schemas': 'shell-action-0.1.xsd,shell-action-0.2.xsd,email-action-0.1.xsd,hive-action-0.2.xsd,hive-action-0.3.xsd,sqoop-action-0.2.xsd,sqoop-action-0.3.xsd,ssh-action-0.1.xsd,distcp-action-0.1.xsd,oozie-sla-0.1.xsd,oozie-sla-0.2.xsd',
                    'oozie.service.JPAService.jdbc.driver': 'com.mysql.jdbc.Driver',
                    'oozie.service.JPAService.jdbc.url': 'jdbc:mysql://hue.my.rds:3306/oozie',
                    'oozie.service.JPAService.jdbc.username': 'oozie',
                    'oozie.service.JPAService.jdbc.password': 'secret'
                }
            },
            {
                'classification': 'hue-ini',
                'configurations': [
                    {
                        'classification': 'desktop',
                        'configurations': [
                            {
                                'classification': 'database',
                                'properties': {
                                    'name': 'huedb',
                                    'user': 'hue',
                                    'password': 'secret',
                                    'host': 'hue.my.rds'
                                }
                            }
                        ]
                    }
                ]
            }
        ]

        expected = {
            'Configurations': [
                {
                    'Classification': 'oozie-env',
                    'Configurations': [
                        {
                            'Classification': 'export',
                            'Properties': {
                                'OOZIE_URL': 'http://localhost:11000/oozie'
                            }
                        }
                    ]
                },
                {
                    'Classification': 'oozie-site',
                    'Properties': {
                        'oozie.services.ext': 'org.apache.oozie.service.JMSAccessorService,org.apache.oozie.service.JMSTopicService,org.apache.oozie.service.EventHandlerService,org.apache.oozie.sla.service.SLAService',
                        'oozie.service.EventHandlerService.event.listeners': 'org.apache.oozie.jms.JMSJobEventListener,org.apache.oozie.sla.listener.SLAJobEventListener,org.apache.oozie.jms.JMSSLAEventListener,org.apache.oozie.sla.listener.SLAEmailEventListener',
                        'oozie.service.SchemaService.wf.ext.schemas': 'shell-action-0.1.xsd,shell-action-0.2.xsd,email-action-0.1.xsd,hive-action-0.2.xsd,hive-action-0.3.xsd,sqoop-action-0.2.xsd,sqoop-action-0.3.xsd,ssh-action-0.1.xsd,distcp-action-0.1.xsd,oozie-sla-0.1.xsd,oozie-sla-0.2.xsd',
                        'oozie.service.JPAService.jdbc.driver': 'com.mysql.jdbc.Driver',
                        'oozie.service.JPAService.jdbc.url': 'jdbc:mysql://hue.my.rds:3306/oozie',
                        'oozie.service.JPAService.jdbc.username': 'oozie',
                        'oozie.service.JPAService.jdbc.password': 'secret'
                    }
                },
                {
                    'Classification': 'hue-ini',
                    'Configurations': [
                        {
                            'Classification': 'desktop',
                            'Configurations': [
                                {
                                    'Classification': 'database',
                                    'Properties': {
                                        'name': 'huedb',
                                        'user': 'hue',
                                        'password': 'secret',
                                        'host': 'hue.my.rds'
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        assert expected == ConfigurationsArgument().parse(configuration)
