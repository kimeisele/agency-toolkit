"""
Setup script for Agency Toolkit
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="agency-toolkit",
    version="1.0.0",
    description="Professional automation toolkit for agencies - Built on Genesis Core architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Agency Toolkit Team",
    python_requires=">=3.8",
    packages=find_packages(exclude=["tests*", "examples*"]),
    install_requires=[
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
        ],
        "imaging": [
            "Pillow>=9.0.0",
        ],
        "pdf": [
            "fpdf2>=2.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "agency-toolkit=cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
