import React from 'react';
import DragDrop from '../components/DragDrop';
import Footer from '../components/Footer';
import './ProfilePage.css';

const ProfilePage = () => {
  return (
    <div className="profile-page">
      <h2>Profile Information</h2>
      <input type="text" placeholder="Full Name" />
      <input type="email" placeholder="Email" />
      <div className="your-images">
        <h3>Your Images</h3>
        <DragDrop />
      </div>
      <Footer />
    </div>
  );
};

export default ProfilePage;