using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace ProjetDNC_client
{
    public partial class Main_form : Form
    {
        public Socket sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        public List<string> clients_actifs = new List<string>();
        public List<string> sessions_privees = new List<string>();

        //Fonction déléguée d'ajout dans le chat
        public delegate void chat_append(string from, string contenu);
        public chat_append del_chat_append;

        //Fonction déléguée d'affchage de l'erreur de pseudo
        public delegate void reg_err(string contenu);
        public reg_err del_reg_err;

        //Fonction déléguée de traitement de la réponse à :who
        public delegate void traiter_who(string contenu);
        public traiter_who del_traiter_who;

        //Fonction déléguée de traitement du signal d'arret du serveur
        public delegate void close_fromserv();
        public close_fromserv del_close_fromserv;

        //Fonction déléguée de traitement des signaux privés
        public delegate void private_msg(string type, string sender, string content);
        public private_msg del_private_msg;

        //Fonction déléguée d'affichage d'erreurs reçues inopinément
        public delegate void error_show(int code, string contenu);
        public error_show del_error_show;

        /// <summary>
        /// Initialistation du formulaire principal
        /// </summary>
        public Main_form()
        {
            InitializeComponent();

            //Instanciation des méthodes déléguées
            del_chat_append = new chat_append(Chat_append);
            del_reg_err = new reg_err(Reg_err);
            del_traiter_who = new traiter_who(Traiter_who);
            del_close_fromserv = new close_fromserv(Close_fromserv);
            del_private_msg = new private_msg(Private_msg);
            del_error_show = new error_show(Error_show);
        }

        /// <summary>
        /// Fonction exécutée une fois le formulaire principal affiché (et donc entièrement chargé)
        /// </summary>
        private void Main_form_Shown(object sender, EventArgs e)
        {
            try //Connexion au seveur
            {
                string line;
                string adresse = "";
                string port = "";

                // Lecture du fichier DNC_client.ini
                System.IO.StreamReader file = new System.IO.StreamReader("DNC_client.ini");
                while ((line = file.ReadLine()) != null)
                {
                    line = line.ToUpper();
                    if (line.Contains("SERVER_IP"))
                    {
                        string[] tab = line.Split('=');
                        adresse = tab[1];
                    }
                    else if (line.Contains("SERVER_PORT"))
                    {
                        string[] tab = line.Split('=');
                        port = tab[1];
                    }
                }

                file.Close();

                //IPHostEntry ipHostInfo = Dns.GetHostEntry("mass-cara2.univ-tlse2.fr");
                IPAddress adr = IPAddress.Parse(adresse); //ipHostInfo.AddressList[0]; //ou 
                sock.Connect(adr, int.Parse(port));

                //Lancement de la boite de dialogue de connexion
                Form_login fl = new Form_login(this);

                fl.ShowDialog(this);
            }
            catch (SocketException err) //Echec de connexion
            {
                MessageBox.Show("Connexion au serveur impossible !\n(" + err.Message + ")", "Erreur de connexion", MessageBoxButtons.OK, MessageBoxIcon.Error);
                Application.Exit();
            }
            catch (System.IO.IOException) //Echec d'ouverture du fichier de configuration
            {
                MessageBox.Show("Le fichier de configuration DNC_client.ini est introuvable !", "Erreur de connexion", MessageBoxButtons.OK, MessageBoxIcon.Error);
                Application.Exit();
            }
            catch (FormatException) //Echec de conversion du numéro de port en int.
            {
                MessageBox.Show("La lecture du fichier de configuration DNC_client.ini à échoué, peut être est-il mal formé !", "Erreur de connexion", MessageBoxButtons.OK, MessageBoxIcon.Error);
                Application.Exit();
            }
        }

        /// <summary>
        /// Fonction exécutée lors de la fermeture du formulaire principal
        /// </summary>
        private void Main_form_FormClosing(object sender, FormClosingEventArgs e)
        {
            if(t != null)
                t.Abort(); //Arret de l'écoute si le thread est lancé

            if(sock.Connected)
                Envoyer("/quit"); //Envoi de la commande de déconnexion

            Thread.Sleep(1000); //Attente du traitement des requetes par le serveur

            sock.Close(); //Fermeture le la socket client
        }

        /// <summary>
        /// Définit le bouton de submit lors du focus de la zone de texte publique
        /// </summary>
        private void pubic_text_Enter(object sender, EventArgs e)
        {
            this.AcceptButton = this.public_btn;
        }

        /// <summary>
        /// Définit le bouton de submit lors du focus de la zone de texte privee
        /// </summary>
        private void private_text_Enter(object sender, EventArgs e)
        {
            this.AcceptButton = this.private_btn;
        }

        private void public_btn_Click(object sender, EventArgs e)
        {
            if (this.pubic_text.Text.Trim() != "")
            {
                Envoyer("", "", this.pubic_text.Text);
                this.pubic_text.Clear();
            }
        }

        /// <summary>
        /// Action au clic sur "Quitter"
        /// </summary>
        private void déconnexionToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        /// <summary>
        /// Action au clic sur "Pause"
        /// </summary>
        private void déconnexionToolStripMenuItem_Click(object sender, EventArgs e)
        {
            timer.Stop(); //Arret des requetes automatiques
            Envoyer("/disable");
            MessageBox.Show("Session en pause, cliquez sur OK pour reprendre.", "Pause", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
            Envoyer("/enable");
            Envoyer("/userlist");
            timer.Start();
        }


        /// <summary>
        /// Action au clic sur "Changer de nom..."
        /// </summary>
        private void changerDeNomToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form_nickname fn = new Form_nickname(this);
            fn.ShowDialog(this);
        }

        /// <summary>
        /// Action au clic sur "Conversation privée..."
        /// </summary>
        private void conversationPrivéeToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form_private fp = new Form_private(this, false);
            fp.ShowDialog(this);
        }

        /// <summary>
        /// Action au cli sur le bouton de chat privé -> envoi du message au destinataire sélectionné
        /// </summary>
        private void private_btn_Click(object sender, EventArgs e)
        {
            if (this.private_text.Text.Trim() != "")
            {
                Envoyer(private_combo.SelectedItem.ToString(), "/pm", private_text.Text);
                this.private_text.Clear();
            }
        }

        /// <summary>
        /// Action au clic sur "Arrêt de conversation privée..."
        /// </summary>
        private void arrêtDeConversationPrivéeToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Form_private fp = new Form_private(this, true);
            fp.ShowDialog(this);
        }

        /// <summary>
        /// Ajoute le message entré en paramètre à la fenetre de chat principale
        /// </summary>
        /// <param name="from">Provenance du message</param>
        /// <param name="content">Texte du message</param>
        public void Chat_append(string from, string content)
        {
            chat_window.AppendText(from + "  " + content);
        }

        /// <summary>
        /// Affichage d'une erreur en cas de mauvais pseudo saisi dans la commande :nick
        /// </summary>
        /// <param name="content">Message du serveur</param>
        public void Reg_err(string content)
        {
            MessageBox.Show("Pseudo incorrect !\n(" + content + ")", "Erreur d'identification", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }

        /// <summary>
        /// Traitement de la réponse à la command :who et affichage dans la liste des clients
        /// </summary>
        /// <param name="content">Réponse du serveur</param>
        public void Traiter_who(string content)
        {
            content = content.Replace('\0', ' ').Trim();
            string[] tab = content.Split(' ');
            users_list.Items.Clear();
            clients_actifs.Clear();

            ListViewItem cur = users_list.Items.Add(mon_pseudo);
            cur.BackColor = Color.LightGreen;

            foreach (string cli in tab)
            {
                if (cli != mon_pseudo)
                { 
                    clients_actifs.Add(cli);
                    users_list.Items.Add(cli);
                }
            }
        }

        /// <summary>
        /// Fermeture du chat a l'initiative du serveur
        /// </summary>
        private void Close_fromserv()
        {
            if (t != null)
            {
                t.Abort();
                t = null;
            }

            if (sock.Connected)
                Envoyer("quit");

            MessageBox.Show("Le serveur est en cours d'arret...", "Arret du serveur", MessageBoxButtons.OK, MessageBoxIcon.Warning);

            this.Close();
        }

        /// <summary>
        /// Traitement des requetes privées reçues et leurs conséquences graphiques
        /// </summary>
        /// <param name="type">Type de la requete reçue</param>
        /// <param name="sender">Nom de l'envoyeur</param>
        /// <param name="content">Contenu de la requete</param>
        private void Private_msg(string type, string sender, string content)
        {
            switch (type)
            {
                case "dit":
                    {
                        Chat_append("PRIVÉ - <" + sender + ">", content);
                        break;
                    }
                case "demande":
                    {
                        DialogResult res = MessageBox.Show(sender + " voudrait engager une conversation privée avec vous. Acceptez-vous ?", "Demande privée", MessageBoxButtons.YesNo, MessageBoxIcon.Information);

                        if (res == DialogResult.Yes)
                        {
                            Envoyer(sender, "accept");
                            sessions_privees.Add(sender);
                            this.private_combo.Items.Add(sender);
                            this.private_text.Visible = true;
                            this.private_lbl.Visible = true;
                            this.private_btn.Visible = true;
                            this.private_combo.Visible = true;
                            this.private_combo.SelectedIndex = 0;
                            this.arrêtDeConversationPrivéeToolStripMenuItem.Enabled = true;
                        }
                        else
                        {
                            Envoyer(sender, "decline");
                        }

                        break;
                    }
                case "accepte":
                    {
                        sessions_privees.Add(sender);
                        this.private_combo.Items.Add(sender);
                        this.private_text.Visible = true;
                        this.private_btn.Visible = true;
                        this.private_lbl.Visible = true;
                        this.private_combo.Visible = true;
                        this.private_combo.SelectedIndex = 0;
                        Chat_append("*", sender + " a acctepté une conversation privée avec vous.\r\n");
                        this.arrêtDeConversationPrivéeToolStripMenuItem.Enabled = true;

                        break;
                    }
                case "refuse":
                    {
                        Chat_append("*", sender + " a refusé d'ouvrir une conversation privée avec vous.\r\n");
                        break;
                    }
                case "quitte":
                    {
                        sessions_privees.Remove(sender);
                        this.private_combo.Items.Remove(sender);
                        if (private_combo.Items.Count == 0)
                        {
                            this.private_text.Visible = false;
                            this.private_text.Clear();
                            this.private_lbl.Visible = false;
                            this.private_btn.Visible = false;
                            this.private_combo.Visible = false;
                            this.arrêtDeConversationPrivéeToolStripMenuItem.Enabled = false;
                        }
                        else
                            this.private_combo.SelectedIndex = 0;

                        Chat_append("*", sender + " a quitté la conversation privée avec vous.\r\n");
                        break;
                    }
            }
        }

        /// <summary>
        /// Affichage des erreurs inconnues
        /// </summary>
        private void Error_show(int code, string content)
        {
            MessageBox.Show(code + " -> " + content, "Erreur inattendue", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }

        /// <summary>
        /// Gère les conséquences graphiques de l'arret d'une session privée
        /// </summary>
        /// <param name="pseudo">Utilisateur avec qui la session se termine</param>
        public void Fin_conv(string pseudo)
        {
            this.sessions_privees.Remove(pseudo);
            this.private_combo.Items.Remove(pseudo);
            if (private_combo.Items.Count == 0)
            {
                this.private_text.Visible = false;
                this.private_text.Clear();
                this.private_lbl.Visible = false;
                this.private_btn.Visible = false;
                this.private_combo.Visible = false;
                this.arrêtDeConversationPrivéeToolStripMenuItem.Enabled = false;
            }
            else
                this.private_combo.SelectedIndex = 0;
        }
    }
}
