## @package Server
#  Module server
import os
import socket
import threading
import sys
import configparser
import re
import Log


#   Code retour
#   INFO
USERLIST_ENABLE = 300
USERLIST_DISABLE = 301
HAS_JOIN = 302
HAS_LEFT = 303
NEW_MSG = 304
NAME_CHANGED = 305
NEW_PM = 306
ASKING_FOR_PM = 307
PRIVATE_DISCU_ACCEPTED_FROM = 308
PRIVATE_DISCU_REFUSED_FROM = 309
IS_NOW_ENABLE = 310
IS_NOW_DISABLE = 311
HAS_ASKED_FILE = 312
CAN_SEND_FILE = 313
HAS_REJECT_FILE = 314

#   SUCCESS
SUCC_CHANNEL_JOINED = 200
SUCC_CHANNEL_QUIT = 201
SUCC_MESSAGE_SENDED = 202
SUCC_NICKNAME_CHANGED = 203
SUCC_PM_SENDED = 205
SUCCESSFUL_ASKED_CONV = 206
SUCCESSFUL_ACCEPTED_CONV = 207
SUCCESSFUL_REFUSED_CONV = 208
SUCC_ENABLED = 209
SUCC_DISABLED = 210
SUCC_PMFILE = 211
SUCC_ACCEPTED_FILE = 212
SUCC_REFUSED_FILE = 213

#    ERROR
ERR_NICKNAME_ALREADY_USED = 400
ERR_NO_NICKNAME = 401
ERR_CONV_NOT_ALLOWED = 402
DEST_NOT_FOUND = 403
ERR_ALREADY_ASKED_FOR_PM = 404
ERR_NO_INVIT_TO_CONV_FOUND = 405
ERR_UNKNOWN_ACCEPTED_FILE = 406
COMMAND_NOT_FOUND = 407
ERR_INVALID_NICKNAME = 408
ERR_INTERNAL_SERVER_ERROR = 409
ERR_NOT_DISABLED = 410
ERR_NOT_ENABLED = 411


##
#   Load Configuration and Start the Server
def main():
    # Global vars
    global usersConnected, log, sock
    global askPM, validatePM
    global askFT
    usersConnected = {}
    askPM = []
    validatePM = []
    askFT = []

    # Config
    config = configparser.ConfigParser()
    if not os.path.isfile("dncServer.conf"):
        config['NETWORK'] = {'port': '2222'}
        config['LOG'] = {'logDirectory': 'log'}
        with open('dncServer.conf', 'w') as configfile:
            config.write(configfile)
    config.read("dncServer.conf")
    log = Log.Log(config["LOG"]["logdirectory"])
    log.printL("Configuration Load", Log.lvl.INFO)
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
            usersConnected[connection] = [client_address, None, True]  # (ip,port) pseudo status
            threading.Thread(target=handle_connection, args=(connection, client_address)).start()
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


##  Handle a connection from a client.
#   Wait for request from the client
#   @param connection the socket descriptor of the connection
#   @param client_adress ("ip", port) of the connection
def handle_connection(connection, client_address):
    try:
        log.printL("Connection from IP -> {}".format(client_address), Log.lvl.INFO)
        while True:
            data = connection.recv(4096)
            if data:
                log.printL("Request from IP -> {}"
                           " {}".format(client_address, data.decode()), Log.lvl.INFO)
                threading.Thread(target=handle_request, args=(connection, data.decode())).start()
            else:
                break
    except Exception as e:
        log.printL("Handle connection fail : ".format(str(e)), Log.lvl.FAIL)
    finally:
        quit_user(connection)


