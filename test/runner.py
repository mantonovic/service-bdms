import asyncio
import asyncpg

"""
Usage example:
==============
ipython
%load_ext autoreload
%autoreload 2

from test import runner
from bms.v1.borehole import ListBorehole
runner.execute(ListBorehole)
"""

ioloop = asyncio.get_event_loop()
ioloop.set_debug(enabled=True)

def execute(action, request={}):
    try:
        a = action(
            ioloop.run_until_complete(
                asyncpg.create_pool(
                    user='postgres', password='postgres',
                    database='bms', host='localhost'
                )
            )
        )
        return ioloop.run_until_complete(a.execute(**request))
    finally:
        ioloop.close()