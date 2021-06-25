# osctowebskt-py

- Forward osc (on port 3333 in this instance) to a locally hosted website via WebSockets (hosted on port 8080 in this instance)! All web files go in the `public/` folder and run `python main.py` to start the bridge/server.
- Uses Python 3's [python-osc](https://github.com/attwad/python-osc) and [aiohttp](https://github.com/aio-libs/aiohttp).
- Work-in-progress as I'm new to async programming in Python. Example files are already in the `public/` folder and an example Pure Data patch called `osccontrol.pd` is included to test things out. Only OSC -> webpage for now but the reverse direction shouldn't be too difficult to manage.

## Usage Notes
- Needs Python 3
- run the `main.py` file (so `python main.py` or `python3 main.py` if python3 isn't symlinked to python)
- the OSC server runs on `0.0.0.0` at port `3333` (ran into issues trying to receive messages from another computer using `127.0.0.1` for some reason)
- incoming OSC messages are automatically cached and printed by the script every 0.25 seconds (so if incoming messages are being received, it'll get printed, this value is stored in `PRINT_DUR`)
- `control + c` kills the server when in the same terminal pane as the script you executed the previous command (as usual). Sometimes I've been unable to kill the server using this method and had to do `ps aux | grep python` to find the PID to kill the server using `kill -9 (insert PID here)` but I haven't quite figured that out yet.
