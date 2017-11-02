# -*- coding:utf-8; -*-

import re

import telebot
from telebot import util

from fsm_telebot.storage.base import BaseStorage, DisabledStorage


class TeleBot(telebot.TeleBot):
    def __init__(self, token, storage=DisabledStorage(), threaded=True, skip_pending=False, num_threads=2):
        assert issubclass(storage.__class__, BaseStorage)
        self.storage = storage
        super(TeleBot, self).__init__(token, threaded=threaded, skip_pending=skip_pending, num_threads=num_threads)

    def message_handler(self, state=None, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        """
        Message handler decorator.
        This decorator can be used to decorate functions that must handle certain types of messages.
        All message handlers are tested in the order they were added.

        Example:

        bot = TeleBot('TOKEN')

        # Handles all messages which text matches regexp.
        @bot.message_handler(regexp='someregexp')
        def command_help(message):
            bot.send_message(message.chat.id, 'Did someone call for help?')

        # Handle all sent documents of type 'text/plain'.
        @bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
        def command_handle_document(message):
            bot.send_message(message.chat.id, 'Document received, sir!')

        # Handle all other commands.
        @bot.message_handler(func=lambda message: True, content_types=['audio', 'video', 'document', 'text', 'location', 'contact',
        'sticker'])
        def default_command(message):
            bot.send_message(message.chat.id, "This is the default command handler.")

        # Handle message from user with state 'test'
        @bot.message_handler(state='test'
        def state_handle(message):
            bot.send_message(message.chat.id, "Your state is 'test'")

        :param commands: Optional list of commands, those commands will be handled by this handler.
        :param state: Optional state, user must have this state to handle his commands.
        :param regexp: Optional regular expression.
        :param func: Optional lambda function. The lambda receives the message to test as the first parameter. It must return True if the
        command should handle the message.
        :param content_types: This commands' supported content types. Must be a list. Defaults to ['text'].
        """
        if not content_types:
            content_types = ['text']

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler,
                                                    state=state,
                                                    commands=commands,
                                                    regexp=regexp,
                                                    func=func,
                                                    content_types=content_types,
                                                    **kwargs)

            self.add_message_handler(handler_dict)

            return handler

        return decorator

    def edited_message_handler(self, state=None, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        if not content_types:
            content_types = ['text']

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler,
                                                    state=state,
                                                    commands=commands,
                                                    regexp=regexp,
                                                    func=func,
                                                    content_types=content_types,
                                                    **kwargs)
            self.add_edited_message_handler(handler_dict)
            return handler

        return decorator

    def channel_post_handler(self, state=None, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        if not content_types:
            content_types = ['text']

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler,
                                                    state=state,
                                                    commands=commands,
                                                    regexp=regexp,
                                                    func=func,
                                                    content_types=content_types,
                                                    **kwargs)
            self.add_channel_post_handler(handler_dict)
            return handler

        return decorator

    def inline_handler(self, func, state=None, **kwargs):
        def decorator(handler):
            handler_dict = self._build_handler_dict(handler, func=func, state=state, **kwargs)
            self.add_inline_handler(handler_dict)
            return handler

        return decorator

    def chosen_inline_handler(self, func, state=None, **kwargs):
        def decorator(handler):
            handler_dict = self._build_handler_dict(handler, func=func, state=state, **kwargs)
            self.add_chosen_inline_handler(handler_dict)
            return handler

        return decorator

    def callback_query_handler(self, func, state=None, **kwargs):
        def decorator(handler):
            handler_dict = self._build_handler_dict(handler, func=func, state=state, **kwargs)
            self.add_callback_query_handler(handler_dict)
            return handler

        return decorator

    def shipping_query_handler(self, func, state=None, **kwargs):
        def decorator(handler):
            handler_dict = self._build_handler_dict(handler, func=func, state=state, **kwargs)
            self.add_shipping_query_handler(handler_dict)
            return handler

        return decorator

    def pre_checkout_query_handler(self, func, state=None, **kwargs):
        def decorator(handler):
            handler_dict = self._build_handler_dict(handler, func=func, state=state, **kwargs)
            self.add_pre_checkout_query_handler(handler_dict)
            return handler

        return decorator

    def _test_filter(self, filter, filter_value, message):
        test_cases = {
            'state': lambda msg: self.storage.get_state(msg.chat.id, msg.from_user.id, default='') == filter_value
            if msg.from_user else self.storage.get_state(msg.chat.id, default='') == filter_value,
            'content_types': lambda msg: msg.content_type in filter_value,
            'regexp': lambda msg: msg.content_type == 'text' and re.search(filter_value, msg.text, re.IGNORECASE),
            'commands': lambda msg: msg.content_type == 'text' and util.extract_command(msg.text) in filter_value,
            'func': lambda msg: filter_value(msg)
        }

        return test_cases.get(filter, lambda msg: False)(message)

    def set_state(self, state, chat_id=None, user_id=None):
        """
        Set state for user in chat.
        At least chat_id or user_id must be passed.
        :param state:
        :param chat_id: Optional.
        :param user_id: Optional.
        :return:
        """
        self.storage.set_state(chat_id, user_id, state)

    def set_data(self, data, chat_id=None, user_id=None):
        """
        Set data for user in chat.
        At least chat_id or user_id must be passed.
        :param data:
        :param chat_id: Optional.
        :param user_id: Optional.
        :return:
        """
        self.storage.set_data(chat_id, user_id, data)

    def get_state(self, chat_id=None, user_id=None, default=None):
        """
        Get state for user in chat.
        At least chat_id or user_id must be passed.
        :param chat_id: Optional.
        :param user_id: Optional.
        :param default: Optional. Returns if no state
        :return:
        """
        self.storage.get_state(chat_id, user_id, default=default)

    def get_data(self, chat_id=None, user_id=None, default=None):
        """
        Get data for user in chat.
        At least chat_id or user_id must be passed.
        :param chat_id: Optional.
        :param user_id: Optional.
        :param default: Optional. Returns if no data
        :return:
        """
        self.storage.get_state(chat_id, user_id, default=default)

    def update_data(self, data, chat_id=None, user_id=None):
        """
        Update data for user in chat.
        At least chat_id or user_id must be passed.
        :param data:
        :param chat_id: Optional.
        :param user_id: Optional.
        :return:
        """
        self.storage.update_data(chat_id, user_id, data=data)

    def reset_state(self, chat_id=None, user_id=None):
        """
        Reset state for user in chat.
        At least chat_id or user_id must be passed.
        :param chat_id: Optional
        :param user_id: Optional
        :return:
        """
        self.storage.reset_state(chat_id, user_id)

    def reset_data(self, chat_id=None, user_id=None):
        """
        Reset data for user in chat.
        At least chat_id or user_id must be passed.
        :param chat_id: Optional
        :param user_id: Optional
        :return:
        """
        self.storage.reset_data(chat_id, user_id)

    def finish_user(self, chat_id=None, user_id=None):
        """
        Reset all for user in chat.
        At least chat_id or user_id must be passed.
        :param chat_id: Optional
        :param user_id: Optional
        :return:
        """
        self.storage.finish(chat_id, user_id)
