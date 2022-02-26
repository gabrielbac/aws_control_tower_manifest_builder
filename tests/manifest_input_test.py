"""Tests for `aws_control_tower_manifest_builder.manifest_input` package."""

import os
import pytest
from src.aws_control_tower_manifest_builder.manifest_input import (
    Scp,
    CfTemplate,
    ManifestInput,
)

DEFAULT_REGION = "us-east-1"
PATH_TO_SCP = "tests/sample_scp"
PATH_TO_CF = "tests/sample_templates"

error_input_data = [
    pytest.param(
        os.path.join(PATH_TO_SCP, "scp_missing_json_error.yaml"),
        "File does not have corresponding json file",
        Scp,
        id="Tests error if SCP yaml does not have corresponding json file",
    ),
    pytest.param(
        os.path.join(PATH_TO_CF, "cf_template_missing_ou_accounts_error.yaml"),
        "Missing OU or accounts",
        CfTemplate,
        id="Tests error if file is missing OU or accounts",
    ),
    pytest.param(
        os.path.join(PATH_TO_CF, "cf_template_account_wrong_length_error.yaml"),
        "Account provided is not 12 digit",
        CfTemplate,
        id="Tests error if account provided is not 12 digit",
    ),
    pytest.param(
        os.path.join(PATH_TO_CF, "cf_template_account_not_string_error.yaml"),
        "Account provided is not a string",
        CfTemplate,
        id="Tests error if account provided is not a string",
    ),
    pytest.param(
        os.path.join(PATH_TO_CF, "empty.yaml"),
        "File does not contain the required metadata",
        CfTemplate,
        id="Tests error if input file has no required metadata",
    ),
]


@pytest.mark.parametrize("file_name, error, file_type", error_input_data)
def test_input_file_throw_error(file_name, error, file_type):
    """Test that input file throw error"""
    new_input = file_type(file_name, DEFAULT_REGION)
    assert new_input.error == error


good_input_data = [
    pytest.param(
        os.path.join(PATH_TO_SCP, "ec2_deny.yaml"),
        {
            "name": "ec2_deny",
            "accounts": ["123456789012", "987456123989"],
            "organizational_units": ["dev", "prod"],
            "regions": ["us-east-1", "us-east-2"],
            "resource_file": "tests/sample_scp/ec2_deny.yaml",
            "deploy_method": "scp",
        },
        Scp,
        id="Tests that SCP yaml is proceesed correctly",
    ),
    pytest.param(
        os.path.join(PATH_TO_CF, "cf_template_minimal.yaml"),
        {
            "accounts": ["123456789012", "987456123989"],
            "name": "cf_template_minimal",
            "region": "us-east-1",
            "resource_file": "tests/sample_templates/cf_template_minimal.yaml",
            "deploy_method": "stack_set",
        },
        CfTemplate,
        id="Tests that input file with only required args is processed",
    ),
    pytest.param(
        os.path.join(PATH_TO_CF, "cf_template_detailed.yaml"),
        {
            "name": "detailed_template",
            "deploy_method": "stack_set",
            "accounts": ["123456789012", "987456123989"],
            "organizational_units": ["dev", "prod"],
            "regions": ["us-east-1", "us-east-2"],
            "parameters": [
                {"parameter_key": "parameter1", "parameter_value": "value1"},
                {"parameter_key": "parameter2", "parameter_value": "value2"},
            ],
            "export_outputs": [
                {
                    "name": "/org/member/test-ssm/app-id",
                    "value": "$[output_ApplicationId]",
                }
            ],
            "resource_file": "tests/sample_templates/cf_template_detailed.yaml",
        },
        CfTemplate,
        id="Tests that input file with all args is processed",
    ),
    pytest.param(
        os.path.join(PATH_TO_CF, "cf_template_local.yaml"),
        {
            "name": "templateLocalIAM",
            "description": "Template to deploy baseline IAM resources",
            "accounts": ["123456789012", "987456123989"],
            "organizational_units": ["dev", "prod"],
            "regions": ["us-east-1", "us-east-2"],
            "resource_file": "tests/sample_templates/cf_template_local.yaml",
            "deploy_method": "stack_set",
        },
        CfTemplate,
        id="Tests that input file local file is processed",
    ),
    pytest.param(
        os.path.join(PATH_TO_CF, "cf_template_S3.yaml"),
        {
            "name": "testS3",
            "resource_file": "https://s3.amazonaws.com/solutions-reference/\
customizations-for-aws-control-tower/latest/custom-control-tower-initiation.template",
            "accounts": ["123456789012", "987456123989"],
            "organizational_units": ["dev", "prod"],
            "regions": ["us-east-1", "us-east-2"],
            "deploy_method": "stack_set",
        },
        CfTemplate,
        id="Tests that input file with template is S3 is processed",
    ),
]


@pytest.mark.parametrize("file_name, error, file_type", good_input_data)
def test_input_file(file_name, error, file_type):
    """Test that input files are processed correctly"""
    new_input = file_type(file_name, DEFAULT_REGION)
    assert new_input.metadata_dict == error


file_input_data = [
    pytest.param(
        "fake_file",
        "Unable to open fake_file - [Errno 2] No such file or directory",
        id="Test that load_yaml throws error if file does not exists",
    ),
    pytest.param(
        os.path.join(PATH_TO_CF, "empty.yaml"),
        "Error, yaml is empty",
        id="Tests that load_yaml throws error if file is empty",
    ),
]


@pytest.mark.parametrize("file_name, error", file_input_data)
def test_load_yaml_file(file_name, error, caplog):
    """Test that load yaml throws error if file does not exists"""
    ManifestInput.load_yaml(file_name, True)
    assert error in caplog.text


def test_load_yaml_dict():
    """Test that load yaml when input is string"""
    dict = {"hello": "bye"}
    string_dict = str(dict)
    dict = ManifestInput.load_yaml(string_dict, False)
    assert dict == {"hello": "bye"}


def test_write_yaml_error(caplog):
    """Test that write yaml throws error if file does not exists"""
    fake_file = "fake_dir/fake_file"
    ManifestInput.write_yaml(fake_file, {})
    assert f"Unable to open {fake_file}" in caplog.text


def test_write_yaml():
    """Test that write yaml"""
    real_file = "tests/output_manifest/fake_file.yaml"
    ManifestInput.write_yaml(real_file, {"hello"})
    assert os.path.exists(real_file) is True
    os.remove("tests/output_manifest/fake_file.yaml")
