from setuptools import setup, find_packages

setup(
    name="celltypeAgent",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pandas",
        "requests",
        "rich>=13.0.0",
        "click>=8.0.0"
    ],
    entry_points={
        'console_scripts': [
            'celltype-agent=celltypeAgent.cli:main',
        ],
    },
)