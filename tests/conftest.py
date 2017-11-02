# -*- coding:utf-8; -*-

import pytest


def pytest_addoption(parser):
    parser.addoption('--dbhost', action='store', default='localhost', help='DB host')
    parser.addoption('--dbport', action='store', type=int, default=28015, help='DB port')
    parser.addoption('--db', action='store', default='FSMBot', help='DB name')
    parser.addoption('--dbuser', action='store', default='FSMBot', help='DB user')
    parser.addoption('--dbpassword', action='store', default='FSMBot', help='DB password')
    parser.addoption('--dbtimeout', action='store', type=int, default=20, help='DB timeout')
    parser.addoption('--no-db', action='store_true', default=False, help='Skip DB storage test')


def pytest_collection_modifyitems(config, items):
    if not config.getoption('--no-db'):
        return
    skip_db = pytest.mark.skip(reason='--no-db flag was passed')
    for item in items:
        if 'db' in item.keywords:
            item.add_marker(skip_db)


@pytest.fixture
def cmdopts(request):
    return request.config
