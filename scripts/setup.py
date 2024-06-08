from setuptools import setup, find_packages

setup(
    name='prompt-engineering-system',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'datasets',
        'pinecone-client',
        'langchain',
        'tqdm',
        'pandas',
        'openai' 
        ],
    entry_points={
        'console_scripts': [
            'prompt-engineering-system=src.main:main',
        ],
    },
)
