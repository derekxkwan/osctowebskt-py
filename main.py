from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from aiohttp import web
import asyncio
import os
import signal
import functools
from sys import exit

script_path = os.path.abspath(os.path.dirname(__file__))
index_path = os.path.join(script_path, 'public', 'index.html')
public_path = os.path.join(script_path, 'public')

oscip = "0.0.0.0"
oscp = 3333
PRINT_DUR = 0.25
WS_DUR = 0
webhost = os.getenv("HOST", "127.0.0.1")
webport = int(os.getenv("PORT", 8080))
ws = None
to_send = None
to_print = None

async def add_to_print(cur):
    global to_print
    await to_print.put(cur)

async def add_to_send(cur):
    global to_send
    await to_send.put(cur)

def hard_exit(signame, loop):
    loop.stop()
    exit(0)

def osc_to_ws(addr, *args):
    loop = asyncio.get_event_loop()
    loop.create_task(add_to_print(f"{addr}: {args}"))
    if ws != None:
        #print(f"{addr}: {args}")
        retstr = addr
        for x in args:
            retstr += f" {x}"
        loop.create_task(add_to_send(retstr))
    else:
        loop.create_task(add_to_print("no ws"))

dispatcher = Dispatcher()
dispatcher.map("/*", osc_to_ws)


async def ws_handler(req):
    global ws
    global to_send
    ws = web.WebSocketResponse()
    await ws.prepare(req)
    while True:
        cur = await to_send.get()
        await ws.send_str(cur)
        await asyncio.sleep(WS_DUR)

async def send_loop():
    global ws
    global to_print
    while True:
        while not to_print.empty():
            cur = await to_print.get()
            print(cur)
        await asyncio.sleep(PRINT_DUR)

async def root_router(req):
    return web.FileResponse(index_path)

async def web_server():
    app = web.Application()
    app.add_routes([web.get('/ws', ws_handler), web.get('/', root_router), web.static('/', public_path)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, webhost, webport)
    await site.start()
    while True:
        await asyncio.sleep(3600)

async def osc_server(loop):
    server = AsyncIOOSCUDPServer((oscip, oscp), dispatcher, loop)
    tport, protocol = await server.create_serve_endpoint()
    await send_loop()
    tport.close()

async def main():
    global to_send
    global to_print
    to_send = asyncio.Queue()
    to_print = asyncio.Queue()
    loop = asyncio.get_event_loop()
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(hard_exit, signame, loop))
    await asyncio.gather(osc_server(loop), web_server())

asyncio.run(main())
