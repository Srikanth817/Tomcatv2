import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5007
    
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

sock.bind((UDP_IP, UDP_PORT))
#sock2.bind(("127.0.0.1", 5006))

while True:
  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  print(data)
  # if(data=="hello"):
  #   sock2.sendto("Recieved",("127.0.0.1",5006))
  
  # if(data=='166'):
  #   sock2.send(b'hello')
  