from contextlib import asynccontextmanager
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <h2>Your ID: <span id="ws-id"></span></h2>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var client_id = Date.now()
#             document.querySelector("#ws-id").textContent = client_id;
#             var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """

html = """
<!DOCTYPE html>
    <html>
   <head>
    <title>Currency Observer</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
    <body>
        <h1>Currency Observer</h1>
        <div id="client-id"></div>
        <input type="text" id="charcode-input" placeholder="Enter stock charcode">
        <button id="send-charcode">Send</button>
        <table id="currency-table">
        <thead>
            <tr>
                <th>Charcode</th>
                <th>Name</th>
                <th>Value</th>
            </tr>
            </thead>
                <tbody>
            </tbody>
        </table>
        <script>
        const clientId = Math.floor(Date.now() / 1000);
        document.getElementById("client-id").innerText = `Client ID: ${clientId}`;

        const ws = new WebSocket(`ws://${location.host}/ws/${clientId}`);

        
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            const a = JSON.parse(data);
            console.log("Currency data updated:", a);
            const tbody = document.getElementById("currency-table").getElementsByTagName("tbody")[0];
            tbody.innerHTML = "";  // Очистить таблицу перед обновлением
            console.log(a);
            for (const [code, currency] of Object.entries(a)) {
                for (const [charcode, details] of Object.entries(currency)) {
                    const row = tbody.insertRow();
                    row.insertCell(0).innerText = charcode;
                    row.insertCell(1).innerText = details[0];
                    row.insertCell(2).innerText = details[1][0] + "." + details[1][1];
                }
            }
        };
        document.getElementById("send-charcode").onclick = function() {
            const charcode = document.getElementById("charcode-input").value;
            const tbody = document.getElementById("currency-table").getElementsByTagName("tbody")[0];
            tbody.innerHTML = "";
            ws.send(charcode);
        };
    </script>
    </body>
</html>"""



import requests
import asyncio
import sys
sys.path.append('..')
from Observer import Client, CurrenciesManager


subject = CurrenciesManager(time_rate=10)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(upload_period(subject))
    yield
    task.cancel()
    await task

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    # print("ws create")
    observer = Client(int(client_id), websocket)
    subject.attach(observer)
    try:
        while True:
            # await fetch_currency_rates(subject)
            message = await websocket.receive_text()
            observer.charcodes = message.split(' ')
            observer.curr_dict.clear()
            await fetch_currency_rates(subject)
            
            
    except WebSocketDisconnect:
        subject.detach(observer)


async def fetch_currency_rates(subject):
        await subject.update_currencies()
        
async def upload_period(subject):
    while True:
        await subject.update_currencies()
        await asyncio.sleep(subject.time_rate)
        


