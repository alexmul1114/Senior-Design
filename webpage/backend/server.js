const express = require('express');
const fs = require('fs');
const path = require('path');
const basicAuth = require('express-basic-auth');

const app = express();
const PORT = process.env.PORT || 5000;

// Basic authentication middleware
app.use(basicAuth({
  users: { 'admin': 'password123' }, // Replace 'password123' with your desired password
  challenge: true
}));

// Define paths for folders
const imagesFolder = path.join(__dirname, 'assets/images');
const selectedImagesFolder = path.join(__dirname, 'assets/selectedImages');
const homePageSlidesFolder = path.join(__dirname, 'assets/homePageSlides');
const processedImagesFolder = path.join(__dirname, 'assets/processedImages');

// Middleware to parse JSON bodies
app.use(express.json());

// Create folders if they don't exist
const folders = [imagesFolder, selectedImagesFolder, homePageSlidesFolder, processedImagesFolder];
folders.forEach((folder) => {
  if (!fs.existsSync(folder)) {
    fs.mkdirSync(folder, { recursive: true });
  }
});

// Endpoint to get list of images from a specified folder
app.get('/api/images/:folder', (req, res) => {
  const folderName = req.params.folder;
  let folderPath;

  switch (folderName) {
    case 'images':
      folderPath = imagesFolder;
      break;
    case 'selectedImages':
      folderPath = selectedImagesFolder;
      break;
    case 'homePageSlides':
      folderPath = homePageSlidesFolder;
      break;
    case 'processedImages':
      folderPath = processedImagesFolder;
      break;
    default:
      return res.status(400).send('Invalid folder name');
  }

  fs.readdir(folderPath, (err, files) => {
    if (err) {
      return res.status(500).send('Unable to read folder');
    }
    res.json(files);
  });
});

// Endpoint to add an image to selectedImages folder
app.post('/api/addImage', (req, res) => {
  const { imageName } = req.body;
  const sourcePath = path.join(imagesFolder, imageName);
  const destinationPath = path.join(selectedImagesFolder, imageName);

  fs.copyFile(sourcePath, destinationPath, (err) => {
    if (err) {
      return res.status(500).send('Failed to copy image');
    }
    res.send('Image added successfully');
  });
});

// Endpoint to remove an image from selectedImages folder
app.post('/api/removeImage', (req, res) => {
  const { imageName } = req.body;
  const filePath = path.join(selectedImagesFolder, imageName);

  fs.unlink(filePath, (err) => {
    if (err) {
      return res.status(500).send('Failed to remove image');
    }
    res.send('Image removed successfully');
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
