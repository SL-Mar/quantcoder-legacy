from setuptools import setup, find_packages
from pathlib import Path

readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="quantcli",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "Click>=8.0",
        "requests>=2.32.0",
        "pdfplumber>=0.11.0",
        "spacy>=3.8.0",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "pygments>=2.19.0",
        "inquirerpy>=0.3.4",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "quantcli=quantcli.cli:cli",
        ],
    },
    author="SL-MAR",
    author_email="smr.laignel@gmail.com",
    description="Generate QuantConnect trading algorithms from research papers using AI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SL-Mar/quantcoder-legacy",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