##
#   Handle a request.
#   @param connection the socket descriptor of the request sender
#   @param data the request to handle in String
def handle_request(connection, data):
    try:
        array_data = data.split(" ")

        ### Command for user with nickname ###
        if usersConnected[connection][1] is not None:
            ### No command -> new message ###
            if not array_data[0][0] == "/" and usersConnected[connection][2]:
                connection.sendall("{}".format(SUCC_MESSAGE_SENDED).encode())
                broadcast_message(connection, "{} {} {} ".format(NEW_MSG, usersConnected[connection][1], data))
                return
            else:
                ### Command for user enable & disable ###
                if array_data[0] == "/name":
                    change_name(connection, array_data[1])
                    return
                if array_data[0] == "/userlist":
                    user_list_active(connection)
                    return
                if array_data[0] == "/userlistaway":
                    user_list_away(connection)
                    return
                if array_data[0] == "/enable":
                    enable_user(connection)
                    return
                if array_data[0] == "/disable":
                    disable_user(connection)
                    return
                if array_data[0] == "/quit":
                    connection.shutdown(socket.SHUT_RD)
                    return

                ### Command available for enable only ###
                if not usersConnected[connection][2]:
                    connection.sendall("{}".format(ERR_CONV_NOT_ALLOWED).encode())
                    return
                else:
                    if array_data[0] == "/askpm":
                        ask_private_message(connection, array_data[1])
                        return
                    if array_data[0] == "/acceptpm":
                        accept_private_message(connection, array_data[1])
                        return
                    if array_data[0] == "/rejectpm":
                        reject_private_message(connection, array_data[1])
                        return
                    if array_data[0] == "/pm":
                        private_message(connection, array_data[1], " ".join(array_data[2:]))
                        return
                    if array_data[0] == "/pmfile":
                        ask_file(connection, array_data[1], array_data[2])
                        return
                    if array_data[0] == "/acceptfile":
                        accept_file(connection, array_data[1], " ".join(array_data[3:]), array_data[2])
                        return
                    if array_data[0] == "/rejectfile":
                        reject_file(connection, array_data[1], " ".join(array_data[2:]))
                        return
            connection.sendall("{}".format(COMMAND_NOT_FOUND).encode())
        else:
            ### Command for user without nickname ###
            if array_data[0] == "/newname":
                new_name(connection, array_data[1])
                return
            if array_data[0] == "/quit":
                connection.shutdown(socket.SHUT_RD)
                return
            connection.sendall("{}".format(ERR_NO_NICKNAME).encode())
    except IndexError:
        log.printL("Parameter missing in the request", Log.lvl.WARNING)
        connection.sendall("{}".format(COMMAND_NOT_FOUND).encode())
    except Exception as e:
        log.printL("Handle request fail : {}".format(str(e)), Log.lvl.FAIL)
        connection.sendall("{}".format(ERR_INTERNAL_SERVER_ERROR).encode())


##
#   Broadcast a message to all the users connected except to the sender of the request
#   @param connection the socket descriptor of the request sender
#   @param message message to broadcast (String)
def broadcast_message(connection, message):
    log.printL("User Connected : {}".format(usersConnected), Log.lvl.DEBUG)
    for con, value in usersConnected.items():
        # value 1 : pseudo value 2 : status (enable/disable)
        if value[1] is not None and con != connection and value[2]:
            try:
                con.sendall(message.encode())
            except Exception as e:
                log.printL(str(e), Log.lvl.FAIL)
        log.printL("Broadcast : {}".format(message), Log.lvl.INFO)


##
#   Send the list of enable user
#   @param connection the socket descriptor of the target
def user_list_active(connection):
    l = "{} ".format(USERLIST_ENABLE)
    for con, value in usersConnected.items():
        if value[1] is not None and value[2]:
            l += value[1] + " "
    connection.sendall(l[:-1].encode())
    log.printL("Send to {} : {}".format(usersConnected[connection][0][0], l[:-1]), Log.lvl.INFO)


##
#   Send the list of disable user
#   @param connection the socket descriptor of the target
def user_list_away(connection):
    l = "{} ".format(USERLIST_DISABLE)
    for con, value in usersConnected.items():
        if value[1] is not None and not value[2]:
            l += value[1] + " "
    connection.sendall(l[:-1].encode())


##
#   Change the nickname of the user
#   @param connection the socket descriptor of the target
#   @param pseudo new nickname for the user (String)
def change_name(connection, pseudo):
    if not re.match("^\w{3,15}$", pseudo):
        connection.sendall("{}".format(ERR_INVALID_NICKNAME).encode())
    elif get_connection_by_pseudo(pseudo) is not None:
        connection.sendall("{}".format(ERR_NICKNAME_ALREADY_USED).encode())
    else:
        broadcast_message(connection, "{} {} {}".format(NAME_CHANGED, usersConnected[connection][1], pseudo))
        connection.sendall("{}".format(SUCC_NICKNAME_CHANGED).encode())
        usersConnected[connection][1] = pseudo


