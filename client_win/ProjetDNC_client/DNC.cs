using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Windows.Forms;

namespace ProjetDNC_client
{
    public partial class Main_form : Form //Code à usage non-graphique
    {
        public string mon_pseudo;
        public string tmp_pseudo = null;
        private byte[] myBuff = new byte[4096];
        private Thread t = null;
        private System.Windows.Forms.Timer timer;

        /// <summary>
        /// Envoi de la requete :who à chaque signal du timer
        /// </summary>
        private void timer_Tick(object sender, EventArgs e)
        {
            Envoyer(conf.GetValue("USERLIST", "COMMAND"));
        }

        /// <summary>
        /// Envoi d'une requête DNC formattée au serveur
        /// </summary>
        /// <param name="pseudo">Pseudo de la cible</param>
        /// <param name="commande">Commande de la requête</param>
        /// <param name="contenu">Contenu de la requête</param>
        public void Envoyer(string pseudo, string commande, string contenu)
        {
            contenu = contenu.Replace("\n", "\n          ").Replace('|', ' ').Trim(); // Les sauts de ligne et le | sont indedits

            if (pseudo != null && pseudo != "")
            {
                pseudo = " " + pseudo;
            }

            if (contenu != null && contenu != "")
            {
                contenu = " " + contenu;
            }

            string mess = commande + pseudo + contenu;
            mess = mess.Trim();

            if(sock.Connected)
                sock.Send(Encoding.UTF8.GetBytes(mess + "|"));
        }

        /// <summary>
        /// Envoi d'une requête DNC formattée au serveur sans contenu
        /// </summary>
        /// <param name="prefixe">Préfixe de la requête</param>
        /// <param name="commande">Commande de la requête</param>
        public void Envoyer(string prefixe, string commande)
        {
            Envoyer(prefixe, commande, "");
        }

        /// <summary>
        /// Envoi d'une requête DNC formattée au serveur sans préfixe ni contenu
        /// </summary>
        /// <param name="commande">Commande de la requête</param>
        public void Envoyer(string commande)
        {
            Envoyer("", commande);
        }

        /// <summary>
        /// Attend un message du serveur et le décompose dans un objet Mess (uniquement utilisé en mode synchrone)
        /// </summary>
        /// <returns>Mess représentant le message reçu</returns>
        public Mess Recevoir()
        {
            myBuff = new byte[4096];
            sock.Receive(myBuff);
            string reponse = Encoding.UTF8.GetString(myBuff);
            reponse = reponse.TrimEnd('|', ' ', '\0');
            string[] tab = reponse.Split(new char[] { ' ' }, 3);

            if(tab.Length == 1)
                return new Mess(tab[0], "", "");
            else if(tab.Length == 2)
                return new Mess(tab[0], tab[1], "");
            else
                return new Mess(tab[0], tab[1], tab[2]);
        }

        /// <summary>
        /// Méthode de lancement du thread d'écoute en mode asynchrone
        /// </summary>
        public void Lancer_ecoute(string pseudo)
        {
            mon_pseudo = pseudo;

            //Lancement d'un timer pour l'appel régulier à la commande :who
            timer = new System.Windows.Forms.Timer();
            timer.Tick += new EventHandler(timer_Tick);
            timer.Interval = 10000; // Toutes les 10 secondes
            timer.Start();

            Envoyer(conf.GetValue("USERLIST", "COMMAND")); //Récupération de la liste des clients connectés
            t = new Thread(() => Ecoute(this, sock));
            t.Start();
        }

        /// <summary>
        /// Tread d'écoute (asynchcrone)
        /// </summary>
        /// <param name="form">Formulaire de base (requis pour les invocations asynchrones des méthodes déléguées)</param>
        /// <param name="sock">Socket client</param>
        public void Ecoute(Main_form form, Socket sock)
        {
            Thread.CurrentThread.IsBackground = true;
            byte[] Buff;

            while (true)
            {
                StringBuilder builder = new StringBuilder();

                string reponse, part = "";

                do
                {
                    Buff = new byte[4096];
                    try
                    {
                        //Réception du message
                        sock.Receive(Buff);
                    }
                    catch(SocketException) //Déconnexion à l'initiative du serveur
                    {
                        form.Invoke(form.del_close_fromserv);
                        return;
                    }

                    part = Encoding.UTF8.GetString(Buff);
                    part = part.Replace('\0', ' ').Trim(); //Enlèvement des caractères nuls

                    builder.Append(part);

                    if (builder.Length == 0) //Déconnexion à l'initiative du serveur
                    {
                        form.Invoke(form.del_close_fromserv);
                        return;
                    }
                } while (!(builder[builder.Length-1] == '|')); //La fin du message est marquée par un |

                reponse = builder.ToString().TrimEnd('|', ' ');

                if (reponse.Contains("|")) // En cas de double écriture dans la socket
                {
                    string[] reponses = reponse.Split('|');
                    foreach(string rep in reponses)
                    {
                        Traiter(form, rep);
                    }
                }
                else
                {
                    Traiter(form, reponse);
                }
            }
        }

