"""Main module."""

import os
import sys
from jinja2 import Environment, FileSystemLoader
from datetime import date
from prettytable import PrettyTable

import aws_control_tower_manifest_builder.manifest_input as manifest_input
import aws_control_tower_manifest_builder.logger as logger


log = logger.setup_applevel_logger()
SPACING = "\n\t\t\t\t\t\t\t\t\t"
JINJA_MANIFEST_PATH = os.path.dirname(__file__)


def main(args: None):

    if args:
        template_path = args.input_cf
        policies_path = args.input_scp
        output_path = args.output
        output_manifest_file = os.path.join(output_path, "manifest.yaml")
        default_region = "us-east-1"
        ABORT_IF_ERROR = args.abort_if_error

    final_report = PrettyTable(["Type", "Successes", "Failures", "Totals"])

    log.info("Processing CF Templates from {}".format(template_path))
    cf_resources, cf_successes, cf_failures = loop_through_files(
        template_path, manifest_input.CfTemplate, default_region
    )
    final_report.add_row(
        [
            manifest_input.CfTemplate.__name__,
            cf_successes,
            cf_failures,
            cf_successes + cf_failures,
        ]
    )

    log.info("Processing SCPs from {}".format(policies_path))
    scp_resources, scp_successes, scp_failures = loop_through_files(
        policies_path, manifest_input.Scp, default_region
    )
    final_report.add_row(
        [
            manifest_input.Scp.__name__,
            scp_successes,
            scp_failures,
            scp_successes + scp_failures,
        ]
    )
    final_report.add_row(["-------", "-------", "-------", "-------"])
    final_report.add_row(
        [
            "Totals",
            cf_successes + scp_successes,
            cf_failures + scp_failures,
            cf_successes + scp_successes + cf_failures + scp_failures,
        ]
    )

    data = {"resources": cf_resources + scp_resources}
    data["region"] = default_region
    data["date"] = date.today().strftime("%y-%m-%d")

    e = Environment(loader=FileSystemLoader(JINJA_MANIFEST_PATH))
    template = e.get_template("manifest.yaml.j2")

    manifest = template.render(data)
    manifest_dict = manifest_input.ManifestInput.load_yaml(manifest, False)

    log.info(
        "Results from procesing \n CF templates {} \n SCPs {}".format(
            template_path, policies_path
        )
    )
    log.info(final_report)

    if ABORT_IF_ERROR and (cf_failures + scp_failures) > 0:
        log.info("Skiping writing output YAML file due to failures")
        sys.exit(0)
    log.info("Writing output YAML file {}".format(output_manifest_file))
    manifest_input.ManifestInput.write_yaml(output_manifest_file, manifest_dict)


def loop_through_files(path: str, type: manifest_input, default_region: str) -> list:
    resources = []
    successes = 0
    failures = 0
    for filename in os.scandir(path):
        if filename.is_file() and "yaml" in filename.name:
            if type == manifest_input.CfTemplate or (
                type == manifest_input.Scp
                and os.path.exists(filename.path.replace("yaml", "json"))
            ):
                input = type(filename.path, default_region)
                if input.metadata_dict and not input.error:
                    log.info("Processed .. {}".format(filename.path))
                    resources.append(input.metadata_dict)
                    successes += 1
                else:
                    log.info(
                        "Failed to Process .. {}, {}Error -> {}".format(
                            filename.path, SPACING, input.error
                        )
                    )
                    failures += 1
            else:
                log.info(
                    "Failed to Process .. {}, {}Error -> does not have corresponding \
                    json file".format(
                        filename.path, SPACING
                    )
                )
                failures += 1
    return resources, successes, failures


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
