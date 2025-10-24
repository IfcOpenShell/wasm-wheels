import glob
import os

# Generate index.html in root listing all .whl files

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IfcOpenShell Pyodide Wheels</title>
</head>
<body>
    <h1>Available IfcOpenShell Pyodide Wheels</h1>
    <p><a href="https://github.com/IfcOpenShell/wasm-wheels#pyodide-test-wheels">See README for details</a></p>
    <ul>
"""

# Find all .whl files in the repo, sorted descending
whl_files = sorted(glob.glob("**/*.whl", recursive=True), reverse=True)

for whl_file in whl_files:
    filename = os.path.basename(whl_file)
    # Since index.html is in root, link to filename
    html_content += f'        <li><a href="{filename}">{filename}</a></li>\n'

html_content += """    </ul>
</body>
</html>
"""

print(html_content)
