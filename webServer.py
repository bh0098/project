
import socket



def send_file_handler(socket, fileName='file.txt'):
    """

    :param socket:
    :param fileName: we use default file name in this server
    :return: data of file(string) and isFileExist (boolean)
    """
    data = ''
    try:
        f = open(fileName, 'rb')
        line = f.read(1024)
        while (line):
            # socket.send(line)
            # print("line",line)
            data +=line.decode('utf-8')
            # print("data on fn: ", data)
            print('Sent ', repr(line))
            line = f.read(1024)
        f.close()
        return data,True
    except:
        return data,False




def _generate_headers(response_code):
    """
        Parameter : Response code (200 or 4040)
        Generate response Header
        404 or 200 status
    """
    header = ''
    if response_code == 200:
        header += 'HTTP/1.1 200 OK\n'
    elif response_code == 404:
        header += 'HTTP/1.1 404 Not Found\n'

    # time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    # header += 'Date: {now}\n'.format(now=time_now)
    header += 'Server: Behnam&Morteza-server \n'
    header += 'Connection: close\n\n'  # Signal that connection will be closed after completing the request
    return header


port = 8080
ip = ''
# create port
sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# make connection with port and ip
sok.bind((ip, port))

# listening to the port
sok.listen(5)

rscvPort = 8000
size = 1024
while True:
    clientSock, addr = sok.accept()
    print('connect to {}'.format(addr))
    binaryMsg = clientSock.recv(size)
    msg = binaryMsg.decode('utf-8')
    print('print msg : ', msg)
    matches = msg.split()

    # print('socket name {}'.format(clientSock.getsockname()))
    response = ''
    data,isFileExist= send_file_handler(socket=clientSock)
    print('data of file :',data)
    if isFileExist:
        header = _generate_headers(200)
        response = header.encode() + data.encode()
    else:
        header = _generate_headers(404)
        response = header
    clientSock.send(response)
    # clientSock.send(bytes('thanks','utf-8'))
    clientSock.close()
