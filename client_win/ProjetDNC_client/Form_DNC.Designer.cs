namespace ProjetDNC_client
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
            this.conversationPrivéeToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.arrêtDeConversationPrivéeToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.transfertDeFichierToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.outilsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.changerDeNomToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.déconnexionToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.déconnexionToolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.menuStrip = new System.Windows.Forms.MenuStrip();
            this.chat_window = new System.Windows.Forms.TextBox();
            this.users_list = new System.Windows.Forms.ListView();
            this.pubic_text = new System.Windows.Forms.TextBox();
            this.public_btn = new System.Windows.Forms.Button();
            this.private_btn = new System.Windows.Forms.Button();
            this.private_text = new System.Windows.Forms.TextBox();
            this.private_lbl = new System.Windows.Forms.Label();
            this.private_combo = new System.Windows.Forms.ComboBox();
            this.menuStrip.SuspendLayout();
            this.SuspendLayout();
            // 
            // fonctionsToolStripMenuItem
            // 
            this.fonctionsToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.conversationPrivéeToolStripMenuItem,
            this.arrêtDeConversationPrivéeToolStripMenuItem,
            this.transfertDeFichierToolStripMenuItem});
            this.fonctionsToolStripMenuItem.Name = "fonctionsToolStripMenuItem";
            resources.ApplyResources(this.fonctionsToolStripMenuItem, "fonctionsToolStripMenuItem");
            // 
            // conversationPrivéeToolStripMenuItem
            // 
            this.conversationPrivéeToolStripMenuItem.Name = "conversationPrivéeToolStripMenuItem";
            resources.ApplyResources(this.conversationPrivéeToolStripMenuItem, "conversationPrivéeToolStripMenuItem");
            this.conversationPrivéeToolStripMenuItem.Click += new System.EventHandler(this.conversationPrivéeToolStripMenuItem_Click);
            // 
            // arrêtDeConversationPrivéeToolStripMenuItem
            // 
            resources.ApplyResources(this.arrêtDeConversationPrivéeToolStripMenuItem, "arrêtDeConversationPrivéeToolStripMenuItem");
            this.arrêtDeConversationPrivéeToolStripMenuItem.Name = "arrêtDeConversationPrivéeToolStripMenuItem";
            this.arrêtDeConversationPrivéeToolStripMenuItem.Click += new System.EventHandler(this.arrêtDeConversationPrivéeToolStripMenuItem_Click);
            // 
            // transfertDeFichierToolStripMenuItem
            // 
            resources.ApplyResources(this.transfertDeFichierToolStripMenuItem, "transfertDeFichierToolStripMenuItem");
            this.transfertDeFichierToolStripMenuItem.Name = "transfertDeFichierToolStripMenuItem";
            // 
            // outilsToolStripMenuItem
            // 
            this.outilsToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.changerDeNomToolStripMenuItem,
            this.déconnexionToolStripMenuItem,
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
            this.fonctionsToolStripMenuItem});
            resources.ApplyResources(this.menuStrip, "menuStrip");
            this.menuStrip.Name = "menuStrip";
            this.menuStrip.RenderMode = System.Windows.Forms.ToolStripRenderMode.Professional;
            // 
            // chat_window
            // 
            resources.ApplyResources(this.chat_window, "chat_window");
            this.chat_window.BackColor = System.Drawing.SystemColors.InactiveBorder;
            this.chat_window.Name = "chat_window";
            this.chat_window.ReadOnly = true;
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
            // private_combo
            // 
            resources.ApplyResources(this.private_combo, "private_combo");
            this.private_combo.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.private_combo.FormattingEnabled = true;
            this.private_combo.Name = "private_combo";
            // 
            // Main_form
            // 
            resources.ApplyResources(this, "$this");
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.private_combo);
            this.Controls.Add(this.private_lbl);
            this.Controls.Add(this.private_btn);
            this.Controls.Add(this.private_text);
            this.Controls.Add(this.public_btn);
            this.Controls.Add(this.pubic_text);
            this.Controls.Add(this.users_list);
            this.Controls.Add(this.chat_window);
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
        private System.Windows.Forms.ToolStripMenuItem conversationPrivéeToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem arrêtDeConversationPrivéeToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem transfertDeFichierToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem changerDeNomToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem déconnexionToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem déconnexionToolStripMenuItem1;
        private System.Windows.Forms.TextBox chat_window;
        private System.Windows.Forms.ListView users_list;
        private System.Windows.Forms.TextBox pubic_text;
        private System.Windows.Forms.Button public_btn;
        private System.Windows.Forms.Button private_btn;
        private System.Windows.Forms.TextBox private_text;
        private System.Windows.Forms.Label private_lbl;
        private System.Windows.Forms.ComboBox private_combo;

    }
}

