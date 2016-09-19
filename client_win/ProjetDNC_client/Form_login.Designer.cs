namespace ProjetDNC_client
{
    partial class Form_login
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.pseudo_txt = new System.Windows.Forms.TextBox();
            this.connexion_btn = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(195, 36);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(109, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Choisissez un pseudo";
            // 
            // pseudo_txt
            // 
            this.pseudo_txt.Location = new System.Drawing.Point(148, 64);
            this.pseudo_txt.MaxLength = 16;
            this.pseudo_txt.Name = "pseudo_txt";
            this.pseudo_txt.Size = new System.Drawing.Size(203, 20);
            this.pseudo_txt.TabIndex = 1;
            // 
            // connexion_btn
            // 
            this.connexion_btn.Location = new System.Drawing.Point(211, 99);
            this.connexion_btn.Name = "connexion_btn";
            this.connexion_btn.Size = new System.Drawing.Size(75, 23);
            this.connexion_btn.TabIndex = 2;
            this.connexion_btn.Text = "Connexion";
            this.connexion_btn.UseVisualStyleBackColor = true;
            this.connexion_btn.Click += new System.EventHandler(this.connexion_btn_Click);
            // 
            // Form_login
            // 
            this.AcceptButton = this.connexion_btn;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(504, 162);
            this.Controls.Add(this.connexion_btn);
            this.Controls.Add(this.pseudo_txt);
            this.Controls.Add(this.label1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MaximumSize = new System.Drawing.Size(520, 200);
            this.MinimizeBox = false;
            this.MinimumSize = new System.Drawing.Size(520, 200);
            this.Name = "Form_login";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Connexion";
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.Form_login_FormClosed);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox pseudo_txt;
        private System.Windows.Forms.Button connexion_btn;
    }
}