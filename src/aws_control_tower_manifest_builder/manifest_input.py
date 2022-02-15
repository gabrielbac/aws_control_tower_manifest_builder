import ruamel.yaml
import os
import re
import aws_control_tower_manifest_builder.logger as logger

log = logger.get_logger(__name__)


class ManifestInput:
    def __init__(self, filename, region):
        self.filename = filename
        self.metadata_dict = (
            self.load_yaml(self.filename, True)
            .get("Metadata")
            .get("manifest_parameters")
        )
        self.name = os.path.basename(filename).split(".")[0]
        self.default_region = region
        self.error = ""
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
                if not re.match("[0-9]{12}", account):
                    self.error = "Account provided {} is not 12 digit".format(account)
        if "resource_file" not in self.metadata_dict.keys():
            self.metadata_dict["resource_file"] = self.filename

    @staticmethod
    def load_yaml(content: str, is_file: bool) -> dict:
        """Loads YAML from either a file or a String

        returns: dict
        """
        yaml = ruamel.yaml.YAML(typ="safe", pure=True)
        yaml.default_flow_style = False
        try:
            if is_file:
                with open(content) as yaml_file:
                    yaml_dict = yaml.load(yaml_file.read())
            else:
                yaml_dict = yaml.load(content)
        except (IOError, ruamel.yaml.YAMLError) as err:
            log.error("Unable to open {} - {}".format(content, err))
        if yaml_dict == {}:
            log.error("Error")
            return False
        return yaml_dict

    @staticmethod
    def write_yaml(filename: str, content: dict) -> None:
        """Writes yaml file

        returns: none
        """
        yaml = ruamel.yaml.YAML()
        yaml.default_flow_style = False
        try:
            with open(filename, "w") as output_file:
                yaml.dump(content, output_file)
            output_file.close()
        except IOError as err:
            log.error("Unable to open {} - {}".format(filename, err))
        return


class CfTemplate(ManifestInput):
    def __init__(self, filename, region):
        self.deploy_method = "stack_set"
        super().__init__(filename, region)
        self.metadata_dict["deploy_method"] = self.deploy_method


class Scp(ManifestInput):
    def __init__(self, filename, region):
        self.deploy_method = "scp"
        super().__init__(filename, region)
        self.filename = filename.replace("yaml", "json")
        self.metadata_dict["deploy_method"] = self.deploy_method
