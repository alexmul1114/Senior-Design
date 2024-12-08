import React from 'react';
import { useDropzone } from 'react-dropzone';
import './DragDrop.css';

const DragDrop = ({ onImageUpload }) => {
  const onDrop = async (acceptedFiles) => {
    for (const file of acceptedFiles) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('https://rocky-crag-89815-04ddc2eb6beb.herokuapp.com/upload', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          console.log('File uploaded successfully to assets/images:', file.name);
          if (onImageUpload) {
            onImageUpload(); // Trigger refresh of image gallery
          }
        } else {
          console.error('Failed to upload file to assets/images:', file.name);
        }
      } catch (error) {
        console.error('Error uploading file to assets/images:', file.name, error);
      }
    }
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div className="drag-drop" {...getRootProps()}>
      <input {...getInputProps()} />
      <p>Drag & Drop your images here, or click to select files.</p>
    </div>
  );
};

export default DragDrop;
