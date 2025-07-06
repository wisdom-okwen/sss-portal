import PropTypes from "prop-types";
import React, { useState } from "react";

const AuthModal = ({ onClose, onSubmit, isSignup }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await onSubmit(email, password, isSignup);
    } catch (err) {
      setError(err.message || "Authentication failed");
    }
  };
  return (
    <div className="modal-backdrop">
      <div className="modal">
        <h2>{isSignup ? "Sign Up" : "Login"}</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">{isSignup ? "Sign Up" : "Login"}</button>
          <button type="button" onClick={onClose}>
            Cancel
          </button>
        </form>
        {error && <div className="error">{error}</div>}
      </div>
    </div>
  );
};

AuthModal.propTypes = {
  onClose: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
  isSignup: PropTypes.bool.isRequired,
};

export default AuthModal;
