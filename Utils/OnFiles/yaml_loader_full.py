import sys
import yaml as y
import re
import logging

logger = logging.getLogger(__name__)


class YamlLoader:
    def __init__(self, configfile_name: str):
        self.configfile_name = configfile_name

    def load(self) -> [dict | bool]:
        try:
            with open(self.configfile_name) as stream:
                logger.info('Loading configuration file: ' + self.configfile_name)
                for i, yamlres in enumerate(y.safe_load_all(stream)):
                    # print(yamlres)
                    if YamlLoader.check_structure(yamlres):
                        logger.info(f"successfully loaded document {i}")
                        yield yamlres
                    else:
                        logger.warning(f"document {i} not loaded")
        except FileNotFoundError:
            logger.critical("Config file not found, maybe incorrect path?")
            sys.exit(-1)
        except y.YAMLError as exc:  # exception on YAML syntax
            if hasattr(exc, 'problem_mark'):
                logger.warning(f"Error in YAML file {stream.name}, line {exc.problem_mark.line + 1}")
            else:
                logger.warning(exc)
            return False

    # static method to check correct fields spelling and their presence
    @staticmethod
    def check_structure(yaml_content: dict) -> bool:
        required_fields = {'broker': r"^(((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4})$|^localhost$",
                           'port': r"^(?:[1-9]\d{0,3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$",
                           'inTopic': r"^([a-zA-Z0-9_\-#]+/?)*[a-zA-Z0-9_\-#]+$",
                           'outTopic': r"^([a-zA-Z0-9_\-#]+/?)*[a-zA-Z0-9_\-#]+$",
                           'retain': re.compile(r"^true$|^false$", re.IGNORECASE),
                           'function': r"^([a-zA-Z0-9_\-])+$",
                           'parameters': r"^([a-zA-Z0-9_\-])+$",
                           'outFormat': r'\b(json|xml|yaml|csv)\b',
                           'inFormat': r'\b(json|xml|yaml|csv)\b'}

        # catches and enlightens missing keys from YAML file
        wrong_fields = []

        logger.debug("spell checking... ")

        for field, pattern in required_fields.items():
            if field not in yaml_content:
                wrong_fields.append(field)
                continue

            value = yaml_content[field]

            # "function" and "outTopic" fields might contain a list of functions, we check all of them
            if isinstance(value, list):
                for v in value:
                    if not re.match(pattern, v):
                        wrong_fields.append(field)
            else:
                if not re.match(pattern, str(value)):
                    wrong_fields.append(field)
        try:
            if wrong_fields:
                raise ValueError()
            else:
                logger.debug("configuration file is valid")
            # all checked, return True
            logger.debug("... end of spell checking")
            return True
        except ValueError:
            logger.warning(f"the following fields are wrong or missing: {wrong_fields}")
            return False
