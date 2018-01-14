import datetime

from skylog.lib.elasticsearch import Elasticsearch


def server_test(servers):
    server_list = []
    for server in servers:
        if Elasticsearch(server).ping():
            server_list.append(server)
    return server_list


def active_index(indexes):
    return indexes


class ElasticWrapper:
    """This wraps around the Elasticsearch client to add some additional features
    """

    def __init__(self, servers, index):
        """

        :param servers: list
        :param index: string
        """
        self.index = index
        self.servers = server_test(servers)
        self.client = Elasticsearch(self.servers, maxsize=100)
        self.Elasticsearch = self.client
        self.ES = self.client
        self.index_creation = self.Elasticsearch.indices.get_settings(index=self.index)[self.index]['settings']['index']['creation_date']
        self.index_uuid = self.Elasticsearch.indices.get_settings(index=self.index)[self.index]['settings']['index']['uuid']

    def __getattr__(self, name):
        """Python implemented a __getattr__() method to handle accesses of unknown attributes (methods are just
        attributes that are callable; so this function handles both methods and non-mehtod fields). Here we assume
        that if you access an unknown attribute, you want a method, so we return a function that can be called

        :param name:
        :return: callable
        """
        return getattr(self.client, name)

    def __call__(self):
        """When you call the class, return this

        :return: self.attributes
        """
        for attribute in dir(self):
            if '__' not in attribute:
                print('{} = {}'.format(attribute, getattr(self, attribute)))

    def age(self):
        """Age of index in days, hours, minutes, and seconds

        :return: string
        """
        epoch = int(self.Elasticsearch.indices.get_settings(index=self.index)[self.index]['settings']['index']['creation_date']) // 1000
        delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(epoch)
        seconds = int(delta.total_seconds())
        days, seconds = seconds // 86400, seconds % 86400
        hours, seconds = seconds // 3600, seconds % 3600
        minutes, seconds = seconds // 60, seconds % 60

        message = '{} was created {} days {} hours {} minutes {} seconds ago\n'.format(
                self.index,
                days,
                hours,
                minutes,
                seconds
        )

        if self.index is 'skynet':
            message += '\nIt is time.'

        return print(message)
