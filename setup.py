from setuptools import setup, find_packages

setup(
    name="quantum_staircase",
    version="0.1.0",
    description="Quantum physics‑inspired tiling generator for architectural panels",
    author="Quantum Staircase Team",
    license="MIT",
    packages=find_packages(),
    install_requires=[ln.strip() for ln in open("requirements.txt") if ln.strip() and not ln.startswith("#")],
    entry_points={"console_scripts": ["quantum-staircase=quantum_staircase.cli:main"]},
    python_requires=">=3.9",
)
