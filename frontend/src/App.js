import "./App.css";
import HomePage from "./components/homepage/HomePage";
import LoginPage from "./components/loginpage/LoginPage";
import { BrowserRouter } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        {/* <HomePage /> */}
        <LoginPage />
      </div>
    </BrowserRouter>
  );
}

export default App;
