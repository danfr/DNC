using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ProjetDNC_client
{
    public partial class Form_private : Form
    {
        Main_form mf;
        bool arret = false;

        public Form_private(Main_form main, bool stop)
        {
            InitializeComponent();
            mf = main;
            arret = stop;

            if (!stop) //Envoi de demande de session privée
            {
                this.pseudo_combo.Items.AddRange(main.clients_actifs.ToArray());
            }
            else //Arret de session privée
            {
                this.pseudo_combo.Items.AddRange(main.sessions_privees.ToArray());
                this.demand_btn.Text = "Arreter la conversation privée";
            }

            if (pseudo_combo.Items.Count == 0)
                this.demand_btn.Enabled = false;
            else
                this.pseudo_combo.SelectedIndex = 0;
        }
    }
}
