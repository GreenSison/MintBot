import asyncio

from aiohttp import web


async def healthz(request: web.Request) -> web.Response:
    payload: dict = {"status": "ok"}
    provider = request.app.get("discord_status")
    if provider is not None:
        try:
            payload.update(provider())
        except Exception as e:
            payload["discord_error"] = str(e)
    return web.json_response(payload)


async def index(request: web.Request) -> web.Response:
    return web.Response(text="Bot is alive!")


def create_app(discord_status=None) -> web.Application:
    app = web.Application()
    if discord_status is not None:
        app["discord_status"] = discord_status
    app.router.add_get("/", index)
    app.router.add_get("/healthz", healthz)
    app.router.add_get("/ping", healthz)
    return app


async def start(port: int, discord_status=None):
    app = create_app(discord_status)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Keep-alive server listening on port {port}")
    # Keep the coroutine alive; cleanup happens on process exit
    while True:
        await asyncio.sleep(3600)
