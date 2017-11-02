# -*- coding:utf-8; -*-

import time

from telebot import types

import fsm_telebot
from fsm_telebot.storage.memory import MemoryStorage

USER, CHAT = '10100101', '10010101'  # random
STATE, DATA, DATA_UPDATE = 'TEST', {'1': '2'}, {'3': '4'}


class TestTeleBot:
    @staticmethod
    def create_text_message(text):
        params = {'text': text}
        chat = types.User(11, False, 'test')
        return types.Message(1, None, None, chat, 'text', params)

    def test_message_handler(self):
        storage = MemoryStorage()
        bot = fsm_telebot.TeleBot('', storage=storage)
        msg = self.create_text_message('1')
        bot.set_state('Test', 11)

        @bot.message_handler(state='Test')
        def state_handler(message):
            message.text = 'Test'

        bot.process_new_messages([msg])
        time.sleep(1)

        assert msg.text == 'Test'

    def test_storage_methods(self):
        chat, user = CHAT, USER
        state, data, data_update = STATE, DATA.copy(), DATA_UPDATE.copy()

        memory_storage = MemoryStorage()
        bot = fsm_telebot.TeleBot('', storage=memory_storage)

        bot.set_state(state, chat, user)
        bot.set_data(data, chat, user)
        assert memory_storage.data[chat][user]['state'] == state
        assert memory_storage.data[chat][user]['data'] == data

        bot.update_data(data_update, chat, user)
        data.update(data_update)
        assert memory_storage.data[chat][user]['data'] == data

        bot.finish_user(chat, user)
        assert memory_storage.data[chat][user] == {'state': None, 'data': {}}

        memory_storage.close()
