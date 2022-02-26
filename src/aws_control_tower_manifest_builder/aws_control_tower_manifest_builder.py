"""Main module."""

import os
import sys
from datetime import date
from jinja2 import Environment, FileSystemLoader
from prettytable import PrettyTable
from . import manifest_input
from . import logger

log = logger.setup_applevel_logger()
SPACING = "\n\t\t\t\t\t\t\t\t\t"
JINJA_MANIFEST_PATH = os.path.dirname(__file__)


def main(args: None):
    """
    Process user arguments and render Control Tower manifest

    Parameters:
    args(dictionary): dicitonary of arguments
    {"input_cf": PATH}
    """

    if args:
        output_manifest_file = os.path.join(args.output, "manifest.yaml")
        default_region = "us-east-1"

    final_report = PrettyTable(["Type", "Successes", "Failures", "Totals"])

    log.info("Processing CF Templates from %s", args.input_cf)
    cf_resources, cf_successes, cf_failures = loop_through_files(
        args.input_cf, manifest_input.CfTemplate, default_region
    )
    final_report.add_row(
        [
            manifest_input.CfTemplate.__name__,
            cf_successes,
            cf_failures,
            cf_successes + cf_failures,
        ]
    )

    log.info("Processing SCPs from %s", args.input_scp)
    scp_resources, scp_successes, scp_failures = loop_through_files(
        args.input_scp, manifest_input.Scp, default_region
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

    loaded_environment = Environment(loader=FileSystemLoader(JINJA_MANIFEST_PATH))
    manifest = loaded_environment.get_template("manifest.yaml.j2").render(data)
    manifest_dict = manifest_input.ManifestInput.load_yaml(manifest, False)

    log.info(
        "Results from procesing \n CF templates %s \n SCPs %s",
        args.input_cf,
        args.input_scp,
    )
    log.info(final_report)

    if args.abort_if_error and (cf_failures + scp_failures) > 0:
        log.info("Skiping writing output YAML file due to failures")
        sys.exit(0)
    log.info("Writing output YAML file %s", output_manifest_file)
    manifest_input.ManifestInput.write_yaml(output_manifest_file, manifest_dict)


def loop_through_files(
    path: str, manifest_type: manifest_input, default_region: str
) -> list:
    """
    Loop through path and create list of either CfTemplate resources or SCPs

    Parameters:
    path(str): location of CFN or SCP
    manifest_type(manifest_input): which current manifest_type [SCP or CFN] thats beeing looked for.

    Return:
    [resources(list), successes(int), failures(int)]
    """
    resources = []
    successes = 0
    failures = 0
    for filename in sorted(os.listdir(path)):
        path_to_file = os.path.join(path, filename)
        if os.path.isfile(path_to_file) and ".yaml" in filename:
            new_input = manifest_type(path_to_file, default_region)
            if new_input.metadata_dict and not new_input.error:
                log.info("Processed .. %s", path_to_file)
                resources.append(new_input.metadata_dict)
                successes += 1
            else:
                log.info(
                    "Failed to Process .. %s, %sError -> %s",
                    path_to_file,
                    SPACING,
                    new_input.error,
                )
                failures += 1
    return resources, successes, failures


if __name__ == "__main__":
    sys.exit(main(None))  # pragma: no cover
