namespace ProjetDNC_client
{
    partial class Form_nickname
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
            this.change_btn = new System.Windows.Forms.Button();
            this.pseudo_txt = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // change_btn
            // 
            this.change_btn.Location = new System.Drawing.Point(211, 99);
            this.change_btn.Name = "change_btn";
            this.change_btn.Size = new System.Drawing.Size(75, 23);
            this.change_btn.TabIndex = 2;
            this.change_btn.Text = "Envoyer";
            this.change_btn.UseVisualStyleBackColor = true;
            this.change_btn.Click += new System.EventHandler(this.change_btn_Click);
            // 
            // pseudo_txt
            // 
            this.pseudo_txt.Location = new System.Drawing.Point(148, 64);
            this.pseudo_txt.MaxLength = 16;
            this.pseudo_txt.Name = "pseudo_txt";
            this.pseudo_txt.Size = new System.Drawing.Size(203, 20);
            this.pseudo_txt.TabIndex = 1;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(195, 35);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(109, 13);
            this.label1.TabIndex = 3;
            this.label1.Text = "Choisissez un pseudo";
            // 
            // Form_nickname
            // 
            this.AcceptButton = this.change_btn;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(504, 162);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.pseudo_txt);
            this.Controls.Add(this.change_btn);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "Form_nickname";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Hide;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Changement de pseudo";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Button change_btn;
        private System.Windows.Forms.TextBox pseudo_txt;
        private System.Windows.Forms.Label label1;
    }
}