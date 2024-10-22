import React from 'react';
import { useDropzone } from 'react-dropzone';
import './DragDrop.css';

const DragDrop = () => {
  const onDrop = (acceptedFiles) => {
    console.log(acceptedFiles);
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