"""
Setup script for RuvScan MCP Server
Provides backwards compatibility with setuptools
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ruvscan-mcp",
    version="0.5.0",
    author="Ruvnet",
    author_email="support@ruvnet.ai",
    description="RuvScan MCP Server - Sublinear intelligence for GitHub discovery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ruvnet/ruvscan",
    project_urls={
        "Documentation": "https://github.com/ruvnet/ruvscan#readme",
        "Source": "https://github.com/ruvnet/ruvscan",
        "Tracker": "https://github.com/ruvnet/ruvscan/issues",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.23.0",
            "black>=24.0.0",
            "ruff>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ruvscan-mcp=mcp.mcp_stdio_server:main",
        ],
    },
    keywords="mcp github ai semantic-search sublinear claude",
)
