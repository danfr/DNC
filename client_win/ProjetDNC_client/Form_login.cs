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
            mf.Envoyer("", conf.GetValue("NEWNAME", "COMMAND"), pseudo_txt.Text);
            Mess reponse = mf.Recevoir(); 

            if(reponse.Code == 302) //On ignore le 302
            {
                reponse = mf.Recevoir();
            }

            if (reponse.Code == 200)
            {
                ok = true;
                mf.Lancer_ecoute(pseudo_txt.Text.Trim());
                this.Close();
            }
            else if (reponse.Code == 408)
            {
                MessageBox.Show("Pseudo incorrect !\n(" + reponse.Code + ")", "Erreur de connexion", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
            else if (reponse.Code == 400)
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
