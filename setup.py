#!/usr/bin/env python

from setuptools import setup

setup(name='check-graylog-lag',
      version='1.0.1',
      description='Nagios plugin to check graylog lag',
      long_description=open('README.md').read(),
      author='Ilya Margolin',
      author_email='ilya@jimdo.com',
      url='https://github.com/fungusakafungus/check-graylog-lag',
      scripts=['check_graylog_lag'],
      install_requires=open('requirements.txt').readlines(),
      classifiers=[
          'Topic :: System :: Monitoring',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
      ],
      )
