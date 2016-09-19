using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ProjetDNC_client
{
    public partial class Form_login : Form
    {
        private Main_form mf;
        private bool ok = false;

        public Form_login(Main_form main_form)
        {
            InitializeComponent();
            this.mf = main_form;
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
            mf.Envoyer("", "pseudo", pseudo_txt.Text);
            Mess reponse = mf.Recevoir();

            if (reponse.Code == 200)
            {
                ok = true;
                mf.Lancer_ecoute(pseudo_txt.Text.Trim());
                this.Close();
            }
            else if (reponse.Code == 301)
            {
                MessageBox.Show("Pseudo incorrect !\n(" + reponse.Content + ")", "Erreur de connexion", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                mf.Recevoir(); //Vidage du buffer
            }
        }
    }
}
