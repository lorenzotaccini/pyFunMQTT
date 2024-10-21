import csv
import json
from io import StringIO
from typing import Any
import xml.etree.ElementTree as et

import yaml

from Utils.UserFunctions.user_functions import Service


class MethodToolBox:

    def __init__(self):
        self.services = {str.lower(cls.__name__): cls() for cls in Service.__subclasses__()}

    # process normalized input using function chain
    def process(self, conf: dict, data: Any) -> Any:

        data = self.normalize_input(conf['format'], data)

        datalist = []
        res = []

        datalist.append(data)
        for f in conf['functions']:  # it's a list of single key dicts, so f is a dict
            for (k, v) in f.items():  # it's a single element, not a real cycle
                if k in self.services.keys():
                    for d in datalist:
                        tmp = self.services[k].serve(v, d)
                        if isinstance(tmp, list):
                            res.extend(tmp)
                        else:
                            res.append(tmp)
            datalist = res

            res = []

        for i in range(len(datalist)):
            datalist[i] = self.convert_output(conf['format'], datalist[i])

        return datalist if len(datalist) > 0 else []

    @staticmethod
    def normalize_input(input_format: str, data: Any) -> [dict]:
        if input_format == 'csv':
            data = data.decode('utf-8')
            reader = csv.DictReader(data.splitlines())
            return [row for row in reader]

        elif input_format == 'xml':
            root = et.fromstring(data)
            return [{child.tag: child.text for child in root}]

        elif input_format == 'json':
            return json.loads(data)

        elif input_format == 'yaml':
            return yaml.safe_load(data)

        elif input_format == 'png':  # do nothing, we just need raw data
            return data

        elif input_format == 'txt':
            data = data.decode('utf-8')
            return data

        else:
            raise ValueError("input input_format is not supported")

    @staticmethod
    def convert_output(output_format: str, data: Any) -> Any:
        print("done")
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

        elif output_format == 'png':
            return data  # do nothing
        elif output_format == 'txt':
            return str(data)  # do nothing
        else:
            raise ValueError("Invalid output input_format. Supported formats: 'yaml', 'xml', 'csv', 'json'")

    @staticmethod
    def convert_list(output_format, lst, item_name):
        if output_format.lower() == 'json':
            return json.dumps(lst, indent=2)
        elif output_format.lower() == 'yaml':
            return yaml.dump(lst, default_flow_style=False)
        elif output_format.lower() == 'csv':
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(lst)
            return output.getvalue().strip()
        elif output_format.lower() == 'xml':
            root = et.Element("root")
            for item in lst:
                child = et.Element(str(item_name))
                child.text = str(item)
                root.append(child)
            return et.tostring(root, encoding='unicode')
        else:
            raise ValueError("Format not supported: " + output_format)


