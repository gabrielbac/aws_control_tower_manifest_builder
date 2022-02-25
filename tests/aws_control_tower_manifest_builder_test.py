"""Tests for `aws_control_tower_manifest_builder.aws_control_tower_manifest_builder` package."""

import pytest
from src.aws_control_tower_manifest_builder.aws_control_tower_manifest_builder import (
    loop_through_files,
)
from src.aws_control_tower_manifest_builder.manifest_input import Scp, CfTemplate

default_region = "us-east-1"

input_data = [
    pytest.param(
        "tests/sample_scp",
        Scp,
        default_region,
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
    ),
    pytest.param(
        "tests/sample_templates",
        CfTemplate,
        default_region,
        [
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
            {
                "name": "testS3",
                "resource_file": "https://s3.amazonaws.com/solutions-reference/customizations-for-aws-control-tower/latest/custom-control-tower-initiation.template",
                "accounts": ["123456789012", "987456123989"],
                "organizational_units": ["dev", "prod"],
                "regions": ["us-east-1", "us-east-2"],
                "deploy_method": "stack_set",
            },
        ],
        4,
        4,
    ),
]


@pytest.mark.parametrize(
    "path, manifest_type, default_region, resources, successes, failures", input_data
)
def test_loop_through_files_success(
    path, manifest_type, default_region, resources, successes, failures
):
    o_resources, o_successes, o_failures = loop_through_files(
        path, manifest_type, default_region
    )
    assert o_successes == successes


@pytest.mark.parametrize(
    "path, manifest_type, default_region, resources, successes, failures", input_data
)
def test_loop_through_files_failures(
    path, manifest_type, default_region, resources, successes, failures
):
    o_resources, o_successes, o_failures = loop_through_files(
        path, manifest_type, default_region
    )
    assert o_failures == failures


@pytest.mark.parametrize(
    "path, manifest_type, default_region, resources, successes, failures", input_data
)
def test_loop_through_files_resources(
    path, manifest_type, default_region, resources, successes, failures
):
    o_resources, o_successes, o_failures = loop_through_files(
        path, manifest_type, default_region
    )
    print(o_resources)
    assert o_resources == resources
