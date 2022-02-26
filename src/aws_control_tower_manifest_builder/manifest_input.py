"""Class for parsing and structuring YAML and JSON"""
import os
import re
import ruamel.yaml
from aws_control_tower_manifest_builder import logger

log = logger.get_logger(__name__)


class ManifestInput:
    """Base Class for SCP and Manifest Objects"""

    def __init__(self, filename, region):
        """
        Base Object to structure Manifest and SCP objects

        Parameters:
        filename(string): Name of file to be loaded
        region(string of aws region): aws region
        """
        self.filename = filename
        file_dict = self.load_yaml(self.filename, True)
        try:
            file_dict["Metadata"]["manifest_parameters"]
        except KeyError:
            self.error = "File does not contain the required metadata"
            return {}, self.error
        self.metadata_dict = (
            self.load_yaml(self.filename, True)
            .get("Metadata")
            .get("manifest_parameters")
        )
        self.name = os.path.basename(filename).split(".")[0]
        self.default_region = region
        if "name" not in self.metadata_dict.keys():
            self.metadata_dict["name"] = self.name
        if "regions" not in self.metadata_dict.keys():
            self.metadata_dict["region"] = self.default_region
        if (
            "accounts" not in self.metadata_dict.keys()
            and "organizational_units" not in self.metadata_dict.keys()
        ):
            self.error = "Missing OU or accounts"
            return {}, self.error
        if "accounts" in self.metadata_dict.keys():
            for account in self.metadata_dict.get("accounts"):
                if not isinstance(account, str):
                    self.error = "Account provided is not a string"
                elif not re.match("[0-9]{12}", account):
                    self.error = "Account provided is not 12 digit"
        if "resource_file" not in self.metadata_dict.keys():
            self.metadata_dict["resource_file"] = self.filename

    @staticmethod
    def load_yaml(content: str, is_file: bool) -> dict:
        """Loads YAML from either a file or a String

        returns: dict
        """
        yaml_dict = {}
        yaml = ruamel.yaml.YAML(typ="safe", pure=True)
        yaml.default_flow_style = False
        try:
            if is_file:
                with open(content, encoding="utf-8") as yaml_file:
                    yaml_dict = yaml.load(yaml_file.read())
            else:
                yaml_dict = yaml.load(content)
        except (IOError, ruamel.yaml.YAMLError) as err:
            log.error(f"Unable to open {content} - {err}")
            return yaml_dict
        if yaml_dict is None:
            log.error("Error, yaml is empty")
            yaml_dict = {}
        return yaml_dict

    @staticmethod
    def write_yaml(filename: str, content: dict):
        """
        Writes yaml file
        """
        yaml = ruamel.yaml.YAML()
        yaml.default_flow_style = False
        try:
            with open(filename, "w", encoding="utf-8") as output_file:
                yaml.dump(content, output_file)
            output_file.close()
        except IOError as err:
            log.error(f"Unable to open {filename} - {err}")


class CfTemplate(ManifestInput):
    """
    Object for structuring CFN Templates
    """

    def __init__(self, filename, region):
        """
        Object for structuring CFN Templates
        """
        self.error = ""
        self.metadata_dict = {}
        self.deploy_method = "stack_set"
        super().__init__(filename, region)
        self.metadata_dict["deploy_method"] = self.deploy_method


class Scp(ManifestInput):
    """
    Object for structuring CFN Templates
    """

    def __init__(self, filename, region):
        """
        Object for structuring CFN Templates
        """
        self.error = ""
        self.deploy_method = "scp"
        self.metadata_dict = {}
        file = filename.replace("yaml", "json")
        if not os.path.exists(filename.replace("yaml", "json")):
            print(f"lookign for {file} if exist ")
            self.error = "File does not have corresponding json file"
        super().__init__(filename, region)
        self.filename = filename.replace("yaml", "json")
        self.metadata_dict["deploy_method"] = self.deploy_method
