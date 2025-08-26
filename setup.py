from setuptools import setup, find_packages

setup(
    name='fastapi_service',               # Your package name
    version='1.0',                   # Initial version
    description='A sample Python package to run the production grade service',
    author='Tushar Sharma',
    author_email='tushar5353@gmail.com',
    packages=find_packages(),        # Finds all packages automatically
    install_requires=[
        'numpy',
        'pandas',
        'fastapi[all]',
        'asgi_correlation_id',
        'confluent_kafka',
        'mysql-connector-python',
        'sqlalchemy'
        # Add your dependencies here
    ],
)

