using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Runtime.InteropServices;
using System.Diagnostics;
using Microsoft.Win32;

namespace ProjetDNC_client
{
    public partial class Main_form : Form
    {
        public Socket sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        public List<string> clients_actifs = new List<string>();
        public List<ListViewItem> liste_items = new List<ListViewItem>();
        public List<string> sessions_privees = new List<string>();
        public bool notif;
        Ini conf;

        //Fonction déléguée d'ajout dans le chat
        public delegate void chat_append(string from, string contenu);
        public chat_append del_chat_append;

        //Fonction déléguée d'ajout d'un user dans le chat
        public delegate void new_user(string from);
        public new_user del_new_user;

        //Fonction déléguée de supressiond'un user dans le chat
        public delegate void del_user(string from);
        public del_user del_del_user;

        //Fonction déléguée de supressiond'un user dans le chat
        public delegate void pseudo_change(string ancien, string nouveau);
        public pseudo_change del_pseudo_change;

        //Fonction déléguée d'affchage de l'erreur de pseudo
        public delegate void reg_err(string contenu);
        public reg_err del_reg_err;

        //Fonction déléguée de traitement de la réponse à :who
        public delegate void traiter_who(string contenu);
        public traiter_who del_traiter_who;

        //Fonction déléguée de traitement du signal d'arret du serveur
        public delegate void close_fromserv();
        public close_fromserv del_close_fromserv;

        //Fonction déléguée d'affichage d'erreurs reçues inopinément
        public delegate void error_show(int code, string contenu);
        public error_show del_error_show;

        System.Media.SoundPlayer player = new System.Media.SoundPlayer();

        /// <summary>
        /// Initialistation du formulaire principal
        /// </summary>
        public Main_form()
        {
            //Création du fichier ini si nécessaire
            conf = new Ini("DNC_client.ini");
            if (conf.GetSections().Length == 0)
            {
                conf.WriteValue("IP", "SERVER", "127.0.0.1");
                conf.WriteValue("PORT", "SERVER", "2222");

                conf.WriteValue("DEFAULT_PSEUDO", "USER", "Bob");
                conf.WriteValue("SOUND_NOTIF", "USER", "1");

                conf.WriteValue("USERNAME", "COMMAND", "/name");
                conf.WriteValue("NEWNAME", "COMMAND", "/newname");
                conf.WriteValue("USERLIST", "COMMAND", "/userlist");
                conf.WriteValue("USERLISTAWAY", "COMMAND", "/userlistaway");
                conf.WriteValue("ENABLE", "COMMAND", "/enable");
                conf.WriteValue("DISABLE", "COMMAND", "/disable");
                conf.WriteValue("QUIT", "COMMAND", "/quit");
                conf.WriteValue("ASKPM", "COMMAND", "/askpm");
                conf.WriteValue("ACCEPTPM", "COMMAND", "/acceptpm");
                conf.WriteValue("REJECTPM", "COMMAND", "/rejectpm");
                conf.WriteValue("PM", "COMMAND", "/pm");
                conf.WriteValue("PMFILE", "COMMAND", "/pmfile");
                conf.WriteValue("ACCEPTFILE", "COMMAND", "/acceptfile");
                conf.WriteValue("REJECTFILE", "COMMAND", "/rejectfile");

                conf.Save();
            }

            InitializeComponent();

            //Instanciation des méthodes déléguées
            del_chat_append = new chat_append(Chat_append);
            del_new_user = new new_user(New_user);
            del_del_user = new del_user(Del_user);
            del_pseudo_change = new pseudo_change(Pseudo_change);
            del_reg_err = new reg_err(Reg_err);
            del_traiter_who = new traiter_who(Traiter_who);
            del_close_fromserv = new close_fromserv(Close_fromserv);
            del_error_show = new error_show(Error_show);

            //Initialisation des notifications
            player.Stream = Properties.Resources.notif;
            notif = (conf.GetValue("SOUND_NOTIF", "USER") == "1");
            son_active.Checked = notif;

            mon_pseudo = conf.GetValue("DEFAULT_PSEUDO", "USER");

            //Détection du ScreenLock
            SystemEvents.SessionSwitch += new SessionSwitchEventHandler(SystemEvents_SessionSwitch);
        }