##
#   Affect the nickname of the user for the first time
#   @param connection the socket descriptor of the target
#   @param pseudo nickname for the user (String)
def new_name(connection, pseudo):
    if not re.match("^\w{3,15}$", pseudo):
        connection.sendall("{}".format(ERR_INVALID_NICKNAME).encode())
    elif get_connection_by_pseudo(pseudo) is not None:
        connection.sendall("{}".format(ERR_NICKNAME_ALREADY_USED).encode())
    else:
        broadcast_message(connection, "{} {} ".format(HAS_JOIN, pseudo))
        connection.sendall("{}".format(SUCC_CHANNEL_JOINED).encode())
        usersConnected[connection][1] = pseudo


##
#   Ask for a private discussion between the sender of the request and the pseudo
#   @param connection the socket descriptor of the sender
#   @param pseudo the pseudo of target of the demand
def ask_private_message(connection, pseudo):
    c = get_connection_by_pseudo(pseudo)
    if c is None:
        connection.sendall("{}".format(DEST_NOT_FOUND).encode())
    else:
        pm = (connection, c)
        if pm in askPM:
            connection.sendall("{}".format(ERR_ALREADY_ASKED_FOR_PM).encode())
        else:
            askPM.append(pm)
            log.printL("askPm {}".format(askPM), Log.lvl.DEBUG)
            c.sendall("{} {}".format(ASKING_FOR_PM, usersConnected[connection][1]).encode())
            connection.sendall("{}".format(SUCCESSFUL_ASKED_CONV).encode())


##
#   Accept a private discussion
#   @param connection the socket descriptor of the person who accept the private discussion
#   @param pseudo the pseudo of the person who asked for a private discussion
def accept_private_message(connection, pseudo):
    log.printL("askPm {}".format(askPM), Log.lvl.DEBUG)
    c = get_connection_by_pseudo(pseudo)
    if c is None:
        connection.sendall("{}".format(DEST_NOT_FOUND).encode())
    else:
        pm = (c, connection)
        if pm not in askPM:
            connection.sendall("{}".format(ERR_NO_INVIT_TO_CONV_FOUND).encode())
        else:
            askPM.remove(pm)
            validatePM.append(pm)
            connection.sendall("{}".format(SUCCESSFUL_ACCEPTED_CONV).encode())
            c.sendall("{} {}".format(PRIVATE_DISCU_ACCEPTED_FROM, usersConnected[connection][1]).encode())


##
#   Reject a private discussion
#   @param connection the socket descriptor of the person who reject private discussion
#   @param pseudo the pseudo of the person who asked for a private discussion
def reject_private_message(connection, pseudo):
    c = get_connection_by_pseudo(pseudo)
    if c is None:
        connection.sendall("{}".format(DEST_NOT_FOUND).encode())
    else:
        pm = (c, connection)
        pmr = (connection, c)
        if pm not in askPM:
            if pm in validatePM:
                validatePM.remove(pm)
                connection.sendall("{}".format(SUCCESSFUL_REFUSED_CONV).encode())
                c.sendall("{} {}".format(PRIVATE_DISCU_REFUSED_FROM, usersConnected[connection][1]).encode())
            elif pmr in validatePM:
                validatePM.remove(pmr)
                connection.sendall("{}".format(SUCCESSFUL_REFUSED_CONV).encode())
                c.sendall("{} {}".format(PRIVATE_DISCU_REFUSED_FROM, usersConnected[connection][1]).encode())
            else:
                connection.sendall("{}".format(ERR_NO_INVIT_TO_CONV_FOUND).encode())
        else:
            askPM.remove(pm)
            connection.sendall("{}".format(SUCCESSFUL_REFUSED_CONV).encode())
            c.sendall("{} {}".format(PRIVATE_DISCU_REFUSED_FROM, usersConnected[connection][1]).encode())


##
#   Send a private message if a private discussion had been accepted
#   @param connection the soccket descriptor of the sender
#   @param pseudo the pseudo of the private message target
#   @param msg the message to send
def private_message(connection, pseudo, msg):
    c = get_connection_by_pseudo(pseudo)
    if c is None:
        connection.sendall("{}".format(DEST_NOT_FOUND).encode())
    else:
        pm = (connection, c)
        pmr = (c, connection)
        if pm not in validatePM and pmr not in validatePM:
            connection.sendall("{}".format(ERR_CONV_NOT_ALLOWED).encode())
        else:
            c.sendall("{} {} {}".format(NEW_PM, usersConnected[connection][1], msg).encode())
            connection.sendall("{}".format(SUCC_PM_SENDED).encode())


