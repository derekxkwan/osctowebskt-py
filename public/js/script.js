let skt = new WebSocket("ws://127.0.0.1:8080/ws");
let disp = document.getElementById("disp");

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

function format_str(cur) {
    let addr = cur["addr"];
    let args = cur["args"];
    return `Address: ${addr}, Args: ${args}`;
}

skt.addEventListener('open', (evt) => {console.log("ws open");});

skt.addEventListener('message', (evt) => {
    let msg = evt.data;
    let p = parseMsg(msg);
    let cur = format_str(p);
    let curtext = disp.innerHTML;
    curtext += (cur + "<br>");
    disp.innerHTML = curtext;
});

