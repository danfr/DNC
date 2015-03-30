from socket import *

Host = "127.0.0.1"
Port = 2222
Addr = (Host,Port)

def Client():
	s = socket(AF_INET,SOCK_STREAM);
	s.connect(Addr);

	while True :
			cmd = input("Entrez votre commande (help pour la liste des commandes et quit pour quitter) : ")
			if cmd.lower() == "quit":
				break
			try :
				s.send(cmd.encode())
				#data , addr = s.recvfrom(4096)
				#print(data.decode())
			except timeout :
				print("Erreur : Timeout. Le serveur ne repond pas.")
			
	s.close();


if __name__ == "__main__":
	Client()



