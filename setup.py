"""
MCP Ad Manager Ultimate - 最强大的Google Ad Manager MCP服务器
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mcp-admanager-ultimate",
    version="1.0.0",
    author="chre3",
    author_email="chremata3@gmail.com",
    description="最强大的Google Ad Manager MCP服务器，提供完整的功能支持",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chre3/mcp-admanager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.18.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcp-admanager-ultimate=mcp_admanager_ultimate.server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mcp_admanager_ultimate": ["config/*.json", "docs/*.md"],
    },
    keywords="google ad manager mcp server",
    project_urls={
        "Bug Reports": "https://github.com/chre3/mcp-admanager/issues",
        "Source": "https://github.com/chre3/mcp-admanager",
        "Documentation": "https://github.com/chre3/mcp-admanager/blob/main/README.md",
    },
)
