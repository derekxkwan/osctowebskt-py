from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from aiohttp import web
import asyncio
import os
from signal import signal, SIGINT
from sys import exit

oscip = "127.0.0.1"
oscp = 33333
webhost = os.getenv("HOST", "127.0.0.1")
webport = int(os.getenv("PORT", 8080))
ws = None
to_send = []
running = True

def sigint_handler(recv, frame):
    global running
    running = False

def osc_to_ws(addr, *args):
    global ws
    global to_send
    if ws != None:
        #print(f"{addr}: {args}")
        retstr = addr
        for x in args:
            retstr += f" {x}"
        to_send.append(retstr)
    else:
        print("no ws connection")

dispatcher = Dispatcher()
dispatcher.map("/*", osc_to_ws)


async def ws_handler(req):
    global ws
    ws = web.WebSocketResponse()
    await ws.prepare(req)
    while True:
        await asyncio.sleep(3600)
    return ws

async def loop():
    global ws
    global to_send
    global running
    while running==True:
        while len(to_send) > 0:
            cur = to_send.pop()
            await ws.send_str(cur)
        await asyncio.sleep(0)

async def web_server():
    app = web.Application()
    app.add_routes([web.get('/ws', ws_handler), web.static('/', './public/')])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, webhost, webport)
    await site.start()
    while True:
        await asyncio.sleep(3600)

async def init_main():
    server = AsyncIOOSCUDPServer((oscip, oscp), dispatcher, asyncio.get_event_loop())
    tport, protocol = await server.create_serve_endpoint()
    await loop()
    tport.close()
    exit(0)

signal(SIGINT, sigint_handler)
asyncio.ensure_future(web_server())
asyncio.ensure_future(init_main())
mloop = asyncio.get_event_loop()
mloop.run_forever()
