import os
from .basic_script import BasicScript


class Scribe(BasicScript):
    """Generate the documentation and basic configuration to run next Jimmy's steps based on database structure"""

    def get_arguments(self):
        """
        Get the arguments to configure current script
        :return: list
        """
        return [
            {
                'short': '-D',
                'long': '--db-driver',
                'help': 'Driver to use to connect to the database',
                'required': True
            },
            {
                'short': '-H',
                'long': '--db-host',
                'help': 'Database\'s hostname',
                'required': True
            },
            {
                'short': '-P',
                'long': '--db-port',
                'help': 'Database\'s port'
            },
            {
                'short': '-u',
                'long': '--db-user',
                'help': 'Database\'s username',
                'required': True
            },
            {
                'short': '-p',
                'long': '--db-pwd',
                'help': 'Database\'s password'
            },
            {
                'short': '-n',
                'long': '--db-name',
                'help': 'Database\'s name to get the information from'
            },
            {
                'short': '-s',
                'long': '--db-schema',
                'help': 'Database\'s schema to get the information from'
            },
            {
                'short': '-l',
                'long': '--table-list',
                'help': 'List of tables, separated by commas, to get information from'
            },
            {
                'short': '-E',
                'long': '--excel-only',
                'action': 'store_true',
                'help': 'If set, generate excel only for documentation purposes'
            },
            {
                'short': '-r',
                'long': '--max-records',
                'default': 30,
                'help': 'Set the max number of sample records per table, default 30.'
            },
            {
                'short': '-o',
                'long': '--output',
                'help': 'Directory where the output would be generated'
            },
            {
                'short': '-N',
                'long': '--yaml-db-name',
                'help': 'Database\'s name to be used in YML files'
            },
            {
                'short': '-w',
                'long': '--where',
                'help': 'Where clause to extend default query'
            },
            {
                'short': '-o',
                'long': '--output',
                'help': 'Directory where write all the files',
                'default': os.getcwd()
            }
        ]

    def run(self, args, injector):
        """
        Run the component to generate documentation and basic configuration files based on source database
        :param args: Namespace
        :param injector: Injector
        """
        logger = injector.get('logger')

        logger.info('Getting driver instance and connecting to database')
        db = injector.get('db_factory').get_driver(injector, args.db_driver, args.db_host, args.db_user, args.db_pwd,
                                                   db_port=args.db_port, db_name=args.db_name, db_schema=args.db_schema)

        logger.info('Getting tables information')
        tables_information = db.get_all_tables_info(args.table_list, args.where, args.max_records)

        logger.info('Writing tables information into excel file')
        injector.get('excel_writer').generate_excel_file(tables_information['tables'], args.db_name, args.output)

        if not args.excel_only:
            logger.info('Writing tables information into config files')
            injector.get('yaml_configuration_writer').generate_yaml_files(injector, tables_information, args.db_driver,
                                                                          args.db_host, args.db_port,
                                                                          args.db_user, args.db_name, args.db_pwd,
                                                                          args.output)
