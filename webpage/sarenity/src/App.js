import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ImagesPage from './pages/ImagesPage';
import ProfilePage from './pages/ProfilePage';
import AboutUsPage from './pages/AboutUsPage';
import NavBar from './components/NavBar';
import Login from './components/Login';
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [credentials, setCredentials] = useState(null);

  // Handle login callback from Login component
  const handleLogin = (username, password) => {
    setCredentials({ username, password });
    setIsAuthenticated(true);
  };

  return (
    <Router>
      <div className="App">
        {!isAuthenticated ? (
          // If the user is not authenticated, show the login page
          <Login onLogin={handleLogin} />
        ) : (
          // If the user is authenticated, show the rest of the app
          <>
            <NavBar />
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/images" element={<ImagesPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/about-us" element={<AboutUsPage />} />
            </Routes>
          </>
        )}
      </div>
    </Router>
  );
}

export default App;
