from dependency_injector import containers
from dependency_injector.ext import aiohttp
from aiohttp import web

import views


class ApplicationContainer(containers.DeclarativeContainer):

    app = aiohttp.Application(web.Application)

    convert_view = aiohttp.View(views.convert)
    database_view = aiohttp.View(views.database)
