import csv
import json
from typing import Any
import xml.etree.ElementTree as et

import yaml

from Utils.UserFunctions.user_functions import Service


class MethodToolBox:

    def __init__(self):
        self.services = {str.lower(cls.__name__): cls() for cls in Service.__subclasses__()}

    def process(self, conf: dict, data: Any) -> Any:
        # normalize input
        data = self.normalize_input(conf['inFormat'], data)

        # process normalized input using function chain
        for f in conf['function']:
            if f in self.services.keys():
                data = self.services[f].serve(conf, data)

        # convert in requested format and return

        if isinstance(data, dict):
            for k, v in data.values():
                data[k] = self.convert_output(conf['outFormat'], v)
            return data  # will return a dict where every value is converted

        return self.convert_output(conf['outFormat'], data)

    @staticmethod
    def normalize_input(input_format: str, data: Any) -> [dict]:
        if input_format == 'csv':
            # Assume che input_data sia una stringa CSV
            reader = csv.DictReader(data.splitlines())
            return [row for row in reader]
        elif input_format == 'xml':
            # Assume che input_data sia una stringa XML
            root = et.fromstring(data)
            return [{child.tag: child.text for child in root}]
        elif input_format == 'json':
            # Assume che input_data sia una stringa JSON
            return json.loads(data)
        elif input_format == 'yaml':
            # Assume che input_data sia una stringa YAML
            return yaml.safe_load(data)
        else:
            raise ValueError("input format is not supported")

    @staticmethod
    def convert_output(output_format: str, data: Any) -> Any:
        if output_format == 'yaml':
            return yaml.dump(data)
        elif output_format == 'xml':
            root = et.Element(tag="data")
            for item in data:
                entry = et.SubElement(root, tag="entry")
                for key, value in item.items():
                    sub_element = et.SubElement(entry, key)
                    sub_element.text = str(value)
            return et.tostring(root, encoding="unicode")
        elif output_format == 'csv':
            keys = data[0].keys()
            output = ",".join(keys) + "\n"
            for item in data:
                output += ",".join(str(item[key]) for key in keys) + "\n"
            return output
        elif output_format == 'json':
            return json.dumps(data, indent=4)
        else:
            raise ValueError("Invalid output format. Supported formats: 'yaml', 'xml', 'csv', 'json'")


if __name__ == '__main__':
    m = MethodToolBox()

    # Esempio di dati CSV
    csv_data = """name,age,city
    Alice,30,Roma
    Bob,25,Milano
    Charlie,22,Napoli"""

    # Esempio di dati XML
    xml_data = """<persons>
        <person>
            <name>Alice</name>
            <age>30</age>
            <city>Roma</city>
        </person>
        <person>
            <name>Bob</name>
            <age>25</age>
            <city>Milano</city>
        </person>
        <person>
            <name>Charlie</name>
            <age>22</age>
            <city>Napoli</city>
        </person>
    </persons>"""

    # Esempio di dati JSON
    import json

    json_data = [
        {
            "name": "Alice",
            "age": 30,
            "city": "Roma"
        },
        {
            "name": "Bob",
            "age": 25,
            "city": "Milano"
        },
        {
            "name": "Charlie",
            "age": 22,
            "city": "Napoli"
        }
    ]

    # Esempio di dati YAML
    import yaml

    yaml_data = """
    - name: Alice
      age: 30
      city: Roma
    - name: Bob
      age: 25
      city: Milano
    - name: Charlie
      age: 22
      city: Napoli
    """
    print(m.normalize_input('csv', csv_data))
    print(m.normalize_input('xml', xml_data))
    print(m.normalize_input('yaml', yaml_data))
    print(m.normalize_input('json', json.dumps(json_data)))