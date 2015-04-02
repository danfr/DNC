import os, socket, threading, sys, configparser, re
from serveur import Log


def handleConnection(connection, client_address) :
    #try:
    log.printL("Connection from IP -> {}".format(client_address), Log.lvl.INFO)
    userListActive(connection)
    userListAway(connection)
    while True:
        data = connection.recv(4096)
        if data:
            log.printL("Request from IP -> {}"
                       " {}".format(client_address,data.decode()), Log.lvl.INFO)
            threading.Thread(target=handleRequest, args=(connection, data.decode())).start()
        else:
            break
    """except Exception as e :
        log.printL(str(e), Log.lvl.FAIL)"""


def handleRequest(connection, data):
    #try:
    arrayData = data.split(" ")
    if usersConnected[connection][1] is not None :
        if(not arrayData[0][0] == "/"):
            connection.sendall("SUCC_MESSAGE_SENDED".encode())
            broadcastMsg( "NEW_MSG {} {} ".format(usersConnected[connection][1], data))
            return
        else :
            if  arrayData[0] == "/name" :
                changeName(connection, arrayData[1])
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
            if arrayData[0] == "/enable":
                enableUser(connection)
                return
            if arrayData[0] == "/disable":
                disableUser(connection)
                return
            if arrayData[0] == "/quit" :
                quit(connection)
                return
        connection.sendall("ERR_COMMAND_NOT_FOUND".encode())
    else:
        if  arrayData[0] == "/newname" :
            newName(connection, arrayData[1])
            return
        if arrayData[0] == "/quit" :
            quit(connection)
            return
        connection.sendall("ERR_NO_NICKNAME".encode())
    """except Exception as e :
        log.printL(str(e), Log.lvl.FAIL)"""


def broadcastMsg(connection,message):
    for con, value in usersConnected.items() :
        if usersConnected[con][1]  is not None or con != connection:
            try:
                con.sendall(message.encode())
            except Exception as e :
                log.printL(str(e), Log.lvl.FAIL)


def userListActive(connection):
    l = "USERLIST "
    for con, value in usersConnected.items() :
        if value[2] == True :
            l += value[1] + " "
    connection.sendall(l[:-1].encode())


def userListAway(connection):
    l = "USERAWAY "
    for con,value in usersConnected.items() :
        if value[2] == False :
            l += value[1] + " "
    connection.sendall(l[:-1].encode())


def changeName(connection, pseudo):
    if not re.match("^\w{3,15}$",pseudo) :
        connection.sendall("ERR_INVALID_NICKNAME".encode())
    else:
        broadcastMsg(connection,"NAME_CHANGED {} {}".format(usersConnected[connection][1], pseudo))
        connection.sendall("SUCC_VALID_NICKNAME".encode())
        usersConnected[connection][1] = pseudo


def newName(connection, pseudo):
    if not re.match("^\w{3,15}$",pseudo) :
        connection.sendall("ERR_INVALID_NICKNAME".encode())
    else:
        broadcastMsg(connection, "HAS_JOIN {} ".format(pseudo))
        connection.sendall("SUCC_CHANNEL_JOINED".encode())
        usersConnected[connection][1] = pseudo


def askPrivateMsg(connection,pseudo):
    c = getConnectionByPseudo(pseudo)
    if c is None :
        connection.sendall("ERR_USER_NOT_FOUND".encode())
    else:
        pm =  (connection,c)
        if pm in askPM :
            connection.sendall("ALREADY_ASKED".encode())
        else:
            askPM.append(pm)
            c.sendall("ASKING_FOR_PM {}".format(pseudo).encode())
            connection.sendall("SUCC_INVITED".encode())


def acceptPrivateMsg(connection, pseudo):
    c = getConnectionByPseudo(pseudo)
    if c is None :
        connection.sendall("ERR_USER_NOT_FOUND".encode())
    else:
        pm = (connection,c)
        if pm not in askPM :
            connection.sendall("ERR_USER_HAS_NOT_ASK".encode())
        else:
            askPM.remove(pm)
            validatePM.append(pm)
            connection.sendall("SUCC_PRIVATE_DISCUSSION_ACCEPTED".encode())


def rejectPrivateMsg(connection, pseudo):
    c = getConnectionByPseudo(pseudo)
    if c is None :
        connection.sendall("ERR_USER_NOT_FOUND".encode())
    else:
        pm = (connection,c)
        if pm not in askPM :
            connection.sendall("ERR_USER_HAS_NOT_ASK".encode())
        else:
            askPM.remove(pm)
            connection.sendall("SUCC_PRIVATE_DISCUSSION_REFUSED".encode())


def privateMsg(connection, pseudo, msg):
    c = getConnectionByPseudo(pseudo)
    if c is None :
        connection.sendall("ERR_DEST_NOT_FOUND".encode())
    else:
        pm = (connection,c)
        if sorted(pm) not in sorted(validatePM) :
            connection.sendall("ERR_NOT_ACCEPTED".encode())
        else:
            c.sendall("NEW_PM {} {}".format(pseudo,msg).encode())
            connection.sendall("SUCC_PM_SENDED".encode())


def enableUser(connection):
    if usersConnected[connection][2] == False :
        usersConnected[connection][2] = True
        connection.sendall("SUCC_ENABLED".encode())
    else:
        connection.sendall("ERR_NOT_DISABLED".encode())


def disableUser(connection):
    if usersConnected[connection][2] == True :
        usersConnected[connection][2] = False
        connection.sendall("SUCC_DISABLED".encode())
    else:
        connection.sendall("ERR_NOT_ENABLED".encode())


def quit(connection) :
    connection.sendall("SUCCESSFUL_LOGOUT".encode())
    connection.close()
    log.printL("Disconnection from IP -> {}".format(usersConnected[connection][0]), Log.lvl.INFO)
    usersConnected.pop(connection)
    broadcastMsg("HAS_LEFT {}".format(usersConnected[connection][1]))


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
    config = configparser.ConfigParser()
    if not os.path.isfile("dncserver.conf")  :
        config['NETWORK'] = {'port': '2222'}
        config['LOG'] = {'logDirectory': 'log'}
        with open('dncserver.conf', 'w') as configfile:
          config.write(configfile)
    config.read("dncserver.conf")
    log = Log.Log(config["LOG"]["logdirectory"])
    log.printL("Configuration Log", Log.lvl.INFO)
    log.printL("Server start", Log.lvl.INFO)


    #Init socket serv
    sock = socket.socket()
    sock.bind(("", int(config["NETWORK"]["port"])))
    sock.listen(5)
    log.printL("Server Listen on port {}".format(config["NETWORK"]["port"]), Log.lvl.INFO)


    try :
        while True :
            #Connection client
            connection, client_address = sock.accept()
            usersConnected[connection] = [client_address,None,True] # ip pseudo status
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
