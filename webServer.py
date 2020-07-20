import socket


class WebServer:

    def __init__(self, port, ip, fileName):
        self.port = port
        self.ip = ip
        self.listenNumber = 1
        self.packetSize = 1024
        self.socket = self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fileName = fileName

    def start(self):

        """
        start connection and listen for signal
        """

        self.socket.bind((self.ip, self.port))
        self.socket.listen(self.listenNumber)
        self.printLine()
        print("start for listening ")

    def _send_file_handler(self):

        """
            :param fileName: we use default file name in this server
            :return: data of file(string) and isFileExist (boolean)
        """
        data = ''
        try:
            f = open(self.fileName, 'rb')
            line = f.read(1024)
            while (line):
                data += line.decode('utf-8')
                line = f.read(1024)
            f.close()
            return data, True
        except:
            msg = "file not exist"
            print(msg)
            data = msg
            return data, False

    def _set_fileName(self, msg):
        """

        :param msg : msg of signal
        set global variable of fileName if file name sent in url var set to file name
        else default file name read from constructor(when initiate webServer calss for
        first time )
        """
        file  =msg.splitlines()[0].split('/')[1].split(' ')[0]
        if (file != ''):
            self.fileName = file
        print("file name:",self.fileName)

    def _generate_headers(self, response_code):
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

        header += 'Server: Behnam&Morteza-server \n'
        header += 'Connection: close\n\n'  # Signal that connection will be closed after completing the request
        return header

    def printLine(self):
        """print line !"""
        print('-------------------------------------------------')

    def request_handler(self):
        """make loop and accpeting signal of socket making appropriate response
            close the signal
        """

        size = 1024
        while True:
            # accept message from client
            clientSock, addr = self.socket.accept()
            self.printLine()
            print('connect to {}'.format(addr))

            # print client message content
            msg = clientSock.recv(size).decode('utf-8')
            self.printLine()
            print("sent message :")
            print(msg)

            self.printLine()
            self._set_fileName(msg)

            # check for existance of file in the server (with name of file.txt)
            data, isFileExist = self._send_file_handler()

            self.printLine()
            print('data of file :')
            print(data)

            # create  header for response message
            if isFileExist:
                header = self._generate_headers(200)
            else:
                header = self._generate_headers(404)

            response = header.encode() + data.encode()

            # send response in http protocol
            clientSock.send(response)

            # close the signal
            clientSock.close()
