import asyncio

from aiohttp import web


async def healthz(request: web.Request) -> web.Response:
    return web.json_response({"status": "ok"})


async def index(request: web.Request) -> web.Response:
    return web.Response(text="Bot is alive!")


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", index)
    app.router.add_get("/healthz", healthz)
    app.router.add_get("/ping", healthz)
    return app


async def start(port: int):
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Keep-alive server listening on port {port}")
    # Keep the coroutine alive; cleanup happens on process exit
    while True:
        await asyncio.sleep(3600)
