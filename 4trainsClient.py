import socket


HOST = '192.168.7.2'     # Endereco IP do Servidor
PORT = 65433            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.connect((HOST, PORT))
print ('Para sair use CTRL+X\n')
msg = bytes(input("Informe a mensagem: "),'utf-8')

while (msg != b'\x18'):
    tcp.send (msg)
    msg = bytes(input("Informe a mensagem: "),'utf-8')
tcp.close()
