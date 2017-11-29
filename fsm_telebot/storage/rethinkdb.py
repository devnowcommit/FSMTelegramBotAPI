# -*- coding:utf-8; -*-

import typing
import atexit

import rethinkdb as r

from .base import BaseStorage


class RethinkDBStorage(BaseStorage):
    """
    Storage based on RethinkDB
    """
    def __init__(self,
                 host: typing.Optional[typing.AnyStr] = 'localhost',
                 port: typing.Optional[int] = 28015,
                 db: typing.Optional[typing.AnyStr] = 'FSMBot',
                 table: typing.Optional[typing.AnyStr] = 'states',
                 user: typing.Optional[typing.AnyStr] = 'FSMBot',
                 password: typing.Optional[typing.AnyStr] = 'FSMBot',
                 timeout: typing.Union[int, float] = 20,
                 ssl: typing.Dict = None,
                 **kwargs):
        self._host = host
        self._port = port
        self._db = db
        self._table = table
        self._user = user
        self._port = port
        self._password = password
        self._timeout = timeout
        self._ssl = ssl if ssl else {}
        self._kwargs = kwargs
        self._connection = self._connect()
        self._initialize()
        atexit.register(self.close)

    def _initialize(self):
        """
        Initialize DB and table
        :return:
        """

        if self._db not in r.db_list().run(self._connection):
            r.db_create(self._db).run(self._connection)

        self._connection.use(self._db)

        if self._table not in r.table_list().run(self._connection):
            r.table_create(self._table)

    def _connect(self):
        """
        Connect to RethinkDB
        :return: RethinkDB connection
        """
        return r.connect(host=self._host, port=self._port,
                         user=self._user, password=self._password,
                         timeout=self._timeout, ssl=self._ssl, **self._kwargs)

    def close(self):
        """
        Close connection with RethinkDB
        :return:
        """
        self._connection.close()

    def _set_record(self,
                    chat: typing.Union[int, str, None] = None,
                    user: typing.Union[int, str, None] = None,
                    state=None,
                    data=None,
                    update_data: typing.Optional[bool] = None):
        """
        Make record in RethinkDB
        :param chat: Chat id
        :param user: User id
        :param state: New state
        :param data: New data
        :param update_data: If true, updates data in DB, else rewrites data
        :return:
        """

        if not data:
            data = {}

        chat, user = map(str, self.check_address(chat, user))
        if r.table('states').get(chat).run(self._connection):
            if update_data:
                r.table('states').get(chat).update({user: {'data': data}}).run(self._connection)
            else:
                r.table('states').get(chat).update({user: {'state': state, 'data': r.literal(data)}}).run(self._connection)
        else:
            r.table('states').insert({'id': chat, user: {'state': state, 'data': data}}).run(self._connection)

    def _get_record(self,
                    chat: typing.Union[int, str, None] = None,
                    user: typing.Union[int, str, None] = None):
        """
        Get record form RethinkDB
        :param chat: Chat id
        :param user: User id
        :return: Record
        """
        chat, user = map(str, self.check_address(chat, user))
        return r.table('states').get(chat).default({})[user].default({'state': None, 'data': {}}).run(self._connection)

    @property
    def data(self):
        """
        Return all data from RethinkDB
        :return: Records
        """
        if not self._connection.is_open():
            return {}
        records = list(r.table('states').run(self._connection))
        result = {}
        for chat in records:
            result[chat.pop('id')] = chat
        return result

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
        record = self._get_record(chat, user)
        self._set_record(chat, user, state=state, data=record['data'])

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
        record = self._get_record(chat, user)
        self._set_record(chat, user, state=record['state'], data=data)

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
        return self._get_record(chat, user)['state'] or default

    def get_data(self,
                 chat: typing.Union[int, str, None] = None,
                 user: typing.Union[int, str, None] = None,
                 default: typing.Optional[str] = None) -> typing.Dict:
        """
        Get data for user in chat
        :param chat: Chat id
        :param user: User id
        :param default: Returns if no data.
        :return: User data
        """
        return self._get_record(chat, user)['data'] or default

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
        self._set_record(chat, user, data=data, update_data=True)
