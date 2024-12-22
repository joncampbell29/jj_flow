from setuptools import setup, find_packages

with open('README.md', "r") as f:
    desc = f.read()
    
with open('requirements.txt', "r") as f:
    reqs = f.read().splitlines()

setup(
    name='jjflow_utils',
    version='0.1.0',
    author='Jon Campbell',
    author_email='campbelljonjr@comcast.net',
    description='Finance data and modeling toolset',
    long_description=desc,
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=reqs,
    entry_points={
        "console_scripts": [
            "jjflow-run=scripts.run_pipeline:main",
            "jjflow-train=scripts.train_models:main",
        ]
    }
)