import pyshark

def packet_sniffer(interface, packet_count, client_ip):
    # Create a capture object
    capture = pyshark.LiveCapture(interface=interface, display_filter=f"ip.src == {client_ip}")

    # Start capturing packets
    capture.sniff(packet_count=packet_count)

    # Print information about each packet
    for packet in capture:
        print("Protocol:", packet.layers[1].layer_name)  # Print the protocol of the packet
        print("Payload Size:", len(packet.layers[-1]))  # Print the size of the payload in bytes
        print("------------------------")

if __name__ == "__main__":
    interface = input("Enter interface (e.g. eth0): ")  # specify the interface to sniff packets on (e.g., eth0 for Ethernet)
    packet_count = int(input("Enter the number of packets to capture: "))  # specify the number of packets to capture
    client_ip = input("Enter client IP address: ")  # specify the IP address of your client application
    packet_sniffer(interface, packet_count, client_ip)
