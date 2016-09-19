namespace ProjetDNC_client
{
    partial class Form_private
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
            this.demand_btn = new System.Windows.Forms.Button();
            this.pseudo_combo = new System.Windows.Forms.ComboBox();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(198, 33);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(109, 13);
            this.label1.TabIndex = 6;
            this.label1.Text = "Choisissez un pseudo";
            // 
            // demand_btn
            // 
            this.demand_btn.Location = new System.Drawing.Point(181, 97);
            this.demand_btn.Name = "demand_btn";
            this.demand_btn.Size = new System.Drawing.Size(139, 37);
            this.demand_btn.TabIndex = 5;
            this.demand_btn.Text = "Demander une conversation privée";
            this.demand_btn.UseVisualStyleBackColor = true;
            this.demand_btn.Click += new System.EventHandler(this.demand_btn_Click);
            // 
            // pseudo_combo
            // 
            this.pseudo_combo.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.pseudo_combo.FormattingEnabled = true;
            this.pseudo_combo.Location = new System.Drawing.Point(158, 60);
            this.pseudo_combo.Name = "pseudo_combo";
            this.pseudo_combo.Size = new System.Drawing.Size(188, 21);
            this.pseudo_combo.TabIndex = 1;
            // 
            // Form_private
            // 
            this.AcceptButton = this.demand_btn;
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(504, 162);
            this.Controls.Add(this.pseudo_combo);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.demand_btn);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "Form_private";
            this.ShowIcon = false;
            this.ShowInTaskbar = false;
            this.SizeGripStyle = System.Windows.Forms.SizeGripStyle.Hide;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Conversation privée";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button demand_btn;
        private System.Windows.Forms.ComboBox pseudo_combo;
    }
}