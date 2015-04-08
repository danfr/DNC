import os, socket, threading, sys, configparser, re
from serveur import Log


def handleConnection(connection, client_address):
    try:
        log.printL("Connection from IP -> {}".format(client_address), Log.lvl.INFO)
        while True:
            data = connection.recv(4096)
            if data:
                log.printL("Request from IP -> {}"
                           " {}".format(client_address, data.decode()), Log.lvl.INFO)
                threading.Thread(target=handleRequest, args=(connection, data.decode())).start()
            else:
                break
    except Exception as e:
        log.printL("Handle connection fail : ".format(str(e)), Log.lvl.FAIL)
    finally:
        quit(connection)


def handleRequest(connection, data):
    try:
        arrayData = data.split(" ")

        ### Command for user with nickname ###
        if usersConnected[connection][1] is not None:
            ### No command -> new message ###
            if not arrayData[0][0] == "/" and usersConnected[connection][2]:
                connection.sendall("SUCC_MESSAGE_SENDED".encode())
                broadcastMsg(connection, "NEW_MSG {} {} ".format(usersConnected[connection][1], data))
                return
            else:
                ### Command for user enable & disable ###
                if arrayData[0] == "/name":
                    changeName(connection, arrayData[1])
                    return
                if arrayData[0] == "/userlist":
                    userListActive(connection)
                    return
                if arrayData[0] == "/userlistaway":
                    userListAway(connection)
                    return
                if arrayData[0] == "/enable":
                    enableUser(connection)
                    return
                if arrayData[0] == "/disable":
                    disableUser(connection)
                    return
                if arrayData[0] == "/quit":
                    connection.shutdown(socket.SHUT_RD)
                    return

                ### Command available for enable only ###
                if not usersConnected[connection][2] :
                    connection.sendall("ERR_U_ARE_DISABLE".encode())
                    return
                else :
                    if arrayData[0] == "/askpm":
                        askPrivateMsg(connection, arrayData[1])
                        return
                    if arrayData[0] == "/acceptpm":
                        acceptPrivateMsg(connection, arrayData[1])
                        return
                    if arrayData[0] == "/rejectpm":
                        rejectPrivateMsg(connection, arrayData[1])
                        return
                    if arrayData[0] == "/pm":
                        privateMsg(connection, arrayData[1], " ".join(arrayData[2:]))
                        return
                    if arrayData[0] == "/pmfile":
                        askFile(connection,arrayData[1],arrayData[2])
                        return
                    if arrayData[0] == "/acceptfile":
                        acceptFile(connection, arrayData[1], arrayData[2],arrayData[3])
                        return
                    if arrayData[0] == "/rejectfile":
                        rejectFile(connection, arrayData[1], " ".join(arrayData[2:]))
                        return
            connection.sendall("ERR_COMMAND_NOT_FOUND".encode())
        else:
            ### Command for user without nickname ###
            if arrayData[0] == "/newname":
                newName(connection, arrayData[1])
                return
            if arrayData[0] == "/quit":
                connection.shutdown(socket.SHUT_RD)
                return
            connection.sendall("ERR_NO_NICKNAME".encode())
    except IndexError:
        log.printL("Parameter missing in the request", Log.lvl.WARNING)
        connection.sendall("ERR_PARAMETER_MISSING".encode())
    except Exception as e :
        log.printL("Handle request fail : {}".format(str(e)), Log.lvl.FAIL)
        connection.sendall("ERR_INTERNAL_SERVER_ERROR".encode())


def broadcastMsg(connection, message):
    log.printL("User Connected : {}".format(usersConnected), Log.lvl.DEBUG)
    for con, value in usersConnected.items():
        if value[1] is not None and con != connection and value[2] == True:
            try:
                con.sendall(message.encode())
            except Exception as e:
                log.printL(str(e), Log.lvl.FAIL)


def userListActive(connection):
    l = "USERLIST "
    for con, value in usersConnected.items():
        if value[1] is not None and value[2]:
            l += value[1] + " "
    connection.sendall(l[:-1].encode())


def userListAway(connection):
    l = "USERAWAY "
    for con, value in usersConnected.items():
        if value[1] is not None and not value[2]:
            l += value[1] + " "
    connection.sendall(l[:-1].encode())


