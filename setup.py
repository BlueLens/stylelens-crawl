import os
import re

from setuptools import setup, find_packages

requires = [
    'Scrapy>=1.4',
    'requests>=2.18.4',
    'beautifulsoup4>=4.6.0',
    'js2xml>=0.3.1',
    'google-api-python-client==1.6.4'
]

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


def get_version():
    init = open(os.path.join(os.path.join(ROOT, 'stylelens_crawl'), '__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='stylelens-crawl',
    version=get_version(),
    description='The Stylens crawler for Python',
    long_description=open('README.rst').read(),
    author='Bluehack',
    author_email='devops@bluehack.net',
    url='https://github.com/BlueLens/stylelens-crawl',
    scripts=[],
    package_data={
        # 'stylelens_crawl': [
        #     'data/*/*.csv',
        # ]
    },
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=requires,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 1 - Planning',
    ],
)
