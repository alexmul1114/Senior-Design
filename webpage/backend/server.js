const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Ensure the necessary directories exist
const imagesDir = path.join(__dirname, 'assets/images');
const selectedImagesDir = path.join(__dirname, 'assets/selectedImages');

// Create directories if they don't exist
if (!fs.existsSync(imagesDir)) {
  fs.mkdirSync(imagesDir, { recursive: true });
}

if (!fs.existsSync(selectedImagesDir)) {
  fs.mkdirSync(selectedImagesDir, { recursive: true });
}

// Serve static files from the 'assets' folder
app.use('/assets', express.static(path.join(__dirname, 'assets')));

// Endpoint to list images from the 'assets/images' folder
app.get('/images', (req, res) => {
  fs.readdir(imagesDir, (err, files) => {
    if (err) {
      console.error('Error reading images directory:', err);
      return res.status(500).json({ error: 'Unable to read images directory' });
    }

    const images = files.map((file) => ({
      name: file,
      url: `${req.protocol}://${req.get('host')}/assets/images/${file}`,
    }));

    res.json(images);
  });
});

// Endpoint to list selected images
app.get('/selected-images', (req, res) => {
  fs.readdir(selectedImagesDir, (err, files) => {
    if (err) {
      console.error('Error reading selected images directory:', err);
      return res.status(500).json({ error: 'Unable to read selected images directory' });
    }

    const images = files.map((file) => ({
      name: file,
      url: `${req.protocol}://${req.get('host')}/assets/selectedImages/${file}`,
      size: fs.statSync(path.join(selectedImagesDir, file)).size,
    }));

    res.json(images);
  });
});

// Endpoint to add an image to the selectedImages folder
app.post('/add-image', (req, res) => {
  const { imageName } = req.body;
  const src = path.join(imagesDir, imageName);
  const dest = path.join(selectedImagesDir, imageName);

  fs.copyFile(src, dest, (err) => {
    if (err) {
      console.error('Error copying image to selectedImages folder:', err);
      return res.status(500).json({ error: 'Unable to add image' });
    }
    res.status(200).json({ message: 'Image added successfully' });
  });
});

// Endpoint to remove an image from the selectedImages folder
app.post('/remove-image', (req, res) => {
  const { imageName } = req.body;
  const filePath = path.join(selectedImagesDir, imageName);

  fs.unlink(filePath, (err) => {
    if (err) {
      console.error('Error removing image from selectedImages folder:', err);
      return res.status(500).json({ error: 'Unable to remove image' });
    }
    res.status(200).json({ message: 'Image removed successfully' });
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
