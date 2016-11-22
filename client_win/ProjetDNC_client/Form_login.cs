using System;
using System.Windows.Forms;

namespace ProjetDNC_client
{
    public partial class Form_login : Form
    {
        private Main_form mf;
        private bool ok = false;
        Ini conf;

        public Form_login(Main_form main_form)
        {
            InitializeComponent();
            this.mf = main_form;
            conf = new Ini("DNC_client.ini");
            pseudo_txt.Text = conf.GetValue("DEFAULT_PSEUDO", "USER");
        }

        /// <summary>
        /// Fonction exécutée après la fermeture du formulaire
        /// </summary>
        private void Form_login_FormClosed(object sender, FormClosedEventArgs e)
        {
            if (!ok)
                Application.Exit(); //Si l'utilisateur ne veut pas entrer de pseudo, on ferme l'application
        }

        /// <summary>
        /// Au clic sur le bouton -> Envoi de la requete d'authentification et attente d'une réponse
        /// </summary>
        private void connexion_btn_Click(object sender, EventArgs e)
        {
            Connexion();
        }

        public void Connexion()
        {
            Connexion(pseudo_txt.Text);
        }

        /// <summary>
        /// Envoie une demande de connexion au serveur avec le pseudo demandé
        /// </summary>
        /// <param name="pseudo">Pseudo demandé au serveur</param>
        public void Connexion(string pseudo)
        {
            mf.Envoyer("", conf.GetValue("NEWNAME", "COMMAND"), pseudo);
            Mess reponse = mf.Recevoir();

            if (reponse.Code == 302) //On ignore le 302
            {
                reponse = mf.Recevoir();
            }

            if (reponse.Code == 200) // Identification OK
            {
                ok = true;
                mf.Lancer_ecoute(pseudo.Trim());
                this.Close();
            }
            else if (reponse.Code == 408) // Erreur pseudo incorrect
            {
                MessageBox.Show("Pseudo incorrect !\n(" + reponse.Code + ")", "Erreur de connexion", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
            else if (reponse.Code == 400) // Erreur pseudo déjà utilisé
            {
                MessageBox.Show("Pseudo déjà utilisé !\n(" + reponse.Code + ")", "Erreur de connexion", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
            else
            {
                MessageBox.Show("Erreur inconnue !\n(" + reponse.Code + ")", "Erreur de connexion", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
