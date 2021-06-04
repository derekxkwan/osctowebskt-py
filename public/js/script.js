let skt = new WebSocket("ws://127.0.0.1:8080/ws");

function parseMsg(msg) {
    let ret = {};
    let pmsg = msg.split(" ");
    let addr = pmsg[0];
    let clen = pmsg.length;
    let cvals = pmsg.slice(1,clen);
    let args = cvals.map(x => parseFloat(x));
    ret["addr"] = addr;
    ret["args"] = args;
    return ret;
}

skt.addEventListener('open', (evt) => {console.log("ws open");});

skt.addEventListener('message', (evt) => {
    let msg = evt.data;
    let p = parseMsg(msg);
    console.log(p);
});