        /// <summary>
        /// Fonction exécutée une fois le formulaire principal affiché (et donc entièrement chargé)
        /// </summary>
        private void Main_form_Shown(object sender, EventArgs e)
        {
            try //Connexion au seveur
            {
                string adresse = "";
                string port = "";

                // Lecture du fichier DNC_client.ini
                adresse = conf.GetValue("IP", "SERVER");
                port = conf.GetValue("PORT", "SERVER");

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
                Envoyer(conf.GetValue("QUIT", "COMMAND")); //Envoi de la commande de déconnexion

            Thread.Sleep(1000); //Attente du traitement des requetes par le serveur

            if (sock.Connected)
                sock.Close(); //Fermeture le la socket client

            // Sauvegarde de la conf actuelle
            conf.WriteValue("DEFAULT_PSEUDO", "USER", this.mon_pseudo);
            conf.WriteValue("SOUND_NOTIF", "USER", (this.notif) ? "1" : "0");
            conf.Save();
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
            Envoyer(conf.GetValue("DISABLE", "COMMAND"));
            MessageBox.Show("Session en pause, cliquez sur OK pour reprendre.", "Pause", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
            Envoyer(conf.GetValue("ENABLE", "COMMAND"));
            Envoyer(conf.GetValue("USERLIST", "COMMAND"));
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
                Envoyer(private_to_txt.Text, conf.GetValue("PM", "COMMAND"), private_text.Text);
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

        [DllImport("user32.dll", CharSet = CharSet.Auto, ExactSpelling = true)]
        private static extern IntPtr GetForegroundWindow();
        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern int GetWindowThreadProcessId(IntPtr handle, out int processId);
        /// <summary>Returns true if the current application has focus, false otherwise</summary>
        public static bool ApplicationIsActivated()
        {
            var activatedHandle = GetForegroundWindow();
            if (activatedHandle == IntPtr.Zero)
            {
                return false;       // No window is currently activated
            }

            var procId = Process.GetCurrentProcess().Id;
            int activeProcId;
            GetWindowThreadProcessId(activatedHandle, out activeProcId);

            return activeProcId == procId;
        }

        /// <summary>
        /// Action au Lock de la session (mise AFK)
        /// </summary>
        void SystemEvents_SessionSwitch(object sender, SessionSwitchEventArgs e)
        {
            switch (e.Reason)
            {
                case SessionSwitchReason.SessionLock:
                    Envoyer(conf.GetValue("DISABLE", "COMMAND"));
                    break;
                case SessionSwitchReason.SessionUnlock:
                    Envoyer(conf.GetValue("ENABLE", "COMMAND"));
                    break;
            }
        }



        [DllImport("user32.dll")]
        static extern bool FlashWindow(IntPtr hwnd, bool bInvert);
        /// <summary>
        /// Ajoute le message entré en paramètre à la fenetre de chat principale
        /// </summary>
        /// <param name="from">Provenance du message</param>
        /// <param name="content">Texte du message</param>
        public void Chat_append(string from, string content)
        {
            DateTime time = DateTime.Now;
            string format = "HH:mm:ss";
            if(chat_window.TextLength == 0)
                chat_window.AppendText("[" + time.ToString(format) + "] " + from + "  " + content);
            else
                chat_window.AppendText("\r\n" + "[" + time.ToString(format) + "] " + from + "  " + content);

            if (!ApplicationIsActivated())
            {
                // Notif sonore
                if(notif)
                    player.Play();

                // Notif visuelle (icone qui clignote)
                IntPtr handle = this.Handle;
                FlashWindow(handle, false);
            }

            chat_window.ScrollToCaret();
        }

        /// <summary>
        /// Gère l'ajout d'un nouvel utilisateur
        /// </summary>
        /// <param name="from">nouvel utilisateur</param>
        public void New_user(string from)
        {
            Envoyer(conf.GetValue("USERLIST", "COMMAND"));
            Chat_append("*", from + " joined the chat");
        }

        /// <summary>
        /// Gère la supression d'un utilisateur
        /// </summary>
        /// <param name="from">utilisateur à supprimer</param>
        public void Del_user(string from)
        {
            ListViewItem sup = null;
            foreach (ListViewItem cur in users_list.Items)
            {
                if(cur.Text == from)
                {
                    sup = cur;
                    break;
                }
            }

            Envoyer(conf.GetValue("USERLIST", "COMMAND"));

            Chat_append("*", from + " left the chat");
        }

        /// <summary>
        /// Gère le changement de nom d'un user
        /// </summary>
        /// <param name="ancien">utilisateur à modiifer</param>
        /// /// <param name="nouveau">nouveau nom</param>
        public void Pseudo_change(string ancien, string nouveau)
        {
            ListViewItem sup = null;
            foreach (ListViewItem lvi in users_list.Items)
            {
                if (lvi.Text == ancien)
                {
                    sup = lvi;
                    break;
                }
            }

            Envoyer(conf.GetValue("USERLIST", "COMMAND"));


            Chat_append("*", ancien + " is now known as " + nouveau);
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
            string[] tab = content.Split(' ');

            if (!content.Contains("AWAY"))
            {
                liste_items.Clear();

                ListViewItem cur = null;
                Font f = new Font(FontFamily.GenericSansSerif, 14.0f, FontStyle.Bold, GraphicsUnit.Pixel);

                foreach (string cli in tab)
                {
                    if (cli != mon_pseudo)
                    {
                        clients_actifs.Add(cli);
                        cur = new ListViewItem(cli);
                        cur.Font = f;
                        liste_items.Add(cur);
                    }
                    else if(cli == mon_pseudo)
                    {
                        cur = new ListViewItem(cli);
                        cur.Font = f;
                        cur.BackColor = Color.LightGreen;
                        liste_items.Add(cur);
                    }
                }
            }
            else
            {
                ListViewItem cur = null;
                Font f = new Font(FontFamily.GenericSansSerif, 14.0f, FontStyle.Italic, GraphicsUnit.Pixel);

                //Ajout des utilisateurs AWAY
                foreach (string cli in tab)
                {
                    if (cli != "AWAY")
                    {
                        if (cli != mon_pseudo)
                        {
                            clients_actifs.Remove(cli);

                            cur = new ListViewItem(cli);
                            cur.Font = f;
                            liste_items.Add(cur);
                        }
                        else
                        {
                            cur = new ListViewItem(cli);
                            cur.Font = f;
                            cur.BackColor = Color.LightGreen;
                            liste_items.Add(cur);
                        }
                    }
                }

                users_list.Items.Clear();
                users_list.Items.AddRange(liste_items.ToArray());
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
                sock.Close();

            DialogResult res = MessageBox.Show("Vous avez été déconnecté du serveur !\nVoulez vous tenter de vous reconnecter ?", "Le serveur ne répond pas", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
            

            if(res == DialogResult.Yes)
            {
                bool ok = false;
                do
                {
                    try
                    {
                        string adresse = "";
                        string port = "";

                        // Lecture du fichier DNC_client.ini
                        adresse = conf.GetValue("IP", "SERVER");
                        port = conf.GetValue("PORT", "SERVER");

                        IPAddress adr = IPAddress.Parse(adresse);
                        this.sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
                        sock.Connect(adr, int.Parse(port));

                        ok = true;
                    }
                    catch (SocketException err) //Echec de connexion
                    {
                        MessageBox.Show("Connexion au serveur impossible !\n(" + err.Message + ")", "Erreur de connexion", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        res = MessageBox.Show("La connexion au serveur n'a pas été rétablie !\nVoulez vous tenter de vous reconnecter ?", "Le serveur ne répond pas", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        ok = (res == DialogResult.No);
                    }
                    catch (System.IO.IOException) //Echec d'ouverture du fichier de configuration
                    {
                        MessageBox.Show("Le fichier de configuration DNC_client.ini est introuvable !", "Erreur de connexion", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        res = MessageBox.Show("La connexion au serveur n'a pas été rétablie !\nVoulez vous tenter de vous reconnecter ?", "Le serveur ne répond pas", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        ok = (res == DialogResult.No);
                    }
                    catch (FormatException) //Echec de conversion du numéro de port en int.
                    {
                        MessageBox.Show("La lecture du fichier de configuration DNC_client.ini à échoué, peut être est-il mal formé !", "Erreur de connexion", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        res = MessageBox.Show("La connexion au serveur n'a pas été rétablie !\nVoulez vous tenter de vous reconnecter ?", "Le serveur ne répond pas", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
                        ok = (res == DialogResult.No);
                    }
                } while (!ok);

                Form_login fl = new Form_login(this);
                fl.Connexion(this.mon_pseudo);
            }
            else
                this.Close();
        }

        /// <summary>
        /// Affichage des erreurs inconnues
        /// </summary>
        private void Error_show(int code, string content)
        {
            MessageBox.Show(code + " -> " + content, "Erreur inattendue", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }


        /// <summary>
        /// Sélection d'un item dans la liste
        /// </summary>
        private void users_list_ItemSelectionChanged(object sender, ListViewItemSelectionChangedEventArgs e)
        {
            ListView lv = (ListView)sender;
            if (lv.SelectedItems.Count > 0)
            {
                ListViewItem lvi = lv.SelectedItems[0];

                if (lvi.BackColor != Color.LightGreen)
                    private_to_txt.Text = lvi.Text;
            }
            else
                private_to_txt.Text = "(Cliquer sur le nom)";
        }

        private void sonActive_CheckStateChanged(object sender, EventArgs e)
        {
            this.notif = son_active.Checked;
        }
    }
}
