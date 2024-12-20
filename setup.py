from setuptools import setup, find_packages

with open('README.md', "r") as f:
    desc = f.read()

setup(
    name='tradepulse_utils',
    version='0.1.0',
    author='Jon Campbell',
    author_email='campbelljonjr@comcast.net',
    description='Finance data and modeling toolset',
    long_description=desc,
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=[
        "numpy", 
        "pandas",
        "psycopg2",
        "requests",
        "yfinance",
        "pyyaml",
        "scikit-learn",
        "python-dotenv",
        "fredapi",
        "alpaca-py",
        "bs4",
        "luigi"
    ],
    entry_points={
        "console_scripts": [
            "tradepulse-run=scripts.run_pipeline:main",
            "tradepulse-train=scripts.train_models:main",
        ]
    }
)