def changeName(connection, pseudo):
    if not re.match("^\w{3,15}$", pseudo):
        connection.sendall("ERR_INVALID_NICKNAME".encode())
    elif getConnectionByPseudo(pseudo) is not None:
        connection.sendall("ERR_NICKNAME_ALREADY_USED")
    else:
        broadcastMsg(connection, "NAME_CHANGED {} {}".format(usersConnected[connection][1], pseudo))
        connection.sendall("SUCC_VALID_NICKNAME".encode())
        usersConnected[connection][1] = pseudo


def newName(connection, pseudo):
    if not re.match("^\w{3,15}$", pseudo):
        connection.sendall("ERR_INVALID_NICKNAME".encode())
    elif getConnectionByPseudo(pseudo) is not None:
        connection.sendall("ERR_NICKNAME_ALREADY_USED".encode())
    else:
        broadcastMsg(connection, "HAS_JOIN {} ".format(pseudo))
        connection.sendall("SUCC_CHANNEL_JOINED".encode())
        usersConnected[connection][1] = pseudo
        userListActive(connection)
        userListAway(connection)


def askPrivateMsg(connection, pseudo):
    c = getConnectionByPseudo(pseudo)
    if c is None:
        connection.sendall("ERR_USER_NOT_FOUND".encode())
    else:
        pm = (connection, c)
        if pm in askPM:
            connection.sendall("ALREADY_ASKED".encode())
        else:
            askPM.append(pm)
            log.printL("askPm {}".format(askPM), Log.lvl.DEBUG)
            c.sendall("ASKING_FOR_PM {}".format(usersConnected[connection][1]).encode())
            connection.sendall("SUCC_INVITED".encode())


def acceptPrivateMsg(connection, pseudo):
    log.printL("askPm {}".format(askPM), Log.lvl.DEBUG)
    c = getConnectionByPseudo(pseudo)
    if c is None:
        connection.sendall("ERR_USER_NOT_FOUND".encode())
    else:
        pm = (c, connection)
        if pm not in askPM:
            connection.sendall("ERR_USER_HAS_NOT_ASK".encode())
        else:
            askPM.remove(pm)
            validatePM.append(pm)
            connection.sendall("SUCC_PRIVATE_DISCUSSION_ACCEPTED".encode())
            c.sendall("SUCC_PRIVATE_DISCUSSION_OK {}".format(usersConnected[connection][1]).encode())


def rejectPrivateMsg(connection, pseudo):
    c = getConnectionByPseudo(pseudo)
    if c is None:
        connection.sendall("ERR_USER_NOT_FOUND".encode())
    else:
        pm = (c, connection)
        pmr = (connection, c)
        if pm not in askPM:
            if pm in validatePM :
                validatePM.remove(pm)
                connection.sendall("SUCC_PRIVATE_DISCUSSION_REFUSED".encode())
                c.sendall("SUCC_PRIVATE_DISCUSSION_REJECTED {}".format(usersConnected[connection][1]).encode())
            elif pmr in validatePM :
                validatePM.remove(pmr)
                connection.sendall("SUCC_PRIVATE_DISCUSSION_REFUSED".encode())
                c.sendall("SUCC_PRIVATE_DISCUSSION_REJECTED {}".format(usersConnected[connection][1]).encode())
            else :
                connection.sendall("ERR_USER_HAS_NOT_ASK".encode())
        else:
            askPM.remove(pm)
            connection.sendall("SUCC_PRIVATE_DISCUSSION_REFUSED".encode())
            c.sendall("SUCC_PRIVATE_DISCUSSION_REJECTED {}".format(usersConnected[connection][1]).encode())


def privateMsg(connection, pseudo, msg):
    c = getConnectionByPseudo(pseudo)
    if c is None:
        connection.sendall("ERR_DEST_NOT_FOUND".encode())
    else:
        pm = (connection, c)
        pmr = (c,connection)
        if pm not in validatePM and pmr not in validatePM:
            connection.sendall("ERR_NOT_ACCEPTED".encode())
        else:
            c.sendall("NEW_PM {} {}".format(pseudo, msg).encode())
            connection.sendall("SUCC_PM_SENDED".encode())


