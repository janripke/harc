import json
from harc.repositories.DatasourceRepository import DatasourceRepository
import os


class DatasourceBuilder:
    def __init__(self):
        pass

    @staticmethod
    def build(filename):
        data = open(filename)
        datasource = json.load(data)
        data.close()

        return datasource

    @staticmethod
    def find(name, filename="harc-ds.json"):
        harc = DatasourceBuilder.build(filename)
        datasourcer = DatasourceRepository(harc)
        datasource = datasourcer.get_by_name(name)
        if not datasource:
            datasource = DatasourceBuilder.build(name + ".json")
        return datasource

