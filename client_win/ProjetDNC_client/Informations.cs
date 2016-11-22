using System.Windows.Forms;

namespace ProjetDNC_client
{
    public partial class Informations : Form
    {
        /// <summary>
        /// Constructeur
        /// </summary>
        public Informations()
        {
            InitializeComponent();
        }

        /// <summary>
        /// Action au clic sur le lien github du projet
        /// </summary>
        private void linkLabel_git_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
        {
            System.Diagnostics.Process.Start(linkLabel_git.Text);
        }
    }
}
