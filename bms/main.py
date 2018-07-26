# -*- coding: utf-8 -*-
from tornado import web
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio
import asyncpg
from tornado.httpserver import HTTPServer
import sys

sys.path.append('.')


async def get_conn():
    return await asyncpg.create_pool(
        user='postgres', password='postgres',
        database='bms', host='localhost')

if __name__ == "__main__":

    from bms import (
        BoreholeHandler,
        StratigraphyHandler,
        LayerHandler,
        ProjectHandler,
        CodeListHandler,
        MunicipalityHandler,
        CantonHandler
    )

    AsyncIOMainLoop().install()
    ioloop = asyncio.get_event_loop()
    ioloop.set_debug(enabled=True)

    settings = dict(
        debug=True
    )

    application = web.Application([
        (r'/api/v1/borehole', BoreholeHandler),
        (r'/api/v1/borehole/stratigraphy', StratigraphyHandler),
        (r'/api/v1/borehole/stratigraphy/layer', LayerHandler),
        (r'/api/v1/borehole/project', ProjectHandler),
        (r'/api/v1/borehole/codes', CodeListHandler),
        (r'/api/v1/geoapi/municipality', MunicipalityHandler),
        (r'/api/v1/geoapi/canton', CantonHandler)
    ], **settings)

    application.pool = ioloop.run_until_complete(get_conn())

    http_server = HTTPServer(application)
    http_server.listen(8888, 'localhost')
    ioloop.run_forever()
