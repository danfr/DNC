import argparse
import socket
import threading
import sys
from serveur import Log


def handleConnection(connection, client_address) :
    try:
        log.printL("Connection from IP -> {}".format(client_address), Log.lvl.INFO)
        while True:
            data = connection.recv(4096)
            if data:
                log.printL("Request from IP -> {}"
                           " {}".format(client_address,data.decode()), Log.lvl.INFO)
                threading.Thread(target=handleRequest, args=(connection, data.decode())).start()
            else:
                break
    except Exception as e :
        log.printL(str(e), Log.lvl.FAIL)


def handleRequest(connection, data):
    try:
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
            if arrayData[0] == "/askpm" :
                askPrivateMsg(connection,arrayData[1])
                return
            if arrayData[0] == "/acceptpm" :
                acceptPrivateMsg(connection,arrayData[1])
                return
            if arrayData[0] == "/rejectpm" :
                rejectPrivateMsg(connection,arrayData[1])
                return
            if arrayData[0] == "/pm" :
                privateMsg(connection,arrayData[1],arrayData[2:])
                return
        connection.send("ERR_COMMAND_NOT_FOUND".encode())
    except Exception as e :
        log.printL(str(e), Log.lvl.FAIL)


def broadcastMsg(message):
    sock.sendall(message.encode())


def userListActive(connection):
    l = "USERLIST "
    for con,value in usersConnected :
        if value[2] == True :
            l += value[1] + " "
    connection.send(l[:-1].encode())


def userListAway(connection):
    l = "USERAWAY "
    for con,value in usersConnected :
        if value[2] == False :
            l += value[1] + " "
    connection.send(l[:-1].encode())


def changeName(connection, pseudo):
    broadcastMsg("NAME_CHANGED {} {}".format(usersConnected[connection][1], pseudo))
    usersConnected[connection][1] = pseudo


def askPrivateMsg(connection,pseudo):
    c = getConnectionByPseudo(pseudo)
    if c is None :
        connection.send("ERR_USER_NOT_FOUND".encode())
    else:
        pm =  (connection,c)
        if pm in askPM :
            connection.send("ALREADY_ASKED".encode())
        else:
            askPM.append(pm)
            c.send("NEW_MESSAGE {0} demande une conversation privé \n"
                   "/acceptpm {0} pour accepter\n"
                   "/reject {0} pour refuser".format(pseudo))
            connection.send("SUCC_INVITED".encode())


def acceptPrivateMsg(connection, pseudo):
    c = getConnectionByPseudo(pseudo)
    if c is None :
        connection.send("ERR_USER_NOT_FOUND".encode())
    else:
        pm = (connection,c)
        if pm not in askPM :
            connection.send("ERR_USER_HAS_NOT_ASK".encode())
        else:
            askPM.remove(pm)
            validatePM.append(pm)
            connection.send("SUCC_PRIVATE_DISCUSSION_ACCEPTED".encode())


def rejectPrivateMsg(connection, pseudo):
    c = getConnectionByPseudo(pseudo)
    if c is None :
        connection.send("ERR_USER_NOT_FOUND".encode())
    else:
        pm = (connection,c)
        if pm not in askPM :
            connection.send("ERR_USER_HAS_NOT_ASK".encode())
        else:
            askPM.remove(pm)
            connection.send("SUCC_PRIVATE_DISCUSSION_REFUSED".encode())


def privateMsg(connection, pseudo, msg):
    c = getConnectionByPseudo(pseudo)
    if c is None :
        connection.send("ERR_DEST_NOT_FOUND".encode())
    else:
        pm = (connection,c)
        if sorted(pm) not in sorted(validatePM) :
            connection.send("ERR_NOT_ACCEPTED".encode())
        else:
            c.send("NEW_PM {} {}".format(pseudo,msg).encode())
            connection.send("SUCC_PM_SENDED".encode())


def quit(connection) :
    broadcastMsg("HAS_LEFT {}".format(usersConnected[connection][1]))
    connection.send("SUCCESSFUL_LOGOUT".encode())
    connection.close()
    usersConnected.__delitem__(connection)
    log.printL("Disconnection from IP -> {}".format(usersConnected[connection][0]), Log.lvl.INFO)


def getConnectionByPseudo(pseudo):
    for con, value in usersConnected.items() :
        if value[1] == pseudo :
            return con
    return None


def main():
    #Global vars
    global usersConnected, log, sock
    usersConnected = {}
    global askPM, validatePM
    global askFT, validateFT
    askPM = []
    validatePM = []
    log = Log.Log()

    #Configuration
    parser = argparse.ArgumentParser(usage="usage='%(prog)s [options]",description='Server DNC')
    parser.add_argument('--port', type=int, dest='port', action='store',
                 default=8000, help='port (default=8000)')
    parser.add_argument('--usermax', type=int, dest='usermax', action='store',
                 default=None, help='usermax (default=None)')
    args = parser.parse_args()
    log.printL("Configuration load {}".format(args), Log.lvl.INFO)
    log.printL("Server start", Log.lvl.INFO)

    #Init socket serv
    sock = socket.socket()
    sock.bind(("", args.port))
    sock.listen(5)
    log.printL("Server Listen on port {}".format(args.port), Log.lvl.INFO)


    try :
        while True :
            #Connection client
            connection, client_address = sock.accept()
            usersConnected[connection] = [client_address,"Anonymous",True] # ip pseudo status
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
            quit(con)
        #Close the socket server
        sock.close()
        log.printL("Server shutdown", Log.lvl.INFO)
        sys.exit(0)


if __name__ == '__main__':
    main()