def askFile(connection, pseudo, file):
    c = getConnectionByPseudo(pseudo)
    if c is None:
        connection.sendall("ERR_USER_NOT_FOUND".encode())
    else:
        f = (connection, c, file)
        if f in askFT:
            connection.sendall("ERR_ALREADY_ONE".encode())
        else:
            askFT.append(f)
            log.printL("askFT {}".format(askFT), Log.lvl.DEBUG)
            c.sendall("HAS_ASKED_FILE {} {}".format(usersConnected[connection][1], file).encode())
            connection.sendall("SUCC_ASKED_FILE".encode())


def acceptFile(connection, pseudo, file, port):
    log.printL("askFT {}".format(askFT), Log.lvl.DEBUG)
    c = getConnectionByPseudo(pseudo)
    if c is None:
        connection.sendall("ERR_USER_NOT_FOUND".encode())
    else:
        f = (c, connection, file)
        if f not in askFT:
            connection.sendall("ERR_USER_HAS_NOT_ASK".encode())
        else:
            askFT.remove(f)
            connection.sendall("SUCC_FILE_ACCEPTED {}".format(usersConnected[c][0][0]).encode())
            c.sendall("CAN_SEND_FILE {} {} {} {}".format(file,pseudo,usersConnected[connection][0][0], port).encode())


def rejectFile(connection, pseudo, file):
    c = getConnectionByPseudo(pseudo)
    if c is None:
        connection.sendall("ERR_USER_NOT_FOUND".encode())
    else:
        f = (c, connection, file)
        if f not in askFT:
            connection.sendall("ERR_USER_HAS_NOT_ASK".encode())
        else:
            askPM.remove(f)
            connection.sendall("SUCC_FILE_REFUSED".encode())


def enableUser(connection):
    if usersConnected[connection][2] == False:
        usersConnected[connection][2] = True
        connection.sendall("SUCC_ENABLED".encode())
        broadcastMsg(connection,"IS_NOW_ENABLE {}".format(usersConnected[connection][1]))
    else:
        connection.sendall("ERR_NOT_DISABLED".encode())


def disableUser(connection):
    if usersConnected[connection][2] == True:
        usersConnected[connection][2] = False
        connection.sendall("SUCC_DISABLED".encode())
        broadcastMsg(connection,"IS_NOW_DISABLE {}".format(usersConnected[connection][1]))
    else:
        connection.sendall("ERR_NOT_ENABLED".encode())


def quit(connection):
    try:
        connection.sendall("SUCCESSFUL_LOGOUT".encode())
    except OSError:  # Client close the socket in this side not properly
        log.printL("Client IP -> {} close connection not properly"
                   "".format(usersConnected[connection][0]), Log.lvl.WARNING)
    connection.close()
    log.printL("Disconnection from IP -> {}".format(usersConnected[connection][0]), Log.lvl.INFO)
    pseudo = usersConnected[connection][1]
    usersConnected.pop(connection)
    broadcastMsg(connection, "HAS_LEFT {}".format(pseudo))


def getConnectionByPseudo(pseudo):
    for con, value in usersConnected.items():
        if value[1] == pseudo:
            return con
    return None


def main():
    # Global vars
    global usersConnected, log, sock
    global askPM, validatePM
    global askFT
    usersConnected = {}
    askPM = []
    validatePM = []
    askFT = []
    config = configparser.ConfigParser()
    if not os.path.isfile("dncserver.conf"):
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

    try:
        while True:
            #Connection client
            connection, client_address = sock.accept()
            usersConnected[connection] = [client_address, None, True]  # ip pseudo status
            threading.Thread(target=handleConnection, args=(connection, client_address)).start()
    except KeyboardInterrupt:
        # Disable to received more requests on socket
        for con, value in usersConnected.items():
            con.shutdown(socket.SHUT_RD)
    finally:
        #Wait for threads finish
        log.printL("Wait for threads ending", Log.lvl.INFO)
        for t in threading.enumerate():
            if t != threading.main_thread():
                t.join()
        sock.close()
        log.printL("Server shutdown", Log.lvl.INFO)
        sys.exit(0)
