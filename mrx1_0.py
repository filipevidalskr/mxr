#!/usr/bin/python
import socket
import sys
import requests
import urllib

addr = input("Type the website: ")  # Here you'll add the website you want to discover the infos requested
host = socket.gethostbyname(addr)  # DNS Resolver

start = 1
end = 65535  # Ports available on a server
open_ports = 0  # Counter for open ports
captured_banners = 0  # Counter for captured banners

# Step 1: Scan for open ports and save them in a .txt file
with open("ports_open.txt", "w") as port_doc:  # Open the file to write the open ports
    for door in range(start, end):
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(1)  # Set a limited time to avoid infinite wait

        # Check if the port is open
        if mySocket.connect_ex((host, door)) == 0:  # Check if there'll be a connection
            open_ports += 1  # Live count about all opened ports found
            print(f"Port {door} opened - Total: {open_ports}")
            print(f"{door}", file=port_doc)  # Write on a file all opened ports
        mySocket.close()  # Close the connection after the trial

print(f"\nScanning completed! Total open ports found: {open_ports}")

# Step 2: Perform banner grabbing and save results in a new file
with open("ports_open.txt", "r") as ports_file, open("banner_grabbing.txt", "w") as banners_file:
    for line in ports_file:
        port = int(line.strip())  # Extract port number from each line
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(2)  # Increase timeout for banner grabbing

        try:
            # Attempt to connect and grab the banner
            mySocket.connect((host, port))
            mySocket.sendall(b"HEAD / HTTP/1.1\r\nHost: %s\r\n\r\n" % addr.encode())
            banner = mySocket.recv(1024).decode("utf-8")  # Receive banner
            
            # Save banner to file
            captured_banners += 1  # Increment banner count
            print(f"Banner found on port {port} - Total banners captured: {captured_banners}")
            banners_file.write(f"Port {port}:\n{banner}\n{'-'*40}\n")
        except Exception as e:
            # Handle cases where no banner is found
            print(f"No banner found on port {port} or connection failed: {e}")
        finally:
            mySocket.close()  # Close socket after each attempt

print(f"\nBanner grabbing completed! Total banners captured: {captured_banners}")
print("Check 'banner_grabbing.txt' for results.")
