import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./components/loginpage/LoginPage";
import DashBoardLayout from "./components/DashBoardLayout/DashBoardLayout";
import HomePage from "./components/homepage/HomePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route
          path="/home"
          element={
            <DashBoardLayout>
              <HomePage />
            </DashBoardLayout>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
