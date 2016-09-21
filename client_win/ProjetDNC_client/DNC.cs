using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ProjetDNC_client
{
    public partial class Main_form : Form //Code à usage non-graphique
    {
        public string mon_pseudo;
        public string tmp_pseudo = null;
        private byte[] myBuff = new byte[512];
        private Thread t = null;
        private System.Windows.Forms.Timer timer;

        /// <summary>
        /// Envoi de la requete :who à chaque signal du timer
        /// </summary>
        private void timer_Tick(object sender, EventArgs e)
        {
            Envoyer("/userlist");
        }

        /// <summary>
        /// Envoi d'une requête DNC formattée au serveur
        /// </summary>
        /// <param name="pseudo">Pseudo de la cible</param>
        /// <param name="commande">Commande de la requête</param>
        /// <param name="contenu">Contenu de la requête</param>
        public void Envoyer(string pseudo, string commande, string contenu)
        {
            contenu = contenu.Replace('\r', ' ').Replace('\n', ' ').Trim();

            if (pseudo != null && pseudo != "")
            {
                pseudo = " " + pseudo;
            }

            if (contenu != null && contenu != "")
            {
                contenu = " " + contenu;
            }

            string mess = commande + pseudo + contenu;

            sock.Send(Encoding.UTF8.GetBytes(mess));
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
            sock.Receive(myBuff);
            string reponse = Encoding.UTF8.GetString(myBuff);
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

            Envoyer("/userlist"); //Récupération de la liste des clients connectés
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

            while (true)
            {
                byte[] Buff = new byte[512];

                //Réception du message
                sock.Receive(Buff);
                string reponse = Encoding.UTF8.GetString(Buff);
                string[] tab = reponse.Split(new char[] { ' ' }, 3);

                Mess message = null;

                if (tab.Length == 1)
                    message =  new Mess(tab[0], "", "");
                else if (tab.Length == 2)
                    message = new Mess(tab[0], tab[1], "");
                else
                    message = new Mess(tab[0], tab[1], tab[2]);

                //Traitement
                switch (message.Code)
                {
                    case 0: //Message du serveur
                    {
                        form.Invoke(form.del_chat_append, new Object[] { "*", message.Content });
                        break;
                    }
                    case 1: //Message public
                    {
                        form.Invoke(form.del_chat_append, new Object[] { "<" + message.Sender + ">", message.Content });
                        break;
                    }
                    case 10: //Message privé
                    {
                        form.Invoke(form.del_private_msg, new Object[] { "dit", message.Sender, message.Content });
                        break;
                    }
                    case 11: //Demande de conversation privée
                    {
                        form.Invoke(form.del_private_msg, new Object[] { "demande", message.Sender, "" });
                        break;
                    }
                    case 12: //Acceptation de conversation privée
                    {
                        form.Invoke(form.del_private_msg, new Object[] { "accepte", message.Sender, "" });
                        break;
                    }
                    case 13: //Refus de conversation privée
                    {
                        form.Invoke(form.del_private_msg, new Object[] { "refuse", message.Sender, "" });
                        break;
                    }
                    case 300: //Réponse à la requête :who
                    {
                        form.Invoke(form.del_traiter_who, new Object[] { message.Sender });
                        break;
                    }
                    case 19: //Fin de conversation privée
                    {
                        form.Invoke(form.del_private_msg, new Object[] { "quitte", message.Sender, "" });
                        break;
                    }
                    case 200: //Succès
                    {
                        if (form.tmp_pseudo != null) //Succès après un changement de pseudo
                        {
                            form.mon_pseudo = form.tmp_pseudo;
                            tmp_pseudo = null;
                        }

                        break;
                    }
                    case 301: //Erreur d'identification
                    {
                        form.Invoke(form.del_reg_err, new Object[] { message.Content });
                        break;
                    }
                    case 401: //Arret du serveur
                    {
                        form.Invoke(form.del_close_fromserv);
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
    }

    public class Mess //Structuration des messages
    {
        private int code;
        private string sender;
        private string content;

        public int Code
        {
            get { return code; }
        }

        public string Sender
        {
            get { return sender; }
        }

        public string Content
        {
            get { return content; }
        }

        public Mess(string code, string sender, string content)
        {
            this.code = int.Parse(code);
            this.sender = sender;
            this.content = content;
        }
    }
}
