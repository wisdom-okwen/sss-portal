import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';
import { FaGoogle, FaFacebookF, FaTwitter, FaApple } from 'react-icons/fa';
import { login } from '../../utils/auth';
import Alert from '@mui/material/Alert';
import Collapse from '@mui/material/Collapse';

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [showError, setShowError] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    document.title = "Sign In | SSS-Portal";
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim()) {
      setError("Email is required.");
      setShowError(true);
      return;
    }
    if (!password) {
      setError("Password is required.");
      setShowError(true);
      return;
    }
    setError("");
    setShowError(false);
    const result = await login(email, password);
    if (result.success) {
      navigate("/home");
    } else {
      setError(result.error);
      setShowError(true);
    }
  };

  return (
    <div className="login-page-split">
      <div className="login-image" />
      <div className="login-form-container">
        <div className="login-card">
          {/* Modern error alert at the top of the sign-in box */}
          <Collapse in={showError}>
            <Alert
              severity="error"
              sx={{
                borderRadius: 2,
                mb: 2,
                fontWeight: 500,
                fontSize: "1rem",
                boxShadow: "0 2px 8px rgba(33,150,243,0.12)",
                background: "linear-gradient(90deg, #ffebee 0%, #ffcdd2 100%)",
                color: "#b71c1c",
              }}
              onClose={() => setShowError(false)}
            >
              {error}
            </Alert>
          </Collapse>
          <h2 className="login-title">Sign In</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group floating-label-group">
              <input
                type="email"
                id="email"
                name="email"
                required
                autoComplete="email"
                className="floating-input"
                placeholder=" "
                value={email}
                onChange={e => setEmail(e.target.value)}
              />
              <label htmlFor="email" className="floating-label">Email</label>
            </div>
            <div className="form-group floating-label-group">
              <input
                type="password"
                id="password"
                name="password"
                required
                autoComplete="current-password"
                className="floating-input"
                placeholder=" "
                value={password}
                onChange={e => setPassword(e.target.value)}
              />
              <label htmlFor="password" className="floating-label">Password</label>
            </div>
            <div className="login-options">
              <label className="remember-me">
                <input type="checkbox" name="remember" />
                Remember me
              </label>
              <a className="forgot-password" href="/forgot-password">Forgot password?</a>
            </div>
            <button className="login-btn" type="submit">Login</button>
            <div className="login-links">
              <span className="no-account-text">Don&apos;t have an account?</span>
              <a href="/signup">Sign up</a>
            </div>
          </form>
          <div className="social-login">
            <span className="social-login-text">Or sign in with</span>
            <div className="social-icons">
              <a href="/auth/google" className="social-icon" title="Sign in with Google">
                <FaGoogle />
              </a>
              <a href="/auth/facebook" className="social-icon" title="Sign in with Facebook">
                <FaFacebookF />
              </a>
              <a href="/auth/twitter" className="social-icon" title="Sign in with Twitter">
                <FaTwitter />
              </a>
              <a href="/auth/apple" className="social-icon" title="Sign in with Apple">
                <FaApple />
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
