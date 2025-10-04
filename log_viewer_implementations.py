"""
Real-Time Log Viewer – All 4 Approaches
Approaches:
1. Brute Force
2. Polling per Client
3. SSE with Server-Side Polling
4. Optimized Event-Driven SSE
"""

import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_FILE = "log.txt"

app = FastAPI()

# -----------------------------
# Helper function to read last N lines
# -----------------------------
def read_last_n_lines(file_path, N=10):
    with open(file_path, "rb") as f:
        f.seek(0, 2)
        file_size = f.tell()
        block_size = 1024
        data = b""
        while len(data.splitlines()) <= N and file_size > 0:
            seek_size = min(block_size, file_size)
            file_size -= seek_size
            f.seek(file_size)
            data = f.read(seek_size) + data
        return b"\n".join(data.splitlines()[-N:]).decode("utf-8")

# -----------------------------
# Approach 1: Brute Force
# -----------------------------
@app.get("/approach1")
async def brute_force():
    """
    Every time client requests, read entire file and send last 10 lines
    """
    while True:
        lines = read_last_n_lines(LOG_FILE)
        yield f"data: {lines}\n\n"
        await asyncio.sleep(1)  # polling interval

# -----------------------------
# Approach 2: Polling per Client
# -----------------------------
@app.get("/approach2")
async def polling_per_client():
    """
    Track last position per client, read only new lines
    """
    last_pos = 0

    async def event_gen():
        nonlocal last_pos
        # Send initial last 10 lines
        yield f"data: {read_last_n_lines(LOG_FILE)}\n\n"

        while True:
            with open(LOG_FILE, "r") as f:
                f.seek(last_pos)
                new_lines = f.read()
                if new_lines:
                    yield f"data: {new_lines.strip()}\n\n"
                    last_pos = f.tell()
            await asyncio.sleep(0.5)  # polling interval

    return StreamingResponse(event_gen(), media_type="text/event-stream")

# -----------------------------
# Approach 3: SSE with Server-Side Polling
# -----------------------------
clients_3 = []
last_pos_3 = 0

@app.get("/approach3")
async def sse_server_polling():
    """
    Server reads once, pushes to all clients via SSE
    """
    queue = asyncio.Queue()
    clients_3.append(queue)

    async def event_gen():
        global last_pos_3
        # Send last 10 lines initially
        yield f"data: {read_last_n_lines(LOG_FILE)}\n\n"
        try:
            while True:
                # Polling server side
                with open(LOG_FILE, "r") as f:
                    f.seek(last_pos_3)
                    new_lines = f.read()
                    if new_lines:
                        last_pos_3 = f.tell()
                        for q in clients_3:
                            q.put_nowait(new_lines.strip())
                line = await queue.get()
                yield f"data: {line}\n\n"
                await asyncio.sleep(0.1)  # optional small sleep
        except asyncio.CancelledError:
            clients_3.remove(queue)
            raise

    return StreamingResponse(event_gen(), media_type="text/event-stream")

# -----------------------------
# Approach 4: Optimized Event-Driven SSE
# -----------------------------
clients_4 = []

class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                last_line = f.readlines()[-1].strip()
            for queue in clients_4:
                queue.put_nowait(last_line)

observer = Observer()
observer.schedule(LogHandler(), ".", recursive=False)
observer.start()

@app.get("/approach4")
async def optimized_sse():
    """
    OS-level watcher triggers push to all clients
    """
    queue = asyncio.Queue()
    clients_4.append(queue)

    async def event_gen():
        # Send last 10 lines initially
        yield f"data: {read_last_n_lines(LOG_FILE)}\n\n"

        try:
            while True:
                line = await queue.get()
                yield f"data: {line}\n\n"
        except asyncio.CancelledError:
            clients_4.remove(queue)
            raise

    return StreamingResponse(event_gen(), media_type="text/event-stream")
