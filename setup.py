from setuptools import find_packages, setup


f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='tradestation',
    version='0.1',
    description='An unofficial SDK for Tradestation!',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Graeme Holliday',
    author_email='graeme.holliday@pm.me',
    url='https://github.com/tastyware/tradestation',
    license='MIT',
    install_requires=[
        'httpx>=0.27.0',
    ],
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'tradestation': ['py.typed']},
    include_package_data=True
)
