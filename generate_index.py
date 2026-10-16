"""Print a wheel index with download paths relative to this repository."""

from collections import defaultdict
from dataclasses import dataclass
from html import escape
from pathlib import Path
from urllib.parse import quote

from packaging.utils import parse_wheel_filename
from packaging.version import Version


@dataclass(frozen=True)
class Wheel:
    path: Path
    package: str
    version: Version
    python: str
    platform: str
    size: int


def format_python(interpreter: str) -> str:
    for prefix, label in (("cp", "CPython"), ("py", "Python")):
        if interpreter.startswith(prefix):
            digits = interpreter[len(prefix):]
            if digits.isdigit():
                version = digits if len(digits) == 1 else f"{digits[0]}.{digits[1:]}"
                return f"{label} {version}"
    return interpreter


def collect_wheels(root: Path) -> list[Wheel]:
    wheels = []
    for path in sorted(root.rglob("*.whl")):
        package, version, _, tags = parse_wheel_filename(path.name)
        wheels.append(Wheel(
            path.relative_to(root), package, version,
            ", ".join(format_python(i) for i in sorted({t.interpreter for t in tags})),
            ", ".join(sorted({t.platform for t in tags})), path.stat().st_size,
        ))
    return wheels


def format_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB"):
        if value < 1024 or unit == "GiB":
            return f"{value:,.1f} {unit}" if unit != "B" else f"{size:,} B"
        value /= 1024


def generate_index(root: Path) -> str:
    wheels = collect_wheels(root)
    groups = defaultdict(list)
    for wheel in sorted(wheels, key=lambda w: (w.package, w.path.as_posix())):
        modular = wheel.path.parts[0] == "modular"
        groups[wheel.version, wheel.path.parent if modular else wheel.path].append(wheel)

    parts = ["""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IfcOpenShell Pyodide Wheels</title>
    <style>
        :root { color-scheme: light dark; font-family: system-ui, sans-serif; }
        body { max-width: 1200px; margin: 0 auto; padding: 2rem 1rem; line-height: 1.5; }
        a { color: light-dark(#1764a0, #83c6ff); }
        h1 { margin-bottom: .3rem; }
        .intro { color: light-dark(#555, #bbb); }
        .table-wrap { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; font-size: .9rem; }
        th, td { text-align: left; padding: .6rem; border-bottom: 1px solid #8884; }
        th { white-space: nowrap; }
        td:first-child { min-width: 15rem; }
        td:last-child { white-space: nowrap; }
        .modular-group { background: #8881; }
        .modular-wheel td:first-child { padding-left: 2rem; }
        code { font-size: .85em; overflow-wrap: anywhere; }
        .filename { display: block; font-size: .75rem; margin-top: .2rem; overflow-wrap: anywhere; }
    </style>
</head>
<body>
    <h1>IfcOpenShell Pyodide Wheels</h1>
    <p class="intro">Download a wheel or copy its link to install with micropip.</p>
    <p><a href="https://github.com/IfcOpenShell/wasm-wheels#pyodide-test-wheels">Installation and repository details</a></p>
""", f"    <p>{len(wheels)} wheels available.</p>"]

    parts.append('    <div class="table-wrap"><table>')
    parts.append('    <thead><tr><th scope="col">Package / download</th><th scope="col">Version</th>'
                 '<th scope="col">Python</th><th scope="col">Platform</th>'
                 '<th scope="col">Size</th></tr></thead>')
    for (version, path), rows in sorted(groups.items(), key=lambda item: item[0][0], reverse=True):
        modular = path.parts[0] == "modular"
        parts.append("    <tbody>")
        if modular:
            parts.append(
                f'    <tr class="modular-group"><th scope="rowgroup">{escape(path.as_posix())}</th>'
                f'<td>{escape(str(version))}</td><td colspan="3">{len(rows)} wheels</td></tr>'
            )
        for wheel in rows:
            url = escape(quote(wheel.path.as_posix(), safe="/"), quote=True)
            row_class = ' class="modular-wheel"' if modular else ""
            parts.append(
                f'    <tr{row_class}><td><a href="{url}">{escape(wheel.package)}</a>'
                f'<span class="filename">{escape(wheel.path.as_posix())}</span></td>'
                f"<td>{escape(str(wheel.version))}</td><td>{escape(wheel.python)}</td>"
                f"<td><code>{escape(wheel.platform)}</code></td><td>{format_size(wheel.size)}</td></tr>"
            )
        parts.append("    </tbody>")
    parts.append("    </table></div>")
    if not wheels:
        parts.append("    <p>No wheels available yet.</p>")
    parts.append("</body>\n</html>\n")
    return "\n".join(parts)


if __name__ == "__main__":
    print(generate_index(Path(__file__).resolve().parent), end="")
