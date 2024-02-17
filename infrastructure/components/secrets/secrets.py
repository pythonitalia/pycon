import json
import sys
from subprocess import check_output


def main():
    input_json = sys.stdin.read()
    input_dict = json.loads(input_json)

    service = input_dict["service"]
    workspace = input_dict["workspace"]

    path = f"/pythonit/{workspace}/{service}/"
    aws_output = check_output(["aws", "ssm", "get-parameters-by-path", "--path", path])
    parsed_output = json.loads(aws_output)
    parameters = parsed_output["Parameters"]
    sys.stdout.write(
        json.dumps(
            {
                parameter["Name"].replace(path, "").replace("-", "_"): parameter[
                    "Value"
                ]
                for parameter in parameters
            }
        )
    )


if __name__ == "__main__":
    main()
