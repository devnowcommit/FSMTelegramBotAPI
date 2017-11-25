# FSMTelegramBotAPI
A finite-state machine wrapper for [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

[![Travis](https://img.shields.io/travis/Ars2014/FSMTelegramBotAPI.svg?style=flat-square)](https://travis-ci.org/Ars2014/FSMTelegramBotAPI) [![PyPI](https://img.shields.io/pypi/v/FSMTelegramBotAPI.svg?style=flat-square)](https://pypi.python.org/pypi/FSMTelegramBotAPI)
## Install
1. From PyPI using `pip`:
    ```
    $ pip install -U FSMTelegramBotAPI
    ```
2. From Github using `git`:
    ```
    $ git clone http://github.com/Ars2014/FSMTelegramBotAPI.git
    $ cd FSMTelegramBotAPI
    $ python setup.py install
    ```

## Instructions
All instructions you can find at [original pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI). There are only additions and differences.

### Storages
To store states and data you can use module `fsm_telebot.storage`:
```python
from fsm_telebot.storage.base import BaseStorage # Abstract class
from fsm_telebot.storage.base import DisabledStorage # Use it, if you don't want to store anything
from fsm_telebot.storage.memory import MemoryStorage # In-memory storage
from fsm_telebot.storage.rethinkdb import RethinkDBStorage # RethinkDB based storage
```
Every storage must be a subclass of BaseStorage and implement methods: `set_state`, `set_data`, `get_state`, `get_data`,  `update_data`, `finish` and `close`:
```python
from fsm_telebot.storage.memory import MemoryStorage # you can use any storage

storage = MemoryStorage()

storage.set_state(1, state='Test') 
storage.set_data(1, data={2: 3})

storage.get_state(1) # -> 'Test'
storage.get_data(1) # -> {2: 3}

storage.update_data(1, data={4: 5})
storage.get_data(1) # -> {2: 3, 4: 5}

storage.reset_state(1)
storage.get_state(1) # ->  None
storage.reset_data(1)
storage.get_data(1) # -> {}

storage.finish(1) # Same as reset_state with reset_data
storage.get_state(1) # ->  None
storage.get_data(1) # -> {}

storage.get_data(1) # -> {}

storage.close() # -> closes or clears storage.
```

### Telebot class
Telebot class got 8 new methods: `set_state`, `set_data`, `get_state`, `get_data`, `reset_state`, `reset_data`, `update_data`, `finish_user`:
```python
from fsm_telebot.storage.memory import MemoryStorage
import fsm_telebot

storage = MemoryStorage()
bot = fsm_telebot.Telebot('TOKEN', storage=storage)

bot.set_state(1, state='Test') # storage.set_state
bot.set_data(1, data={2: 3}) # storage.set_data

bot.get_state(1) # storage.get_state
bot.get_data(1) # storage.get_data

bot.update_data(1, data={4: 5}) # storage.update_data
bot.get_data(1) 

bot.reset_state(1) # storage.reset_state
bot.get_state(1) 
bot.reset_data(1) # storage.reset_data
bot.get_data(1) 

bot.finish_user(1) # storage.finish
bot.get_state(1) 
bot.get_data(1) 
```

### Message handlers
All handlers (i.e message, callback, etc.) have new optional parameter `state`, which checks if user got this state.
Here an example: 
```python
import fsm_telebot
from fsm_telebot.storage.memory import MemoryStorage

storage = MemoryStorage()
bot = fsm_telebot.Telebot('TOKEN', storage=storage)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.set_state('Test', msg.chat.id)
    bot.send_message('Your state is now "Test"', msg.chat.id)

@bot.message_handler(state='Test')
def test(msg):
    bot.send_message('Your state is still "Test"', msg.chat.id)
```


## Bot using this framework
Contact [@Ars2013](https://t.me/Ars2013) to add your bot here.