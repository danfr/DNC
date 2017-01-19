using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ProjetDNC_client
{
    public partial class Image_picker : Form
    {
        private Dictionary<string, string> images;
        private Size miniatures_size;
        private Ini conf;

        public string ReturnValue { get; set; }

        public Image_picker(Dictionary<string,string> dict)
        {
            InitializeComponent();

            conf = new Ini("DNC_client.ini");
            int val = 100;
            int.TryParse(conf.GetValue("MIN_SIZE", "IMAGE_PICKER"), out val);
            miniatures_size = new Size(val, val);

            images = dict;

            this.MouseWheel += new MouseEventHandler(scroll_layout);
        }

        private void Image_picker_Load(object sender, EventArgs e)
        {
            foreach(KeyValuePair<string, string> kvp in images)
            {
                PictureBox pb = new PictureBox();
                Image img = new Bitmap(new Bitmap(kvp.Value), miniatures_size);
                pb.Image = img;
                pb.Tag = kvp.Key;
                pb.Size = miniatures_size;
                pb.Margin = new Padding(5);
                pb.MouseClick += new MouseEventHandler(mouse_clicked);
                img_layout.Controls.Add(pb);
            }
        }

        /// <summary>
        /// Redimensionne une image
        /// </summary>
        /// <param name="imgToResize">Image à redimensionner</param>
        /// <param name="size">Taille souhaitée</param>
        /// <returns></returns>
        public static Image resizeImage(Image imgToResize, Size size)
        {
            return (Image)(new Bitmap(imgToResize, size));
        }

        /// <summary>
        /// Fixe un bug sur le scroll
        /// </summary>
        private void scroll_layout(object sender, MouseEventArgs e)
        {
            img_layout.Focus();
        }

        /// <summary>
        /// Action au clic sur une image
        /// </summary>
        private void mouse_clicked(object sender, MouseEventArgs e)
        {
            PictureBox pb = (PictureBox)sender;
            this.ReturnValue = (string)pb.Tag;
            this.DialogResult = DialogResult.OK;
            this.Close();
        }
    }
}