##
#   Ask for a file transfer between the sender of the request and the pseudo
#   @param connection the socket descriptor of the sender
#   @param pseudo the pseudo of target of the demand
def ask_file(connection, pseudo, file):
    c = get_connection_by_pseudo(pseudo)
    if c is None:
        connection.sendall("{}".format(DEST_NOT_FOUND).encode())
    else:
        f = (connection, c, file)
        if f in askFT:
            connection.sendall("{}".format(ERR_ALREADY_ASKED_FOR_PM).encode())
        else:
            askFT.append(f)
            log.printL("askFT {}".format(askFT), Log.lvl.DEBUG)
            c.sendall("{} {} {}".format(HAS_ASKED_FILE, usersConnected[connection][1], file).encode())
            connection.sendall("{}".format(SUCC_PMFILE).encode())


##
#   Accept a file transfer
#   @param connection the socket descriptor of the person who accept a file transfer
#   @param pseudo the pseudo of the person who asked for a file transfer
def accept_file(connection, pseudo, file, port):
    log.printL("askFT {}".format(askFT), Log.lvl.DEBUG)
    c = get_connection_by_pseudo(pseudo)
    if c is None:
        connection.sendall("{}".format(DEST_NOT_FOUND).encode())
    else:
        f = (c, connection, file)
        if f not in askFT:
            connection.sendall("{}".format(ERR_UNKNOWN_ACCEPTED_FILE).encode())
        else:
            askFT.remove(f)
            connection.sendall("{} {}".format(SUCC_ACCEPTED_FILE, usersConnected[c][0][0]).encode())
            c.sendall("{} {} {} {} {}".format(CAN_SEND_FILE, pseudo, usersConnected[connection][0][0],
                                              port, file).encode())


##
#   Reject a file transfer
#   @param connection the socket descriptor of the person who reject a file transfer
#   @param pseudo the pseudo of the person who asked for a file transfer
def reject_file(connection, pseudo, file):
    c = get_connection_by_pseudo(pseudo)
    if c is None:
        connection.sendall("{}".format(DEST_NOT_FOUND).encode())
    else:
        f = (c, connection, file)
        if f not in askFT:
            connection.sendall("{}".format(ERR_UNKNOWN_ACCEPTED_FILE).encode())
        else:
            askPM.remove(f)
            connection.sendall("{}".format(SUCC_REFUSED_FILE).encode())
            connection.sendall("{} {} {}".format(HAS_REJECT_FILE, pseudo, file).encode())


##
#   Enable user
#   @param connection the socket descriptor of the person to enable
def enable_user(connection):
    if not usersConnected[connection][2]:
        usersConnected[connection][2] = True
        connection.sendall("{}".format(SUCC_ENABLED).encode())
        broadcast_message(connection, "{} {}".format(IS_NOW_ENABLE, usersConnected[connection][1]))
    else:
        connection.sendall("{}".format(ERR_NOT_DISABLED).encode())


##
#   Disable user
#   @param connection the socket descriptor of the person to disable
def disable_user(connection):
    if usersConnected[connection][2]:
        usersConnected[connection][2] = False
        connection.sendall("{}".format(SUCC_DISABLED).encode())
        broadcast_message(connection, "{} {}".format(IS_NOW_DISABLE, usersConnected[connection][1]))
    else:
        connection.sendall("{}".format(ERR_NOT_ENABLED).encode())


##
#   Disconnect user
#   @param connection the socket descriptor of the person to disconnect
def quit_user(connection):
    try:
        connection.sendall("{}".format(SUCC_CHANNEL_QUIT).encode())
    except OSError:  # Client close the socket in this side not properly
        log.printL("Client IP -> {} close connection not properly"
                   "".format(usersConnected[connection][0]), Log.lvl.WARNING)
    connection.close()
    log.printL("Disconnection from IP -> {}".format(usersConnected[connection][0]), Log.lvl.INFO)
    pseudo = usersConnected[connection][1]
    usersConnected.pop(connection)
    broadcast_message(connection, "{} {}".format(HAS_LEFT, pseudo))


##
#   Get the socket descriptor by a pseudo
#   @param pseudo pseudo
#   @return the socket descriptor of the pseudo or None
def get_connection_by_pseudo(pseudo):
    for con, value in usersConnected.items():
        if value[1] == pseudo:
            return con
    return None
