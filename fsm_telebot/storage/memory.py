# -*- coding:utf-8; -*-

import typing

from .base import BaseStorage


class MemoryStorage(BaseStorage):
    """
    Memory storage. Not recommended for production due to losing states after restart.
    """
    def __init__(self):
        self.data = {}

    def _get_chat(self, chat_id):
        """
        Get chat data if exists, else create ones
        :param chat_id:
        :return: Chat data
        """
        chat_id = str(chat_id)
        if chat_id not in self.data:
            self.data[chat_id] = {}
        return self.data[chat_id]

    def _get_user(self, chat_id, user_id):
        """
        Get user state and data if exists, else create ones
        :param chat_id:
        :param user_id:
        :return: User data
        """
        self._get_chat(chat_id)
        chat_id = str(chat_id)
        user_id = str(user_id)
        if user_id not in self.data[chat_id]:
            self.data[chat_id][user_id] = {'state': None, 'data': {}}
        return self.data[chat_id][user_id]

    def set_state(self,
                  chat: typing.Union[int, str, None] = None,
                  user: typing.Union[int, str, None] = None,
                  state: typing.Optional[typing.AnyStr] = None):
        """
        Set state for user in chat
        :param chat: Chat id
        :param user: User id
        :param state:
        :return:
        """
        chat, user = self.check_address(chat, user)
        user = self._get_user(chat, user)
        user['state'] = state

    def set_data(self,
                 chat: typing.Union[int, str, None] = None,
                 user: typing.Union[int, str, None] = None,
                 data: typing.Dict = None):
        """
        Set data for user in chat
        :param chat: Chat id
        :param user: User id
        :param data:
        :return:
        """
        chat, user = self.check_address(chat, user)
        user = self._get_user(chat, user)
        user['data'] = data

    def get_state(self,
                  chat: typing.Union[int, str, None] = None,
                  user: typing.Union[int, str, None] = None,
                  default: typing.Optional[str] = None) -> typing.Union[str]:
        """
        Get state for user in chat
        :param chat: Chat id
        :param user: User id
        :param default: Returns if no state.
        :return: User state
        """
        chat, user = self.check_address(chat, user)
        user = self._get_user(chat, user)
        return user['state'] or default

    def get_data(self,
                 chat: typing.Union[int, str, None] = None,
                 user: typing.Union[int, str, None] = None,
                 default: typing.Optional[str] = None) -> typing.Dict:
        """
        Get state for user in chat
        :param chat: Chat id
        :param user: User id
        :param default: Returns if no data.
        :return: User data
                """
        chat, user = self.check_address(chat, user)
        user = self._get_user(chat, user)
        return user['data']

    def update_data(self,
                    chat: typing.Union[int, str, None] = None,
                    user: typing.Union[int, str, None] = None,
                    data: typing.Dict = None):
        """
        Update user data
        :param chat: Chat id
        :param user: User id
        :param data: Data to update
        :return:
        """
        chat, user = self.check_address(chat, user)
        user = self._get_user(chat, user)
        user['data'].update(data)

    def close(self):
        """
        Delete all data
        :return:
        """
        self.data.clear()
