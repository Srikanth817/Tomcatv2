#Tomcat main script
import imu_data as imu_class
import ccsds as ccsds_class
import socket

#Initialization stuff
imu_packetization = imu_class.imu_data()
ccsds = ccsds_class.ccsds()
UDP_IP = "127.0.0.1"
UDP_PORT = 5007
UDP_PORT2 = 5006

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))
sock2.bind((UDP_IP, UDP_PORT2))

running = True

#Main loop
bigString = b''
counter = 0
while(running):
	#Read from GNUradio 
	#if something is recieved, process it

	#Read from imu 
	#Packetize and send every 20 data points. 
	data, addr = sock.recvfrom(40)

	if(len(data)!=0):
		bigString +=data
		counter +=1
	if(counter==10):
		running = False

#print(bigString)
software_status_hex = 'AA'
data_hex = imu_packetization.bytestring_to_hex(bigString)
packet = ccsds.data_hex_to_ccsds_hex(data_hex,software_status_hex)

sock2.sendto(bigString,("127.0.0.1",5006))



