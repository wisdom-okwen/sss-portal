import React, { useEffect } from 'react';
import './LoginPage.css';
import { FaGoogle, FaFacebookF, FaTwitter, FaApple } from 'react-icons/fa';

const LoginPage = () => {
  useEffect(() => {
    document.title = "Sign In | SSS-Portal";
  }, []);

  return (
    <div className="login-page-split">
      <div className="login-image" />
      <div className="login-form-container">
        <div className="login-card">
          <h2 className="login-title">Sign In</h2>
          <form>
            <div className="form-group floating-label-group">
              <input
                type="text"
                id="username"
                name="username"
                required
                autoComplete="username"
                className="floating-input"
                placeholder=" "
              />
              <label htmlFor="username" className="floating-label">Username</label>
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
