import socket
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

def capture_packets(packet_count=10, output_file='packet_log.csv'):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        sock.bind(("0.0.0.0", 0))  

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        try:
            sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        except AttributeError:
            pass 

        captured_data = []

        print(f"Capturing {packet_count} packets...")

        for _ in range(packet_count):
            packet = sock.recvfrom(65565)
            packet_data = packet[0]

            source_ip = '.'.join(map(str, packet_data[12:16]))
            destination_ip = '.'.join(map(str, packet_data[16:20]))

            captured_data.append([source_ip, destination_ip])

        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Source IP', 'Destination IP'])
            writer.writerows(captured_data)

        print(f"\nPacket capture completed. Data saved to {output_file}.")

        try:
            sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        except AttributeError:
            pass 

        sock.close()
    except PermissionError:
        print("Permission denied: Please run the script as Administrator.")