        /// <summary>
        /// Traitement des messages du serveur
        /// </summary>
        /// <param name="form">Formulaire principal</param>
        /// <param name="reponse">Réponse formattée du serveur</param>
        private void Traiter(Main_form form, string reponse)
        {
            string[] tab = reponse.Split(new char[] { ' ' }, 3);

            Mess message = null;

            if (tab.Length == 1)
                message = new Mess(tab[0], "", "");
            else if (tab.Length == 2)
                message = new Mess(tab[0], tab[1], "");
            else
                message = new Mess(tab[0], tab[1], tab[2]);

            //Traitement
            switch (message.Code)
            {
                case 203: //Succès
                    {
                        if (form.tmp_pseudo != null) //Succès après un changement de pseudo
                        {
                            form.mon_pseudo = form.tmp_pseudo;
                            tmp_pseudo = null;
                        }

                        break;
                    }
                case 201: //Différents codes de succès (osef)
                case 202:
                case 204:
                case 205:
                case 206:
                case 207:
                case 208:
                case 209:
                case 210:
                case 211:
                case 212:
                case 213:
                    break;
                case 300: //Réponse à la requête :who
                    {
                        form.Invoke(form.del_traiter_who, new Object[] { message.Info + " " + message.Content });
                        Envoyer(conf.GetValue("USERLISTAWAY", "COMMAND"));
                        break;
                    }
                case 301:
                    {
                        form.Invoke(form.del_traiter_who, new Object[] { "AWAY " + message.Info + " " + message.Content });
                        break;
                    }
                case 302: //Utilisateur connecté
                    {
                        form.Invoke(form.del_new_user, new Object[] { message.Info });
                        break;
                    }
                case 303: //Utilisateur déconnecté
                    {
                        form.Invoke(form.del_del_user, new Object[] { message.Info });
                        break;
                    }
                case 304: //Message public
                    {
                        form.Invoke(form.del_chat_append, new Object[] { "<" + message.Info + "> :", message.Content });
                        break;
                    }
                case 305: //Changement de nom
                    {
                        form.Invoke(form.del_pseudo_change, new Object[] { message.Info, message.Content });
                        break;
                    }
                case 306: //Message privé
                    {
                        form.Invoke(form.del_chat_append, new Object[] { "<" + message.Info + "> PRIVATE:", message.Content });
                        break;
                    }
                case 307: //On ignore la négociation des messages privés
                case 308:
                case 309:
                    break;
                case 310: //Fin AFK
                    {
                        form.Invoke(form.del_chat_append, new Object[] { "*", message.Info + " is now available" });
                        Envoyer(conf.GetValue("USERLIST", "COMMAND"));
                        break;
                    }
                case 311: //Début AFK
                    {
                        form.Invoke(form.del_chat_append, new Object[] { "*", message.Info + " is AFK" });
                        Envoyer(conf.GetValue("USERLIST", "COMMAND"));
                        break;
                    }
                case 666: //Check Alive
                    {
                        Envoyer(mon_pseudo, "/PONG");
                        break;
                    }
                default:
                    {
                        form.Invoke(form.del_error_show, new Object[] { message.Code, message.Content });
                        break;
                    }
            }
        }
    }

    public class Mess //Structuration des messages
    {
        private int code;
        private string info;
        private string content;

        public int Code
        {
            get { return code; }
        }

        public string Info
        {
            get { return info; }
        }

        public string Content
        {
            get { return content; }
        }

        public Mess(string code, string info, string content)
        {
            this.code = int.Parse(code);
            this.info = info;
            this.content = content;
        }
    }
}
