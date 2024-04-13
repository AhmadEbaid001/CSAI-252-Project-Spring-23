
import socket
def receive_file(file_name, port):
    buffer_size = 65507  # Maximum UDP payload size

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))

    received_file_data = []
    expected_packet_num = 0

    while True:
        packet, sender_addr = sock.recvfrom(buffer_size)
        try:
            packet_num, packet_data = packet.split(b'|', 1)
            packet_num = int(packet_num)
        except ValueError:
            print("Error: Unable to split packet")  # Add this line
            continue

        if packet_num == expected_packet_num:
            if packet_data == b'EOF':  # Update this line
                print("Received EOF packet")  # Add this line
                break

            received_file_data.append(packet_data)
            expected_packet_num += 1
            print(f"Received packet {packet_num}")  # Add this line

        # Send an acknowledgement
        ack_packet = str(expected_packet_num).encode()
        sock.sendto(ack_packet, sender_addr)
        print(f"Sent ACK for packet {expected_packet_num}")  # Add this line

    # Write the received file data to a file
    with open(file_name, 'wb') as f:
        f.write(b''.join(received_file_data))
    sock.close()


if __name__ == "_main_":
    file_name = "receiver_file"
    port = 9000

    receive_file(file_name, port)
