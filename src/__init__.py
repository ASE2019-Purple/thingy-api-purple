# from logging import getLogger, basicConfig, INFO
# from os import getenv
# from aiohttp import web
# import aiohttp_cors
# from aiohttp_swagger import setup_swagger

# from .views import (
#     IndexView,
#     TodoIndexView,
#     TodoView,
#     TagIndexView,
#     TagView,
#     TodoTagView,
#     TodoTagIndexView,
#     TagTodoIndexView,
#     TagTodoView,
# )

# from .models import db, Task, Tag, TaskXTag

# IP = getenv("IP", "0.0.0.0")
# IP = getenv("IP", "localhost")
# PORT = getenv("PORT", "8000")

# basicConfig(level=INFO)
# logger = getLogger(__name__)


# async def init(loop):

#     # Connect to Database
#     # localhost/gino

#     # Postgres instance on AWS
#     await db.set_bind("postgresql://postgres:cloudcomputing19@3.124.5.127:5432/gino")

#     # Local postgresql
#     # await db.set_bind("postgresql://localhost/gino")

#     # Create tables
#     await db.gino.create_all()

#     app = web.Application(loop=loop)

#     # Configure default CORS settings.
#     cors = aiohttp_cors.setup(
#         app,
#         defaults={
#             "http://localhost": aiohttp_cors.ResourceOptions(
#                 allow_credentials=True, expose_headers="*", allow_headers="*"
#             ),
#             "http://127.0.0.0": aiohttp_cors.ResourceOptions(
#                 allow_credentials=True, expose_headers="*", allow_headers="*"
#             ),
#         },
#     )

#     # Todos
#     cors.add(
#         app.router.add_route(
#             "*", "/todos/{task_id}/tags/{tag_id}", TodoTagView, name="todo_tag"
#         ),
#         webview=True,
#     )
#     cors.add(
#         app.router.add_route(
#             "*", "/todos/{id}/tags/", TodoTagIndexView, name="todo_tags"
#         ),
#         webview=True,
#     )
#     cors.add(
#         app.router.add_route("*", "/todos/", TodoIndexView, name="todos"), webview=True
#     )
#     cors.add(
#         app.router.add_route("*", "/todos/{id}", TodoView, name="todo"), webview=True
#     )

#     # Tags
#     cors.add(
#         app.router.add_route("*", "/tags/{tag_id}/todos/{task_id}", TagTodoView),
#         webview=True,
#     )
#     cors.add(
#         app.router.add_route("*", "/tags/{id}/todos/", TagTodoIndexView), webview=True
#     )
#     cors.add(
#         app.router.add_route("*", "/tags/", TagIndexView, name="tags"), webview=True
#     )

#     cors.add(app.router.add_route("*", "/tags/{id}", TagView, name="tag"), webview=True)

#     # Routes
#     cors.add(app.router.add_route("get", "/{tail:.*}", IndexView), webview=True)

#     # Config
#     setup_swagger(app, swagger_url="/api/v1/doc", swagger_from_file="swagger.yaml")
#     logger.info("Starting server at %s:%s", IP, PORT)
#     srv = await loop.create_server(app.make_handler(), IP, PORT)
#     return srv
