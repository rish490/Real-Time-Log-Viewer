# Real-Time Log Viewer

A scalable real-time log monitoring system designed to explore different backend architectures for streaming live log updates efficiently to multiple clients.

The project focuses on backend scalability, real-time communication, efficient file processing, event-driven systems, and low-latency streaming techniques commonly used in production monitoring systems.

---

## Problem Statement

Build a system to monitor a server log file in real time with the following requirements:

- Show the latest 10 log lines when a client connects
- Stream new log updates without page refresh
- Efficiently handle very large log files
- Support multiple concurrent clients
- Minimize CPU and disk usage
- Handle log rotation gracefully

---

## Approaches Explored

### 1. Brute Force Approach
Reads the entire file repeatedly for every request.

#### Pros
- Simple implementation

#### Cons
- High CPU and disk usage
- Extremely inefficient for large files
- Poor scalability

Example:
A 2GB log file causes heavy repeated reads and high resource consumption.

---

### 2. Polling Per Client
Each client tracks file position and periodically polls for new updates.

#### Pros
- Reads only newly appended lines
- Better than brute force

#### Cons
- CPU usage increases linearly with number of clients
- Polling introduces latency
- Redundant reads for multiple clients

Example:
5 clients polling every 0.5 seconds results in 5 repeated reads.

---

### 3. SSE with Server-Side Polling
Server polls the file once and pushes updates to all connected clients using Server-Sent Events (SSE).

#### Pros
- Single read shared across all clients
- Lower CPU usage
- Better scalability

#### Cons
- Still depends on polling interval
- Small latency remains

Example:
All clients receive updates simultaneously within polling interval.

---

### 4. Event-Driven SSE (Optimized)
Uses OS-level file watchers to trigger updates only when the log file changes.

#### Pros
- Real-time streaming
- Minimal CPU usage
- Efficient for large files
- Highly scalable
- Supports multiple clients efficiently

#### Cons
- More complex implementation

Example:
100 clients receive instant updates from a 2GB log file with minimal resource usage.

---

## Architecture Evolution

The project progressively evolves through increasingly scalable approaches:

Brute Force → Polling → SSE → Event-Driven Streaming

Each iteration improves:
- scalability
- latency
- concurrent client handling
- resource utilization

---

## Key Concepts

### Server-Sent Events (SSE)
Streams real-time updates from server → client over HTTP.

### File Position Tracking
Tracks last read byte position to avoid re-reading entire files.

### Polling
Periodically checks file for updates.

### OS File Watchers
Uses event-driven mechanisms (e.g. inotify / watchdog) to detect file changes.

### Async Queues
Maintains independent queues for connected clients.

### Scalability
Reduces redundant reads and minimizes CPU usage for concurrent clients.

---

## Production Considerations

The project explores several real-world backend engineering concerns:

- concurrent client management
- efficient file reading
- event-driven architectures
- low-latency streaming
- scalability under high load
- log rotation handling
- resource optimization

---

## Repository Structure

```text
repo/
├─ README.md
├─ log_viewer_all_approaches.md
└─ log_viewer_implementations.py
