# Pyodide Test Wheels

This repository hosts WebAssembly (WASM) wheels for the [ifcopenshell](https://github.com/IfcOpenShell/IfcOpenShell) library, optimized for use with [Pyodide](https://pyodide.org/).

## Purpose

The purpose of this repository is to provide a centralized, publicly accessible source for ifcopenshell wheels, allowing users to install them via URL without needing to host the files themselves.
After [PEP783](https://peps.python.org/pep-0783/) will be accepted, we'll be able to move those wheels to PyPI.

## Available Wheels

The repository contains several versions of ifcopenshell wheels compiled for Pyodide/WASM. An auto-generated index of available wheels is available at: [https://ifcopenshell.github.io/wasm-wheels/](https://ifcopenshell.github.io/wasm-wheels/)

## Installation in Pyodide

To install a wheel in Pyodide:

```python
import micropip
await micropip.install("https://ifcopenshell.github.io/wasm-wheels/ifcopenshell-0.8.3+34a1bc6-cp313-cp313-emscripten_4_0_9_wasm32.whl")
```

Replace the URL with the desired wheel filename from the index.

## Alternatives Considered

Other hosting options were considered:
- Raw files from GitHub repository commits: Do not serve proper CORS headers.
- Files in GitHub Releases: Do not serve proper CORS headers.

GitHub Pages was chosen as it automatically includes Access-Control-Allow-Origin: * headers, enabling cross-origin requests required for Pyodide installations.
