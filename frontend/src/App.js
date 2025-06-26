
import './App.css';
import { HomePage } from './components/homepage/HomePage';
import UserContext from './contexts/UserContext';


function App() {
  // Change role to 'student', 'admin', 'teacher', or 'proxy' to test different homepages
  const user = { name: 'Jane Doe', role: 'student' };
  return (
    <UserContext.Provider value={user}>
      <div className="App">
        <HomePage />
      </div>
    </UserContext.Provider>
  );
}

export default App;
