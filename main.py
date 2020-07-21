from webServer import WebServer

port = 8080
ip = ''
file = 'home.html'

server = WebServer(port, ip, file)
server.start()
server.request_handler()
