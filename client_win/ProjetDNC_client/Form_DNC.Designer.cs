﻿namespace ProjetDNC_client
{
    partial class Main_form
    {
        /// <summary>
        /// Variable nécessaire au concepteur.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Nettoyage des ressources utilisées.
        /// </summary>
        /// <param name="disposing">true si les ressources managées doivent être supprimées ; sinon, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Code généré par le Concepteur Windows Form

        /// <summary>
        /// Méthode requise pour la prise en charge du concepteur - ne modifiez pas
        /// le contenu de cette méthode avec l'éditeur de code.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Main_form));
            this.fonctionsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.transfertDeFichierToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.rechargerLesImagesMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.outilsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.changerDeNomToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.déconnexionToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.son_active = new System.Windows.Forms.ToolStripMenuItem();
            this.déconnexionToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.menuStrip = new System.Windows.Forms.MenuStrip();
            this.infoMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.users_list = new System.Windows.Forms.ListView();
            this.pubic_text = new System.Windows.Forms.TextBox();
            this.public_btn = new System.Windows.Forms.Button();
            this.private_btn = new System.Windows.Forms.Button();
            this.private_text = new System.Windows.Forms.TextBox();
            this.private_lbl = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.private_to_txt = new System.Windows.Forms.TextBox();
            this.chat_window = new System.Windows.Forms.RichTextBox();
            this.btn_img_pri = new System.Windows.Forms.Button();
            this.btn_img_pub = new System.Windows.Forms.Button();
            this.menuStrip.SuspendLayout();
            this.SuspendLayout();
            // 
            // fonctionsToolStripMenuItem
            // 
            this.fonctionsToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.transfertDeFichierToolStripMenuItem,
            this.rechargerLesImagesMenuItem});
            this.fonctionsToolStripMenuItem.Name = "fonctionsToolStripMenuItem";
            resources.ApplyResources(this.fonctionsToolStripMenuItem, "fonctionsToolStripMenuItem");
            // 
            // transfertDeFichierToolStripMenuItem
            // 
            resources.ApplyResources(this.transfertDeFichierToolStripMenuItem, "transfertDeFichierToolStripMenuItem");
            this.transfertDeFichierToolStripMenuItem.Name = "transfertDeFichierToolStripMenuItem";
            // 
            // rechargerLesImagesMenuItem
            // 
            this.rechargerLesImagesMenuItem.Name = "rechargerLesImagesMenuItem";
            resources.ApplyResources(this.rechargerLesImagesMenuItem, "rechargerLesImagesMenuItem");
            this.rechargerLesImagesMenuItem.Click += new System.EventHandler(this.rechargerLesImagesMenuItem_Click);
            // 
            // outilsToolStripMenuItem
            // 
            this.outilsToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.changerDeNomToolStripMenuItem,
            this.déconnexionToolStripMenuItem,
            this.son_active,
            this.déconnexionToolStripMenuItem1});
            this.outilsToolStripMenuItem.Name = "outilsToolStripMenuItem";
            resources.ApplyResources(this.outilsToolStripMenuItem, "outilsToolStripMenuItem");
            // 
            // changerDeNomToolStripMenuItem
            // 
            this.changerDeNomToolStripMenuItem.Name = "changerDeNomToolStripMenuItem";
            resources.ApplyResources(this.changerDeNomToolStripMenuItem, "changerDeNomToolStripMenuItem");
            this.changerDeNomToolStripMenuItem.Click += new System.EventHandler(this.changerDeNomToolStripMenuItem_Click);
            // 
            // déconnexionToolStripMenuItem
            // 
            this.déconnexionToolStripMenuItem.Name = "déconnexionToolStripMenuItem";
            resources.ApplyResources(this.déconnexionToolStripMenuItem, "déconnexionToolStripMenuItem");
            this.déconnexionToolStripMenuItem.Click += new System.EventHandler(this.déconnexionToolStripMenuItem_Click);
            // 
            // son_active
            // 
            this.son_active.Checked = true;
            this.son_active.CheckOnClick = true;
            this.son_active.CheckState = System.Windows.Forms.CheckState.Checked;
            this.son_active.Name = "son_active";
            resources.ApplyResources(this.son_active, "son_active");
            this.son_active.CheckStateChanged += new System.EventHandler(this.sonActive_CheckStateChanged);
            // 
            // déconnexionToolStripMenuItem1
            // 
            this.déconnexionToolStripMenuItem1.Name = "déconnexionToolStripMenuItem1";
            resources.ApplyResources(this.déconnexionToolStripMenuItem1, "déconnexionToolStripMenuItem1");
            this.déconnexionToolStripMenuItem1.Click += new System.EventHandler(this.déconnexionToolStripMenuItem1_Click);
            // 
            // menuStrip
            // 
            this.menuStrip.BackColor = System.Drawing.SystemColors.MenuBar;
            this.menuStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.outilsToolStripMenuItem,
            this.fonctionsToolStripMenuItem,
            this.infoMenuItem});
            resources.ApplyResources(this.menuStrip, "menuStrip");
            this.menuStrip.Name = "menuStrip";
            this.menuStrip.RenderMode = System.Windows.Forms.ToolStripRenderMode.Professional;
            // 
            // infoMenuItem
            // 
            this.infoMenuItem.Alignment = System.Windows.Forms.ToolStripItemAlignment.Right;
            this.infoMenuItem.Name = "infoMenuItem";
            resources.ApplyResources(this.infoMenuItem, "infoMenuItem");
            this.infoMenuItem.Click += new System.EventHandler(this.infoMenuItem_Click);
            // 
            // users_list
            // 
            resources.ApplyResources(this.users_list, "users_list");
            this.users_list.BackColor = System.Drawing.SystemColors.Info;
            this.users_list.MultiSelect = false;
            this.users_list.Name = "users_list";
            this.users_list.ShowGroups = false;
            this.users_list.UseCompatibleStateImageBehavior = false;
            this.users_list.View = System.Windows.Forms.View.List;
            this.users_list.ItemSelectionChanged += new System.Windows.Forms.ListViewItemSelectionChangedEventHandler(this.users_list_ItemSelectionChanged);
            // 
            // pubic_text
            // 
            resources.ApplyResources(this.pubic_text, "pubic_text");
            this.pubic_text.Name = "pubic_text";
            this.pubic_text.Enter += new System.EventHandler(this.pubic_text_Enter);
            // 
            // public_btn
            // 
            resources.ApplyResources(this.public_btn, "public_btn");
            this.public_btn.Name = "public_btn";
            this.public_btn.UseVisualStyleBackColor = true;
            this.public_btn.Click += new System.EventHandler(this.public_btn_Click);
            // 
            // private_btn
            // 
            resources.ApplyResources(this.private_btn, "private_btn");
            this.private_btn.Name = "private_btn";
            this.private_btn.UseVisualStyleBackColor = true;
            this.private_btn.Click += new System.EventHandler(this.private_btn_Click);
            // 
            // private_text
            // 
            resources.ApplyResources(this.private_text, "private_text");
            this.private_text.Name = "private_text";
            this.private_text.Enter += new System.EventHandler(this.private_text_Enter);
            // 
            // private_lbl
            // 
            resources.ApplyResources(this.private_lbl, "private_lbl");
            this.private_lbl.Name = "private_lbl";
            // 
            // label1
            // 
            resources.ApplyResources(this.label1, "label1");
            this.label1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label1.Name = "label1";
            // 
            // private_to_txt
            // 
            resources.ApplyResources(this.private_to_txt, "private_to_txt");
            this.private_to_txt.Name = "private_to_txt";
            // 
            // chat_window
            // 
            resources.ApplyResources(this.chat_window, "chat_window");
            this.chat_window.BackColor = System.Drawing.SystemColors.Window;
            this.chat_window.Name = "chat_window";
            this.chat_window.ReadOnly = true;
            this.chat_window.VScroll += new System.EventHandler(this.chat_window_VScroll);
            // 
            // btn_img_pri
            // 
            resources.ApplyResources(this.btn_img_pri, "btn_img_pri");
            this.btn_img_pri.Image = global::ProjetDNC_client.Properties.Resources.icon_image_25;
            this.btn_img_pri.Name = "btn_img_pri";
            this.btn_img_pri.UseVisualStyleBackColor = true;
            this.btn_img_pri.Click += new System.EventHandler(this.btn_img_pri_Click);
            // 
            // btn_img_pub
            // 
            resources.ApplyResources(this.btn_img_pub, "btn_img_pub");
            this.btn_img_pub.Image = global::ProjetDNC_client.Properties.Resources.icon_image_25;
            this.btn_img_pub.Name = "btn_img_pub";
            this.btn_img_pub.UseVisualStyleBackColor = true;
            this.btn_img_pub.Click += new System.EventHandler(this.btn_img_pub_Click);
            // 
            // Main_form
            // 
            resources.ApplyResources(this, "$this");
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.btn_img_pri);
            this.Controls.Add(this.btn_img_pub);
            this.Controls.Add(this.chat_window);
            this.Controls.Add(this.private_to_txt);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.private_lbl);
            this.Controls.Add(this.private_btn);
            this.Controls.Add(this.private_text);
            this.Controls.Add(this.public_btn);
            this.Controls.Add(this.pubic_text);
            this.Controls.Add(this.users_list);
            this.Controls.Add(this.menuStrip);
            this.KeyPreview = true;
            this.MainMenuStrip = this.menuStrip;
            this.Name = "Main_form";
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Show;
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Main_form_FormClosing);
            this.Shown += new System.EventHandler(this.Main_form_Shown);
            this.menuStrip.ResumeLayout(false);
            this.menuStrip.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ToolStripMenuItem fonctionsToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem outilsToolStripMenuItem;
        private System.Windows.Forms.MenuStrip menuStrip;
        private System.Windows.Forms.ToolStripMenuItem transfertDeFichierToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem changerDeNomToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem déconnexionToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem déconnexionToolStripMenuItem1;
        private System.Windows.Forms.ListView users_list;
        private System.Windows.Forms.TextBox pubic_text;
        private System.Windows.Forms.Button public_btn;
        private System.Windows.Forms.Button private_btn;
        private System.Windows.Forms.TextBox private_text;
        private System.Windows.Forms.Label private_lbl;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox private_to_txt;
        public System.Windows.Forms.RichTextBox chat_window;
        private System.Windows.Forms.ToolStripMenuItem son_active;
        private System.Windows.Forms.ToolStripMenuItem infoMenuItem;
        private System.Windows.Forms.ToolStripMenuItem rechargerLesImagesMenuItem;
        private System.Windows.Forms.Button btn_img_pub;
        private System.Windows.Forms.Button btn_img_pri;
    }
}

