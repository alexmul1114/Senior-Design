const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

// Use CORS to allow requests from your frontend
app.use(cors());

// Serve static files from the 'assets' folder
app.use('/assets', express.static(path.join(__dirname, 'assets')));

// Endpoint to list images from the 'assets/images' folder
app.get('/images', (req, res) => {
  const imagesDir = path.join(__dirname, 'assets/images');

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

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});