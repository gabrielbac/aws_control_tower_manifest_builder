=====
Usage
=====

usage: aws_control_tower_manifest_builder [-h] [--abort-if-error] [--default-region DEFAULT_REGION] --input-cf /path/ --input-scp /path/ [--output /path/]

Produces the manifest.yaml file that works as input for AWS Control Tower

optional arguments:
  -h, --help            show this help message and exit
  --abort-if-error, -a  If set, does not produce the manifest file if any of the input files could not be processed
  --default-region DEFAULT_REGION, -r DEFAULT_REGION
                        Default region for templates with no region. Default us-east-1

  --input-cf /path/, -c /path/
                        the path to the directory containing the cloud formation input files
  --input-scp /path/, -s /path/
                        the path to the directory containing the service control policy input files
  --output /path/, -o /path/
                        the path to store the output manifest.yaml file