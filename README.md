1. Problem Statement (Brief)

Monitor a log file on the server in real-time.

Show the last 10 lines when a client opens the page.

Stream new lines as they appear without refreshing.

Handle large files efficiently.

Support multiple clients.

Minimize CPU and disk usage.

2. Approaches Overview

Approach 1: Brute Force – read entire file each time.

Approach 2: Polling per Client – read only new lines, client-side polling.

Approach 3: SSE with Server-Side Polling – server reads once, pushes to all clients.

Approach 4: Optimized Event-Driven SSE – OS-level file watcher triggers updates.

3. Approach Comparison Table
Approach	How it Works	Pros	Cons	Example
Brute Force	Read entire file each time	Simple	Slow for large files, not scalable	2GB file → high CPU & disk usage
Polling per Client	Each client tracks last position and polls for new lines	Only reads new lines	CPU grows with clients, small latency	5 clients → 5 reads every 0.5s
SSE + Server Polling	Server reads once, pushes to all clients via SSE	Single read for all clients	Still polling → small latency	All clients see updates within polling interval
Event-Driven SSE	OS watcher triggers updates pushed to clients	Real-time, low CPU, scalable, handles log rotation	More complex setup	100 clients receive instant updates from 2GB log
4. Key Concepts / Fundamentals

SSE (Server-Sent Events): Pushes updates from server → client over HTTP.

Polling: Client or server periodically checks for updates.

File Position Tracking: Keeps last read byte to read only new lines.

OS File Watcher: Event-driven mechanism (e.g., inotify / Watchdog) triggers on file change.

Async Queues: Each client has a queue to receive updates independently.

Scalability: Reduce redundant reads and CPU usage for multiple clients.

5. Repository Structure
repo/
├─ README.md                   # This file
├─ log_viewer_all_approaches.md  # Pseudo-code + explanations for all 4 approaches
└─ log_viewer_implementations.py # Actual working code for all 4 approaches

6. Tips for Revision

Focus on Approach Evolution: Brute Force → Polling → SSE → Event-Driven.

Remember Tradeoffs: Understand why each approach is better/worse in terms of CPU, latency, and scalability.

Visualize Data Flow: Especially for Approach 4:

File → Watcher → Server Queue → Client SSE

Key Interview Points:

Explain initial 10 lines logic.

Explain how new lines are streamed.

Discuss handling multiple clients.

Mention log rotation handling for large files.

Use Table + Examples: They stick better than long paragraphs.

7. Optional Diagram (for quick recall)
+------------------+
|   Log File       |
+------------------+
          |
          v
+------------------+     File change event triggers
|  File Watcher    |----------------+
+------------------+                |
          |                         |
          v                         |
+------------------+                |
|  Server Queues   | --------------+
+------------------+
          |
          v
+------------------+
|  Clients (SSE)   |
+------------------+
