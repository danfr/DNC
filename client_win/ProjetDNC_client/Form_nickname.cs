﻿using System;
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
    public partial class Form_nickname : Form
    {
        Main_form mf;
        Ini conf;

        public Form_nickname(Main_form main)
        {
            InitializeComponent();
            this.mf = main;
            conf = new Ini("DNC_client.ini");
        }

        /// <summary>
        /// Action au clic sur le bouton
        /// </summary>
        private void change_btn_Click(object sender, EventArgs e)
        {
            mf.tmp_pseudo = pseudo_txt.Text.Trim();
            mf.Envoyer("", conf.GetValue("USERNAME", "COMMAND"), pseudo_txt.Text.Trim());
            this.Close();
        }
    }
}
