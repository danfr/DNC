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
using System.IO;
using System.Linq;

namespace ProjetDNC_client
{
    public partial class Main_form : Form
    {
        #region Variables

        public Socket sock = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        public List<string> clients_actifs = new List<string>();
        public List<ListViewItem> liste_items = new List<ListViewItem>();
        public List<string> sessions_privees = new List<string>();
        public bool notif, afk;
        Ini conf;
        Dictionary<Color, int> colors = new Dictionary<Color, int> { { Color.Blue, 0 }, { Color.BlueViolet, 0 }, { Color.Brown, 0 }, { Color.DarkCyan, 0 }, { Color.DarkMagenta, 0 }, { Color.DarkOrange, 0 }, { Color.DarkRed, 0 }, { Color.DarkViolet, 0 }, { Color.Fuchsia, 0 }, { Color.Indigo, 0 }, { Color.Purple, 0 }, { Color.Red, 0 } };
        Dictionary<string, Color> dict_colors = new Dictionary<string, Color>(); // Couleurs associées aux pseudos <pseudo,couleur>
        Dictionary<string, string> smileys = new Dictionary<string, string>(); // Répertoire des smileys de base <raccourci clavier, chemin du fichier>
        Dictionary<string, string> images = new Dictionary<string, string>(); // Répertoire des émoticones custom <raccourci clavier (:nom_du_fichier:), chemin du fichier>
        int currentIndex = 0;
        System.Media.SoundPlayer player = new System.Media.SoundPlayer();
        bool scrollAtBottom;
        private const int WM_VSCROLL = 277;
        private const int SB_PAGEBOTTOM = 7;

        #endregion

        #region Delegates & Interfaces

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

        [DllImport("user32.dll", CharSet = CharSet.Auto)]
        private static extern int SendMessage(IntPtr hWnd, int wMsg, IntPtr wParam, IntPtr lParam);

        [DllImport("user32.dll")]
        static extern bool FlashWindow(IntPtr hwnd, bool bInvert);

        [DllImport("user32.dll", CharSet = CharSet.Auto, ExactSpelling = true)]
        private static extern IntPtr GetForegroundWindow();

        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern int GetWindowThreadProcessId(IntPtr handle, out int processId);

        #endregion

        #region Utilities

        /// <summary>
        /// Chargement des images contenues à la racine du dossier img (émoticones custom)
        /// </summary>
        private void LoadCustom()
        {
            String[] ext = new String[] { "jpg", "jpeg", "png", "bmp" };
            if (Directory.Exists("img"))
            {
                string[] myFiles = GetFilesFrom("img", ext, false);
                foreach (string file in myFiles)
                {
                    FileInfo fi = new FileInfo(file);
                    if (fi.Length < 2097152) // Taille du fichier < 2Mo
                    {
                        string nom = Path.GetFileNameWithoutExtension(fi.Name);
                        images.Add(":" + nom + ":", file);
                    }
                }
            }
            else
            {
                MessageBox.Show("Le dossier 'img' n'est pas présent dans le répertoire d'exécution du programme !", "Dossier manquant", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                this.Close();
            }
        }

        /// <summary>
        /// Récupère la liste des fichiers dans un répertoire
        /// </summary>
        /// <param name="searchFolder">Répertoire racine de la recherche</param>
        /// <param name="filters">Liste des extensions de fichier acceptées</param>
        /// <param name="isRecursive">Recherche dans les sous-dossiers ?</param>
        /// <returns>Liste des chemins de fichier correcpondants</returns>
        public static String[] GetFilesFrom(String searchFolder, String[] filters, bool isRecursive)
        {
            List<String> filesFound = new List<String>();
            var searchOption = isRecursive ? SearchOption.AllDirectories : SearchOption.TopDirectoryOnly;
            foreach (var filter in filters)
            {
                filesFound.AddRange(Directory.GetFiles(searchFolder, String.Format("*.{0}", filter), searchOption));
            }
            return filesFound.ToArray();
        }

        /// <summary>
        /// Convertit une image locale en Base64
        /// </summary>
        /// <param name="filename">Chemin de l'image</param>
        /// <returns>Une chaine encodée en Base64</returns>
        private string imageToBase64(string filename)
        {
            using (Image image = Image.FromFile(filename))
            {
                using (MemoryStream m = new MemoryStream())
                {
                    image.Save(m, image.RawFormat);
                    byte[] imageBytes = m.ToArray();

                    // Convert byte[] to Base64 String
                    string base64String = Convert.ToBase64String(imageBytes);
                    return base64String;
                }
            }
        }

        /// <summary>
        /// Convertit une chaine Base64 en fichier
        /// </summary>
        /// <param name="filename">Chemin du fichier à écrire</param>
        /// <param name="data">Chaine Base 64</param>
        private void base64ToImage(string filename, string data)
        {
            var bytes = Convert.FromBase64String(data);
            using (var imageFile = new FileStream(filename, FileMode.Create))
            {
                imageFile.Write(bytes, 0, bytes.Length);
                imageFile.Flush();
            }
        }

        /// <summary>
        /// Déplace le scroll au maximum vers le bas
        /// </summary>
        /// <param name="MyRichTextBox">RichTextBox à scroller</param>
        public static void ScrollToBottom(RichTextBox MyRichTextBox)
        {
            SendMessage(MyRichTextBox.Handle, WM_VSCROLL, (IntPtr)SB_PAGEBOTTOM, IntPtr.Zero);
        }

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

        #region Internal class ScrollInfo

        internal class Scrollinfo
        {
            public const uint ObjidVscroll = 0xFFFFFFFB;

            [DllImport("user32.dll", SetLastError = true, EntryPoint = "GetScrollBarInfo")]
            private static extern int GetScrollBarInfo(IntPtr hWnd,
                                                       uint idObject,
                                                       ref Scrollbarinfo psbi);

            internal static bool CheckBottom(RichTextBox rtb)
            {


                var info = new Scrollbarinfo();
                info.CbSize = Marshal.SizeOf(info);

                var res = GetScrollBarInfo(rtb.Handle,
                                           ObjidVscroll,
                                           ref info);

                var isAtBottom = info.XyThumbBottom > (info.RcScrollBar.Bottom - info.RcScrollBar.Top - (info.DxyLineButton * 2));
                return isAtBottom;
            }
        }

        public struct Scrollbarinfo
        {
            public int CbSize;
            public Rect RcScrollBar;
            public int DxyLineButton;
            public int XyThumbTop;
            public int XyThumbBottom;
            public int Reserved;
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 6)]
            public int[] Rgstate;
        }

