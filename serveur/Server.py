import argparse
import socket
import threading
import re
import sys
from serveur import Log


def handleConnection(connection, client_address) :
    try:
        log.printL("Connection from IP -> {}".format(client_address), Log.lvl.INFO)
        while True:
            data = connection.recv(4096)
            if data:
                log.printL("Request from IP -> {} \n"
                           "{}".format(client_address,data.decode()), Log.lvl.INFO)
                threading.Thread(target=handleRequest, args=(connection, data.decode())).start()
            else:
                break
    except Exception as e :
        log.printL(str(e), Log.lvl.FAIL)


def handleRequest(connection, data):
    arrayData = data.split(" ")
    if(not arrayData[0][0] == "/"):
        broadcastMsg( "NEW_MSG {} {} ".format(usersConnected[connection][1], data))
        return
    else :
        if  arrayData[0] == "/name" :
            changeName(connection, arrayData[1])
            return
        if arrayData[0] == "/quit" :
            quit(connection)
            return
    connection.send("ERR_COMMAND_NOT_FOUND".encode())


def broadcastMsg(message) :
    for con, value in usersConnected.items() :
            con.send(message.encode())


def changeName(connection, pseudo) :
    broadcastMsg("NAME_CHANGED {} {}".format(usersConnected[connection][1], pseudo))
    usersConnected[connection][1] = pseudo


def quit(connection) :
    broadcastMsg("HAS_LEFT {}".format(usersConnected[connection][1]))
    connection.close()
    usersConnected.__delitem__(connection)
    log.printL("Disconnection from IP -> {}".format(usersConnected[connection][0]), Log.lvl.INFO)

def main():
    #Global vars
    global usersConnected, log
    usersConnected = {}
    log = Log.Log()
    log.printL("Server start", Log.lvl.INFO)

    #Configuration
    parser = argparse.ArgumentParser(usage="usage='%(prog)s [options]",description='Server DNC')
    parser.add_argument('--port', type=int, dest='port', action='store',
                 default=8000, help='port (default=8000)')
    args = parser.parse_args()
    log.printL("Configuration load {}".format(args), Log.lvl.INFO)

    #Init socket serv
    sock = socket.socket()
    sock.bind(("", args.port))
    sock.listen(5)
    log.printL("Server Listen on port {} ".format(args.port), Log.lvl.INFO)


    try :
        while True :
            #Connection client
            connection, client_address = sock.accept()
            usersConnected[connection] = [client_address,"Anonymous"]
            threading.Thread(target=handleConnection,args=(connection,client_address)).start()
    except KeyboardInterrupt :
        # Disable to received more requests on socket
        for con, value in usersConnected.items():
            con.shutdown(socket.SHUT_RD)
    finally :
        #Wait for threads finish
        log.printL("Wait for threads ending", Log.lvl.INFO)
        for t in threading.enumerate():
            if t!= threading.main_thread():
                t.join()
        #Close all clients sockets
        for con, value in usersConnected.items():
            con.close()
            log.printL("Disconnection IP -> {}".format(value[0]), Log.lvl.INFO)
        #Close the sockets server
        log.printL("Sockets close", Log.lvl.INFO)
        sock.close()
        log.printL("Server shutdown", Log.lvl.INFO)
        sys.exit(0)


if __name__ == '__main__':
    main()