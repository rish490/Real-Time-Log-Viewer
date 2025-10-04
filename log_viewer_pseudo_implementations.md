# Real-Time Log Viewer – Pseudo Implementations of 4 Approaches

---

## Approach 1: Brute Force – Read Entire File

# Idea: Every client reads the entire file each time

[Client] <--requests-- [Server] <--reads entire-- [Log File]

function get_last_n_lines(file, N):
    lines = read_all_lines(file)
    return last N lines

function serve_client():
    while client_connected:
        lines = get_last_n_lines(LOG_FILE, 10)
        send_to_client(lines)
        wait(some_interval)

# Pros: Simple
# Cons: Slow for large files, high CPU & disk usage, not scalable

---

## Approach 2: Polling per Client – Incremental Read

[Client 1] <-polls-> [Server] <-reads new lines-> [Log File]
[Client 2] <-polls-> [Server] <-reads new lines-> [Log File]

# Idea: Track last read position per client, poll for new lines
function serve_client():
    last_pos = 0
    send_to_client(read_last_10_lines(LOG_FILE))
    while client_connected:
        open LOG_FILE
        move_to(last_pos)
        new_lines = read_new_lines()
        if new_lines:
            send_to_client(new_lines)
            last_pos = current_position
        wait(0.5 seconds)

# Pros: Only new lines read, reduced disk usage
# Cons: Each client polls independently, CPU grows with clients, small latency

---

## Approach 3: SSE with Server-Side Polling

[Log File] --poll--> [Server] --broadcast--> [Client 1]
                               \
                                --> [Client 2]
                               \
                                --> [Client N]
                                
# Idea: Server reads new lines once, broadcasts to all clients via SSE

global last_pos = 0
clients = []

function watch_file():
    while True:
        open LOG_FILE
        move_to(last_pos)
        new_lines = read_new_lines()
        if new_lines:
            last_pos = current_position
            for client in clients:
                client.queue.push(new_lines)
        wait(0.5 seconds)

function serve_client(client):
    send_to_client(read_last_10_lines(LOG_FILE))
    add client.queue to clients
    while client_connected:
        line = client.queue.pop()
        send_to_client(line)

# Pros: Single read per update, clients auto-update
# Cons: Still polling → small latency, moderate CPU usage

---

## Approach 4: Optimized Event-Driven SSE

       [Log File]
            |
       (OS Watcher triggers)
            |
        [Server Queues]
        /       |       \
   [Client 1] [Client 2] [Client N]


# Idea: Use OS-level file watcher to push updates instantly
clients = []

function on_file_change():
    new_line = read_last_line(LOG_FILE)
    for client in clients:
        client.queue.push(new_line)

function serve_client(client):
    client.queue = new_queue()
    clients.append(client.queue)
    send_to_client(last_10_lines(LOG_FILE))
    while client_connected:
        line = client.queue.pop()  # waits until new line arrives
        send_to_client(line)

watch(LOG_FILE, on_change=on_file_change)  # OS-level file watcher

# Pros: Real-time, low CPU, scalable, handles log rotation
# Cons: Slightly more complex setup
