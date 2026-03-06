# TCP — Transmission Control Protocol

## What is TCP?
**Transmission Control Protocol** — a connection-oriented, reliable transport-layer protocol (Layer 4). It guarantees delivery, ordering, and error checking of data between applications.

## What are the key characteristics of TCP?
- **Connection-oriented**: Establishes a connection before data transfer (3-way handshake)
- **Reliable**: Guarantees delivery via acknowledgments and retransmission
- **Ordered**: Data arrives in the correct sequence (sequence numbers)
- **Flow control**: Sliding window prevents sender from overwhelming receiver
- **Congestion control**: Reduces transmission rate during network congestion
- **Full-duplex**: Both sides can send and receive simultaneously

## What is the TCP 3-way handshake?
The process to establish a TCP connection:
1. **SYN**: Client sends a segment with SYN flag set (chooses initial sequence number)
2. **SYN-ACK**: Server responds with SYN and ACK flags set
3. **ACK**: Client sends ACK to complete the connection

## What is the TCP 4-way teardown?
The process to close a TCP connection:
1. **FIN**: Initiating side sends FIN (I'm done sending)
2. **ACK**: Other side acknowledges
3. **FIN**: Other side sends its own FIN
4. **ACK**: Initiating side acknowledges
(Can be combined into 3 steps if both FIN+ACK are sent together)

## What are TCP sequence and acknowledgment numbers?
- **Sequence number**: The byte offset of the first byte in this segment
- **Acknowledgment number**: The next byte the receiver expects to receive (implying all prior bytes received successfully)

## What is TCP sliding window?
A flow control mechanism where the **receiver advertises a window size** (how many bytes it can buffer). The sender can transmit up to the window size of data before waiting for acknowledgments. This allows multiple unacknowledged segments to be "in flight" simultaneously.

## What is the TCP TIME_WAIT state?
After a connection is fully closed, the initiating side stays in TIME_WAIT for **2 × MSL** (Maximum Segment Lifetime, typically 60 seconds = 120s total). This ensures any delayed packets from the connection are discarded before a new connection with the same port pair is established.

## What TCP flags exist?
- **SYN**: Synchronize (start connection)
- **ACK**: Acknowledgment
- **FIN**: Finish (close connection gracefully)
- **RST**: Reset (close connection abruptly)
- **PSH**: Push (deliver data to application immediately)
- **URG**: Urgent (urgent data pointer is valid)
- **ECE/CWR**: Explicit Congestion Notification

## What is TCP congestion control?
Mechanisms to prevent overwhelming the network:
- **Slow start**: Begin with small window, double each RTT
- **Congestion avoidance**: Linear increase once threshold is reached
- **Fast retransmit**: Retransmit on 3 duplicate ACKs without waiting for timeout
- **Fast recovery**: Reduce window by half on triple duplicate ACK (not back to 1)

## What is MSS in TCP?
**Maximum Segment Size** — the largest amount of data (excluding TCP/IP headers) that TCP will send in a single segment. Typically negotiated during the handshake; commonly **1460 bytes** on Ethernet (1500 MTU − 20 IP header − 20 TCP header).

## What TCP port does HTTP use?
**Port 80**

## What TCP port does HTTPS use?
**Port 443**

## What TCP port does SSH use?
**Port 22**

## What is a half-open TCP connection?
A TCP connection where the SYN has been sent but the handshake is not complete. Exploited in **SYN flood attacks** where attackers send many SYN packets without completing the handshake, exhausting server resources.

## What is TCP keepalive?
A feature that sends **probe packets** on an idle connection to check if the remote end is still alive. If no response is received after several probes, the connection is closed.
