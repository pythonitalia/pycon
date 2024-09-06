import json
import subprocess
import sys

git_output = subprocess.check_output(
    ["git", "rev-list", "-1", "HEAD", "--", "."],
)
githash = git_output.decode().strip()

output = {"githash": githash}
output_json = json.dumps(output)
sys.stdout.write(output_json)
