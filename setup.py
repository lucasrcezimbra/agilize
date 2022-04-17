import os

from setuptools import setup

README = os.path.join(os.path.dirname(__file__), 'README.md')


if __name__ == "__main__":
    setup(
        name='Agilize',
        description='Unofficial client to access Agilize',
        version='0.0.1',
        long_description=open(README).read(),
        long_description_content_type='text/markdown',
        author="Lucas Rangel Cezimbra",
        author_email="lucas@cezimbra.tec.br",
        license="LGPLv2",
        url='https://github.com/lucasrcezimbra/agilize',
        keywords=['agilize', 'api', 'client', 'requests', 'accounting', 'finance'],
        install_requires=['requests'],
        packages=['agilize'],
        zip_safe=False,
        include_package_data=True,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: Implementation :: CPython',
            'Topic :: Office/Business :: Financial',
            'Topic :: Office/Business :: Financial :: Accounting',
        ],
    )