        public struct Rect
        {
            public int Left;
            public int Top;
            public int Right;
            public int Bottom;
        }

        #endregion

        #endregion

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

                conf.WriteValue("MIN_SIZE", "IMAGE_PICKER", "100");

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
            afk = false;

            mon_pseudo = conf.GetValue("DEFAULT_PSEUDO", "USER");
            scrollAtBottom = true;

            //Détection du ScreenLock
            SystemEvents.SessionSwitch += new SessionSwitchEventHandler(SystemEvents_SessionSwitch);

            //Couleur des messages du serveur
            dict_colors.Add("*", Color.Green);

            //Ajout des smileys
            smileys.Add(":)", "img/Emoticons/sourire_ico.png");
            smileys.Add(":-)", "img/Emoticons/sourire_ico.png");
            smileys.Add(";)", "img/Emoticons/clin-d-oeil_ico.png");
            smileys.Add(";-)", "img/Emoticons/clin-d-oeil_ico.png");
            smileys.Add(":s", "img/Emoticons/confus_ico.png");
            smileys.Add(":D", "img/Emoticons/grand-sourire_ico.png");
            smileys.Add("XD", "img/Emoticons/mdr_ico.png");
            smileys.Add("xD", "img/Emoticons/mdr_ico.png");
            smileys.Add("B)", "img/Emoticons/like-a-boss_ico.png");
            smileys.Add(":'(", "img/Emoticons/pleure_ico.png");
            smileys.Add(":(", "img/Emoticons/serieux_ico.png");
            smileys.Add(":/", "img/Emoticons/decu_ico.png");
            smileys.Add(":p", "img/Emoticons/tire-la-langue_ico.png");
            smileys.Add(":P", "img/Emoticons/tire-la-langue_ico.png");
            smileys.Add(":o", "img/Emoticons/surpris_ico.png");
            smileys.Add(":O", "img/Emoticons/en-colere_ico.png");
            smileys.Add(":@", "img/Emoticons/en-colere_ico.png");
            smileys.Add(":faceplam:", "img/Emoticons/faceplam_ico.png");
            smileys.Add("<3", "img/Emoticons/coeur_ico.png");
            smileys.Add(":beer:", "img/Emoticons/beer_ico.png");
            smileys.Add(":cawa:", "img/Emoticons/cawa_ico.png");

