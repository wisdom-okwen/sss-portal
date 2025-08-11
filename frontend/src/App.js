import React, { useEffect } from "react";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import LoginPage from "./components/loginpage/LoginPage";
import HomePage from "./components/homepage/HomePage";

function RedirectOnLogin() {
  const navigate = useNavigate();
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      navigate("/home", { replace: true });
    }
  }, [navigate]);
  return null;
}

function App() {
  return (
    <BrowserRouter>
      <RedirectOnLogin />
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/home" element={<HomePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
