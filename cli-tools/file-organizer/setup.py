"""Setup script for file-organizer CLI tool."""

from setuptools import setup, find_packages

setup(
    name="file-organizer",
    version="1.0.0",
    description="Automatically organize files into folders by type",
    long_description=open("README.md", encoding="utf-8").read() if False else "CLI tool to organize files by extension type",
    long_description_content_type="text/markdown",
    author="agent-work",
    url="https://github.com/agent-work/file-organizer",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "file-organizer=file_organizer.organizer:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Topic :: Desktop Environment :: File Management",
    ],
)
