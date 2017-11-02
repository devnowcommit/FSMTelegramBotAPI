# -*- coding:utf-8; -*-

import pytest

from fsm_telebot.storage.base import BaseStorage
from fsm_telebot.storage.memory import MemoryStorage

USER, CHAT = '10100101', '10010101'  # random
STATE, DATA, DATA_UPDATE = 'TEST', {'1': '2'}, {'3': '4'}


class TestStorage:
    def test_address(self):
        base_storage = BaseStorage()

        chat1, user1 = base_storage.check_address(CHAT, USER)
        assert chat1 == CHAT, user1 == USER

        chat2, user2 = base_storage.check_address(None, USER)
        assert chat2 == USER, user2 == USER

        chat3, user3 = base_storage.check_address(CHAT, USER)
        assert chat3 == CHAT, user3 == USER

    def test_memory(self):
        chat, user = CHAT, USER
        state, data, data_update = STATE, DATA.copy(), DATA_UPDATE.copy()
        memory_storage = MemoryStorage()

        memory_storage.set_state(chat, user, state)
        memory_storage.set_data(chat, user, data)
        assert memory_storage.data[chat][user]['state'] == state
        assert memory_storage.data[chat][user]['data'] == data

        memory_storage.update_data(chat, user, data_update)
        data.update(data_update)
        assert memory_storage.data[chat][user]['data'] == data

        memory_storage.finish(chat, user)
        assert memory_storage.data[chat][user] == {'state': None, 'data': {}}

        memory_storage.close()
        assert memory_storage.data == {}

    @pytest.mark.db
    def test_rethinkdb(self, cmdopts):
        from fsm_telebot.storage.rethinkdb import RethinkDBStorage

        chat, user = CHAT, USER
        state, data, data_update = STATE, DATA.copy(), DATA_UPDATE.copy()
        memory_storage = RethinkDBStorage(host=cmdopts.getoption('--dbhost'), port=cmdopts.getoption('--dbport'), db=cmdopts.getoption('--db'),
                                          user=cmdopts.getoption('--dbuser'), password=cmdopts.getoption('--dbpassword'),
                                          timeout=cmdopts.getoption('--dbtimeout'))

        memory_storage.set_state(chat, user, state)
        memory_storage.set_data(chat, user, data)
        assert memory_storage.data[chat][user]['state'] == state
        assert memory_storage.data[chat][user]['data'] == data

        memory_storage.update_data(chat, user, data_update)
        data.update(data_update)
        assert memory_storage.data[chat][user]['data'] == data

        memory_storage.finish(chat, user)
        assert memory_storage.data[chat][user] == {'state': None, 'data': {}}

        memory_storage.close()
        assert memory_storage.data == {}
