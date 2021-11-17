from aiohttp import web

from containers import ApplicationContainer


def create_app():
    container = ApplicationContainer()

    app = container.app()
    app.container = container

    app.add_routes([
        web.get('/convert/', container.convert_view.as_view()),
        web.post('/database/', container.database_view.as_view()),
    ])

    return app
