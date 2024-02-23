def http_get(url):
    import socket
    global retData
    global body
    retData = ""
    body = ""
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
             retData = retData + str(data, 'utf8');
#            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
    body = setBody(retData)
    return "200"

def http_post(url, data):
    import socket
    global retData
    retData = ""    
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('POST /%s HTTP/1.0\r\nHost: %s\r\n\r\n %s\r\n' % (path, host,data), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            retData = retData + str(data, 'utf8');
            #print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
    return "200"

def setBody(retData):
    import io
    retBody = ""
    foundLinebreak=False
    for line in io.StringIO(retData):
        if(foundLinebreak):
            retBody = retBody + line
        if(not foundLinebreak and line == "\n"):
            foundLinebreak = True
    return retBody
