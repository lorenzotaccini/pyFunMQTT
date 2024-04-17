from abc import ABC, abstractmethod
import csv
import json
import yaml


# Abstract Factory
class MessageConverterFactory(ABC):

    @abstractmethod
    def create_converter(self, format_type):
        pass


# Abstract Product
class MessageConverter(ABC):

    @abstractmethod
    def convert(self, message):
        pass


# CSV Converter
class CSVConverter(MessageConverter):

    def convert(self, message):
        # Assuming message is a dictionary
        keys = message.keys()
        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerow(message)


# JSON Converter
class JSONConverter(MessageConverter):

    def convert(self, message):
        with open('output.json', 'w') as jsonfile:
            json.dump(message, jsonfile, indent=4)


# YAML Converter
class YAMLConverter(MessageConverter):

    def convert(self, message):
        with open('output.yaml', 'w') as yamlfile:
            yaml.dump(message, yamlfile)


# Concrete Factory
class ConcreteMessageConverterFactory(MessageConverterFactory):

    def create_converter(self, format_type):
        if format_type == 'csv':
            return CSVConverter()
        elif format_type == 'json':
            return JSONConverter()
        elif format_type == 'yaml':
            return YAMLConverter()
        else:
            raise ValueError(f'Unsupported format: {format_type}')


# Client Code
if __name__ == '__main__':
    factory = ConcreteMessageConverterFactory()

    # Convert to CSV
    csv_converter = factory.create_converter('csv')
    message = {'name': 'John', 'age': 30, 'city': 'New York'}
    csv_converter.convert(message)

    # Convert to JSON
    json_converter = factory.create_converter('json')
    json_converter.convert(message)

    # Convert to YAML
    yaml_converter = factory.create_converter('yaml')
    yaml_converter.convert(message)
