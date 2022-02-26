"""Tests for `aws_control_tower_manifest_builder.aws_control_tower_manifest_builder` package."""

import pytest
from src.aws_control_tower_manifest_builder.aws_control_tower_manifest_builder import (
    loop_through_files,
)
from src.aws_control_tower_manifest_builder.manifest_input import Scp, CfTemplate

DEFAULT_REGION = "us-east-1"


OUTPUT_CF = (
    [
        {
            "name": "testS3",
            "resource_file": "https://s3.amazonaws.com/solutions-reference/\
customizations-for-aws-control-tower/latest/custom-control-tower-initiation.template",
            "accounts": ["123456789012", "987456123989"],
            "organizational_units": ["dev", "prod"],
            "regions": ["us-east-1", "us-east-2"],
            "deploy_method": "stack_set",
        },
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
        {
            "name": "templateLocalIAM",
            "description": "Template to deploy baseline IAM resources",
            "accounts": ["123456789012", "987456123989"],
            "organizational_units": ["dev", "prod"],
            "regions": ["us-east-1", "us-east-2"],
            "resource_file": "tests/sample_templates/cf_template_local.yaml",
            "deploy_method": "stack_set",
        },
        {
            "accounts": ["123456789012", "987456123989"],
            "name": "cf_template_minimal",
            "region": "us-east-1",
            "resource_file": "tests/sample_templates/cf_template_minimal.yaml",
            "deploy_method": "stack_set",
        },
    ],
    4,
    4,
)

OUTPUT_SCP = (
    [
        {
            "name": "ec2_deny",
            "accounts": ["123456789012", "987456123989"],
            "organizational_units": ["dev", "prod"],
            "regions": ["us-east-1", "us-east-2"],
            "resource_file": "tests/sample_scp/ec2_deny.yaml",
            "deploy_method": "scp",
        }
    ],
    1,
    1,
)

input_data = [
    pytest.param("tests/sample_scp", Scp, DEFAULT_REGION, OUTPUT_SCP),
    pytest.param("tests/sample_templates", CfTemplate, DEFAULT_REGION, OUTPUT_CF),
]


@pytest.mark.parametrize("path, manifest_type, default_region, output", input_data)
def test_loop_through_files_success(path, manifest_type, default_region, output):
    """Test that number of successes match"""
    response = loop_through_files(path, manifest_type, default_region)
    assert response[1] == output[1]


@pytest.mark.parametrize("path, manifest_type, default_region, output", input_data)
def test_loop_through_files_failures(path, manifest_type, default_region, output):
    """Test that number of failures match"""
    response = loop_through_files(path, manifest_type, default_region)
    assert response[2] == output[2]


@pytest.mark.parametrize("path, manifest_type, default_region, output", input_data)
def test_loop_through_files_resources(path, manifest_type, default_region, output):
    """Test that output matches"""
    response = loop_through_files(path, manifest_type, default_region)
    assert response[0] == output[0]
