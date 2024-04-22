import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signInWithEmailAndPassword } from 'firebase/auth';
import auth from './firebase/firebase';
import ChatBox from './ChatBox'; // Import the ChatBox component
import './Login.css';

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;
      if (!user.emailVerified) {
        setError("Please verify your email before logging in.");
        return;
      }
      console.log("Login successful");
      navigate('/');
    } catch (error) {
      setError(error.message);
    }
  };

  const handleRegisterClick = () => {
    navigate('/register');
  };

  return (
    <div className="login-page">
      <div className="welcome-text">WELCOME TO INTELLIGENT GUARD AI SURVEILLANCE SYSTEM</div>
      <div className="login-container">
        <h2>Login</h2>
        <form onSubmit={handleLogin}>
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
          <button type="submit" className="submit-button">Login</button>
        </form>
        {error && <p className="error-message">{error}</p>}
        <div className="register-link">
          <button onClick={handleRegisterClick} className="register-button">Register</button>
        </div>
        {/* Add the ChatBox component here */}
        <ChatBox />
      </div>
    </div>
  );
};

export default Login;
