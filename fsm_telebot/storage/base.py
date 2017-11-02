# -*- coding:utf-8; -*-

import typing


class BaseStorage:
    """
    Parent class for all storages.
    """
    @staticmethod
    def check_address(chat: typing.Union[int, str, None] = None,
                      user: typing.Union[int, str, None] = None) -> (typing.Union[int, str], typing.Union[int, str]):

        if chat is not None and user is not None:
            return chat, user
        elif chat is not None and user is None:
            return chat, chat
        elif chat is None and user is not None:
            return user, user
        raise ValueError('At least one of user or chat parameter must be passed.')

    def close(self):
        """
        Every subclass(i.e storage) must override this method
        :return:
        """
        raise NotImplementedError

    def get_state(self,
                  chat: typing.Union[int, str, None] = None,
                  user: typing.Union[int, str, None] = None,
                  default: typing.Optional[str] = None) -> typing.Union[str]:
        """
        Every subclass(i.e storage) must override this method
        :param chat:
        :param user:
        :param default:
        :return:
        """

        raise NotImplementedError

    def get_data(self,
                 chat: typing.Union[int, str, None] = None,
                 user: typing.Union[int, str, None] = None,
                 default: typing.Optional[str] = None) -> typing.Dict:
        """
        Every subclass(i.e storage) must override this method
        :param chat:
        :param user:
        :param default:
        :return:
        """

        raise NotImplementedError

    def set_state(self,
                  chat: typing.Union[int, str, None] = None,
                  user: typing.Union[int, str, None] = None,
                  state: typing.Optional[typing.AnyStr] = None):
        """
        Every subclass(i.e storage) must override this method
        :param chat:
        :param user:
        :param state:
        :return:
        """

        raise NotImplementedError

    def set_data(self,
                 chat: typing.Union[int, str, None] = None,
                 user: typing.Union[int, str, None] = None,
                 data: typing.Dict = None):
        """
        Every subclass(i.e storage) must override this method
        :param chat:
        :param user:
        :param data:
        :return:
        """

        raise NotImplementedError

    def update_data(self,
                    chat: typing.Union[int, str, None] = None,
                    user: typing.Union[int, str, None] = None,
                    data: typing.Dict = None):
        """
        Every subclass(i.e storage) must override this method
        :param chat:
        :param user:
        :param data:
        :return:
        """

        raise NotImplementedError

    def reset_data(self,
                   chat: typing.Union[int, str, None] = None,
                   user: typing.Union[int, str, None] = None):
        """
        Every subclass(i.e storage) must override this method
        :param chat:
        :param user:
        :return:
        """

        self.set_data(chat, user, data={})

    def reset_state(self,
                    chat: typing.Union[int, str, None] = None,
                    user: typing.Union[int, str, None] = None,
                    with_data: typing.Optional[bool] = True):
        """
        Reset state for user in chat
        :param chat: Chat id
        :param user: User id
        :param with_data: Optional. If true, resets user data
        :return:
        """

        self.set_state(chat, user, state=None)
        if with_data:
            self.reset_data(chat, user)

    def finish(self,
               chat: typing.Union[int, str, None] = None,
               user: typing.Union[int, str, None] = None):
        """
        Fully resets state and data for user in chat
        :param chat: Chat id
        :param user: User id
        :return:
        """
        self.reset_state(chat, user, with_data=True)


class DisabledStorage(BaseStorage):
    """
    Use that storage when you don't need to store any state.
    """
    def close(self):
        pass

    def get_state(self,
                  chat: typing.Union[int, str, None] = None,
                  user: typing.Union[int, str, None] = None,
                  default: typing.Optional[str] = None) -> typing.Union[str]:
        return '' or default

    def get_data(self,
                 chat: typing.Union[int, str, None] = None,
                 user: typing.Union[int, str, None] = None,
                 default: typing.Optional[str] = None) -> typing.Dict:
        return {} or default

    def set_state(self,
                  chat: typing.Union[int, str, None] = None,
                  user: typing.Union[int, str, None] = None,
                  state: typing.Optional[typing.AnyStr] = None):
        pass

    def set_data(self,
                 chat: typing.Union[int, str, None] = None,
                 user: typing.Union[int, str, None] = None,
                 data: typing.Dict = None):
        pass

    def update_data(self,
                    chat: typing.Union[int, str, None] = None,
                    user: typing.Union[int, str, None] = None,
                    data: typing.Dict = None):
        pass
