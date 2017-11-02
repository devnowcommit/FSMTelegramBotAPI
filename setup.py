# -*- coding: utf-8; -*-
from distutils.core import setup

setup(
        name='FSMTelegramBotAPI',
        version='0.0.1',
        packages=['fsm_telebot'],
        url='https://github.com/Ars2014/FSMTelegramBotAPI',
        license='GNU GPLv2',
        author="Arslan 'Ars2014' Sakhapov",
        author_email='ars2014@etlgr.com',
        description='Final-state machine wrapper for pyTelegramBotAPI',
        keywords='telegram bot api tools wrapper',
        install_requires=['pyTelegramBotAPI'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Environment :: Console',
            'Topic :: Software Development',
            'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
            'Natural Language :: English',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: Unix',
            'Operating System :: MacOS',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: Implementation :: PyPy',
        ]
)