            //Ajout des images présentes dans le dossier img
            LoadCustom();
        }

        #region Listeners

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
            if (t != null)
                t.Abort(); //Arret de l'écoute si le thread est lancé

            if (sock.Connected)
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

        /// <summary>
        /// Clic sur le bouton d'envoi de essage public
        /// </summary>
        private void public_btn_Click(object sender, EventArgs e)
        {
            String text = this.pubic_text.Text;

            if (text.Trim() != "")
            {
                foreach (KeyValuePair<string, string> img in images) // Détection de l'envoi d'image
                {
                    if (text.Contains(img.Key))
                    {
                        if (File.Exists(img.Value))
                            text = "<BASE64IMG>!" + Path.GetExtension(img.Value) + "!" + imageToBase64(img.Value);
                        break;
                    }
                }

                Envoyer("", "", text);
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
            afk = true;
            Envoyer(conf.GetValue("DISABLE", "COMMAND"));
            MessageBox.Show("Session en pause, cliquez sur OK pour reprendre.", "Pause", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
            Envoyer(conf.GetValue("ENABLE", "COMMAND"));
            Envoyer(conf.GetValue("USERLIST", "COMMAND"));
            afk = false;
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
        /// Action au clic sur le bouton de chat privé -> envoi du message au destinataire sélectionné
        /// </summary>
        private void private_btn_Click(object sender, EventArgs e)
        {
            if (private_to_txt.Text != "(Cliquer sur le nom)")
            {
                String text = this.private_text.Text;

                if (text.Trim() != "")
                {
                    foreach (KeyValuePair<string, string> img in images)
                    {
                        if (text.Contains(img.Key))
                        {
                            if (File.Exists(img.Value))
                                text = "<BASE64IMG>!" + Path.GetExtension(img.Value) + "!" + imageToBase64(img.Value);
                            break;
                        }
                    }
                    Envoyer(private_to_txt.Text, conf.GetValue("PM", "COMMAND"), text);
                    this.private_text.Clear();
                }
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
        /// Action au Lock de la session (mise AFK)
        /// </summary>
        void SystemEvents_SessionSwitch(object sender, SessionSwitchEventArgs e)
        {
            switch (e.Reason)
            {
                case SessionSwitchReason.SessionLock:
                    Envoyer(conf.GetValue("DISABLE", "COMMAND"));
                    timer.Stop();
                    break;
                case SessionSwitchReason.SessionUnlock:
                    Envoyer(conf.GetValue("ENABLE", "COMMAND"));
                    timer.Start();
                    Envoyer(conf.GetValue("USERLIST", "COMMAND"));
                    break;
            }
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

        /// <summary>
        /// Action au changmeent d'état du paramètre "Son Activé"
        /// </summary>
        private void sonActive_CheckStateChanged(object sender, EventArgs e)
        {
            this.notif = son_active.Checked;
        }

        /// <summary>
        /// Action au clic sur "Recharger les images"
        /// </summary>
        private void rechargerLesImagesMenuItem_Click(object sender, EventArgs e)
        {
            this.images.Clear();
            LoadCustom();
        }

        /// <summary>
        /// Action au clic sur le bouton de sélection d'image public
        /// </summary>
        private void btn_img_pub_Click(object sender, EventArgs e)
        {
            string tag = "";
            Image_picker ip = new Image_picker(images);
            DialogResult dr = ip.ShowDialog(this);

            if (dr == DialogResult.OK)
            {
                tag = ip.ReturnValue; // On récupère le tag associé à l'image sélectionnée et on l'envoie
                pubic_text.Text = tag;
                public_btn.PerformClick();
            }

            pubic_text.Focus();
        }

        /// <summary>
        /// Action au clic sur le bouton de sélection d'image privé
        /// </summary>
        private void btn_img_pri_Click(object sender, EventArgs e)
        {
            string tag = "";
            Image_picker ip = new Image_picker(images);
            DialogResult dr = ip.ShowDialog(this);

            if (dr == DialogResult.OK)
            {
                tag = ip.ReturnValue; // On récupère le tag associé à l'image sélectionnée et on l'envoie
                private_text.Text = tag;
                private_btn.PerformClick();
            }

            private_text.Focus();
        }

        /// <summary>
        /// Action au clic sur "?"
        /// </summary>
        private void infoMenuItem_Click(object sender, EventArgs e)
        {
            Informations info_form = new Informations();
            info_form.ShowDialog(this);
        }


        #endregion


        /// <summary>
        /// Ajoute le message entré en paramètre à la fenetre de chat principale
        /// </summary>
        /// <param name="from">Provenance du message</param>
        /// <param name="content">Texte du message</param>
        public void Chat_append(string from, string content)
        {
            DateTime time = DateTime.Now;
            string format = "HH:mm:ss";
            Color col;
            bool serveur = (from == "*");
            bool image = false;

            // Association pseudo/couleur
            if (dict_colors.ContainsKey(from))
            {
                col = dict_colors[from];
            }
            else
            {
                Random rnd = new Random();
                List<Color> tab_col = new List<Color>();

                //On récupère les couleurs les moins utilisées et on en choisi une au hasard
                for (int i = 0; i < 10 && tab_col.Count < 1; i++)
                {
                    Dictionary<Color, int> filtre = colors.Where(kvp => kvp.Value == i).ToDictionary(kvp => kvp.Key, kvp => kvp.Value);
                    tab_col = filtre.Keys.ToList();
                }

                col = tab_col[rnd.Next(0, tab_col.Count - 1)];
                colors[col] = colors[col] + 1;
                dict_colors.Add(from, col);
            }

            // On enregiste l'index actuel pour la recherche des smileys
            currentIndex = chat_window.TextLength;
            string filename = "";

            if (content.StartsWith("<BASE64IMG>")) // Transfert d'image = '<BASE64IMG>'!<EXTENSION>!<DATA>
            {
                image = true;
                string[] tab = content.Split('!');
                string ext = tab[1];
                filename = @"img/tmp/TURING" + ext; // Fichier temporaire
                base64ToImage(filename, tab[2]);
                content = "TURING";
            }

            // Ajout du texte formatté dans le chat
            if (chat_window.TextLength == 0)
            {
                AppendText(chat_window, "[" + time.ToString(format) + "] ", Color.LightGray);
                AppendText(chat_window, from + " ", col);

                if (serveur)
                    AppendText(chat_window, content, col);
                else
                    AppendText(chat_window, content, Color.Black);
            }
            else
            {
                chat_window.AppendText(Environment.NewLine);
                AppendText(chat_window, "[" + time.ToString(format) + "] ", Color.LightGray);
                AppendText(chat_window, from + " ", col);
                if (serveur)
                    AppendText(chat_window, content, col);
                else
                    AppendText(chat_window, content, Color.Black);
            }

            bool isAtBottom = Scrollinfo.CheckBottom(chat_window);
            // On scroll automatiquement si le scroll est déjà en bas
            if (isAtBottom)
            {
                ScrollToBottom(chat_window);
            }

            // Gestion des notifications
            if (!ApplicationIsActivated() && !serveur && !afk)
            {
                // Notif sonore
                if (notif)
                    player.Play();

                // Notif visuelle (icone qui clignote)
                IntPtr handle = this.Handle;
                FlashWindow(handle, false);
            }

            // Ajout des smileys/images
            if (image)
            {
                AddSmileys("TURING", currentIndex, filename);
                try
                {
                    File.Delete(filename); // Supression du fichier temporaire
                }
                catch (IOException)
                { }
            }
            else if (!serveur)
            {
                // AJout des smileys de base
                foreach (KeyValuePair<string, string> kv in smileys)
                {
                    AddSmileys(kv.Key, currentIndex, kv.Value);
                }
            }

            // On scroll automatiquement si le scroll est déjà en bas
            if (isAtBottom)
            {
                ScrollToBottom(chat_window);
            }
        }


        /// <summary>
        /// Ajout d'un texte coloré au chat
        /// </summary>
        /// <param name="box">Fenêtre de chat</param>
        /// <param name="text">Texte à ajouter</param>
        /// <param name="color">Couleur du texte</param>
        public void AppendText(RichTextBox box, string text, Color color)
        {
            box.SelectionStart = box.TextLength;
            box.SelectionLength = 0;

            box.SelectionColor = color;
            box.AppendText(text);
            box.SelectionColor = box.ForeColor;
        }

        /// <summary>
        /// Remplace un texte par un smiley/image dans le chat
        /// </summary>
        /// <param name="word">Texte à remplacer</param>
        /// <param name="startIndex">Début de la recherche</param>
        /// <param name="filename">Chein du fichier à ajouter</param>
        public void AddSmileys(string word, int startIndex, string filename)
        {
            if (word == string.Empty)
                return;

            int s_start = chat_window.SelectionStart, index;

            while ((index = chat_window.Text.IndexOf(word, startIndex)) != -1)
            {
                chat_window.Select(index, word.Length);
                Image_RTF img = new Image_RTF(this);
                img.addImage(filename);
            }

            chat_window.SelectionStart = s_start;
            chat_window.SelectionLength = 0;
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
                if (cur.Text == from)
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

            if (!content.Contains("AWAY")) // Gestion du retour de /userlistaway
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
                    else if (cli == mon_pseudo)
                    {
                        cur = new ListViewItem(cli);
                        cur.Font = f;
                        cur.BackColor = Color.LightGreen;
                        liste_items.Add(cur);
                    }
                }
            }
            else // Gestion du retour de /userlist
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


            if (res == DialogResult.Yes) // Séquence de reconnexion au serveur
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

                // Fermeture de l'application
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

    }

}
