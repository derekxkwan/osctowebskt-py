# osctowebskt-py

Forward osc (on port 33333 in this instance) to a locally hosted website via WebSockets (hosted on port 8080 in this instance)! All web files go in the `public/` folder and run `python main.py` to start the bridge/server.

Uses Python 3's [python-osc](https://github.com/attwad/python-osc) and [aiohttp](https://github.com/aio-libs/aiohttp).

Work-in-progress as I'm new to async programming in Python. Example files are already in the `public/` folder and an example Pure Data patch called `osccontrol.pd` is included to test things out. Only OSC -> webpage for now but the reverse direction shouldn't be too difficult to manage.
