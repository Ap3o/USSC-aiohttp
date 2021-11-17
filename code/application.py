from aiohttp import web
from aiohttp.web import run_app

from containers import ApplicationContainer


def create_app() -> web.Application:
    container = ApplicationContainer()

    app = container.app()
    app.container = container

    app.add_routes([
        web.get('/convert/', container.convert_view.as_view()),
        web.post('/database/', container.database_view.as_view()),
    ])

    return app


if __name__ == "__main__":
    run_app(create_app(), port=8000)
