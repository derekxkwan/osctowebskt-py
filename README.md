# osctowebskt-py

- Forward osc (on port 3333 in this instance) to a locally hosted website via WebSockets (hosted on port 8080 in this instance)! All web files go in the `public/` folder and run `python main.py` to start the bridge/server.
- Uses Python 3's [python-osc](https://github.com/attwad/python-osc) and [aiohttp](https://github.com/aio-libs/aiohttp).
- Work-in-progress as I'm new to async programming in Python. Example files are already in the `public/` folder and an example Pure Data patch called `osccontrol.pd` is included to test things out. Only OSC -> webpage for now but the reverse direction shouldn't be too difficult to manage.

## Usage Notes
- Needs Python 3
- run the `main.py` file (so `python main.py` or `python3 main.py` if python3 isn't symlinked to python)
- the OSC server runs on `0.0.0.0` at port `3333` (ran into issues trying to receive messages from another computer using `127.0.0.1` for some reason)
