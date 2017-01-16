namespace ProjetDNC_client
{
    partial class Image_picker
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
            this.img_layout = new System.Windows.Forms.FlowLayoutPanel();
            this.SuspendLayout();
            // 
            // img_layout
            // 
            this.img_layout.AutoScroll = true;
            this.img_layout.Dock = System.Windows.Forms.DockStyle.Fill;
            this.img_layout.Location = new System.Drawing.Point(0, 0);
            this.img_layout.Name = "img_layout";
            this.img_layout.Padding = new System.Windows.Forms.Padding(10);
            this.img_layout.Size = new System.Drawing.Size(684, 462);
            this.img_layout.TabIndex = 0;
            // 
            // Image_picker
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Window;
            this.ClientSize = new System.Drawing.Size(684, 462);
            this.Controls.Add(this.img_layout);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "Image_picker";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterParent;
            this.Text = "Sélectionner une image";
            this.TopMost = true;
            this.Load += new System.EventHandler(this.Image_picker_Load);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.FlowLayoutPanel img_layout;
    }
}