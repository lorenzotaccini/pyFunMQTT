import yaml
import json
import csv
from abc import ABC, abstractmethod


# Abstract Factory
class DataConverterFactory(ABC):

    @abstractmethod
    def create_normalizer(self, data):
        pass


# Abstract Product
class DataNormalizer(ABC):

    @abstractmethod
    def normalize(self, data):
        pass


# YAML Normalizer
class YAMLNormalizer(DataNormalizer):

    def normalize(self, data):
        return yaml.safe_load(data)


# JSON Normalizer
class JSONNormalizer(DataNormalizer):

    def normalize(self, data):
        return json.loads(data)


# CSV Normalizer
class CSVNormalizer(DataNormalizer):

    def normalize(self, data):
        rows = []
        reader = csv.DictReader(data.splitlines())
        for row in reader:
            rows.append(row)
        return rows


# Concrete Factory
class ConcreteDataConverterFactory(DataConverterFactory):

    def create_normalizer(self, data_format):
        if data_format == 'yaml':
            return YAMLNormalizer()
        elif data_format == 'json':
            return JSONNormalizer()
        elif data_format == 'csv':
            return CSVNormalizer()
        else:
            raise ValueError(f'Unsupported data format: {data_format}')


# Client Code
if __name__ == '__main__':
    factory = ConcreteDataConverterFactory()

    # Sample data as strings (replace with your actual data)
    sample_yaml = """
    name: John
    age: 30
    city: New York
    """
    sample_json = '{"name": "John", "age": 30, "city": "New York"}'
    sample_csv = """
    name,age,city
    John,30,New York
    Jane,25,Los Angeles
    """

    # Normalize sample data
    yaml_normalizer = factory.create_normalizer('yaml')
    normalized_yaml = yaml_normalizer.normalize(sample_yaml)

    json_normalizer = factory.create_normalizer('json')
    normalized_json = json_normalizer.normalize(sample_json)

    csv_normalizer = factory.create_normalizer('csv')
    normalized_csv = csv_normalizer.normalize(sample_csv)

    print('Normalized YAML:', normalized_yaml)
    print('Normalized JSON:', normalized_json)
    print('Normalized CSV:', normalized_csv)
