from injector import Error, AssistedBuilder


class DBFactory(object):
    """Return instances of the databases"""

    def get_driver(self, injector, driver, db_host='localhost', db_user='root', db_pwd=None, db_port=None,
                   db_name=None, db_schema=None):
        """
        Return a connection to the given database using selected driver. In case given driver is not implemented a NotImplementedError is raised
        :param injector: Injector
        :param driver: string
        :param db_host: string
        :param db_user: string
        :param db_pwd: string
        :param db_port: int
        :param db_name: string
        :param db_schema: string
        :return: Selected driver instance
        """
        try:
            return injector.get(AssistedBuilder('database_driver_' + driver.lower())).build(db_host=db_host,
                                                                                            db_user=db_user,
                                                                                            db_pwd=db_pwd,
                                                                                            db_port=db_port,
                                                                                            db_name=db_name,
                                                                                            db_schema=db_schema)
        except Error:
            raise NotImplementedError('Given driver has not been implemented on SlippinJ')
