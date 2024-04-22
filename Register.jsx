import React, { useState } from "react";
import { createUserWithEmailAndPassword, sendEmailVerification } from "firebase/auth";
import auth from "./firebase/firebase";
import { useNavigate } from 'react-router-dom';
import ChatBox from './ChatBox'; // Import the ChatBox component
import './Register.css';

const Register = () => {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [verificationSent, setVerificationSent] = useState(false); // State to track verification email sent

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      // Attempt to create a new user with the provided email and password
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      // If creation is successful, proceed with sending the verification email
      await sendEmailVerification(userCredential.user);
      console.log("Registration successful. Verification email sent.");
      setVerificationSent(true); // Set state to indicate verification email sent
      // Navigate to login page after a delay
      setTimeout(() => {
        navigate('/login');
      }, 5000); // Redirect after 5 seconds
    } catch (error) {
      // If creation fails, check if the error is due to email already in use
      if (error.code === 'auth/email-already-in-use') {
        setError("Email is already taken. Please choose another email address.");
      } else {
        setError(error.message); // Handle other errors
      }
    }
  };

  const handleLoginRedirect = () => {
    navigate('/login');
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <h2>Register</h2>
        <form onSubmit={handleRegister}>
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="input-field"
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="input-field"
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="input-field"
            />
          </div>
          <button type="submit" className="submit-button">Register</button>
        </form>
        {verificationSent && ( // Render the message if verification email sent
          <div className="verification-popup">
            Verification email sent to your email address.
          </div>
        )}
        {error && <p className="error-message">{error}</p>}
        <div className="button-group">
          <button className="redirect-button" onClick={handleLoginRedirect}>Already have an account? Login</button>
        </div>
        {/* Add the ChatBox component here */}
        <ChatBox />
      </div>
    </div>
  );
};

export default Register;
