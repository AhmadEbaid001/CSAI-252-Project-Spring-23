
import socket
import time


def send_file(file_name, receiver_ip, receiver_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)  # Set a timeout for the socket

    with open(file_name, 'rb') as f:
        file_data = f.read()

    packet_size = 200
    num_packets = -(-len(file_data) // packet_size)  # Calculate the number of packets

    for i in range(num_packets):
        packet_data = file_data[i * packet_size:(i + 1) * packet_size]
        packet = f"{i}|".encode() + packet_data

        while True:
            try:
                # Send the packet
                print(f"Sending packet {i}")  # Add this line
                sock.sendto(packet, (receiver_ip, receiver_port))

                # Wait for an acknowledgement
                ack_data, _ = sock.recvfrom(1024)
                ack_num = int(ack_data.decode())
                if ack_num == i + 1:
                    print(f"Received ACK for packet {i}")  # Add this line
                    break
            except socket.timeout:
                print(f"Timeout for packet {i}")  # Add this line
                pass

    # Send an end-of-file packet
    eof_packet = f"{num_packets}|EOF".encode()  # Update this line
    print("Sending EOF packet")  # Add this line
    sock.sendto(eof_packet, (receiver_ip, receiver_port))

    # Close the socket
    sock.close()


if __name__ == "_main_":
    file_name = "test_file"
    receiver_ip = "192.168.1.17"
    receiver_port = 9000

    send_file(file_name, receiver_ip, receiver_port)
