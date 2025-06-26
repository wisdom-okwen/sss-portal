import React, { useContext } from 'react';
import './HomePage.css';
import UserContext from '../../contexts/UserContext';

// HomePage component

const HomePage = () => {
  const user = useContext(UserContext);

  if (user.role === 'student') {
    return (
      <div className="homepage">
        <h1>Welcome, {user.name}!</h1>
        <h2>Student Dashboard</h2>
        <ul>
          <li>View your academic records</li>
          <li>Enroll in classes</li>
          <li>View and pay tuition/fees</li>
          <li>Contact your teachers</li>
        </ul>
      </div>
    );
  }

  if (user.role === 'admin') {
    return (
      <div className="homepage">
        <h1>Welcome, {user.name}!</h1>
        <h2>Administrator Dashboard</h2>
        <ul>
          <li>Manage teachers and students</li>
          <li>View and update finances</li>
          <li>Enroll or remove students</li>
          <li>Manage school settings</li>
        </ul>
      </div>
    );
  }

  if (user.role === 'teacher') {
    return (
      <div className="homepage">
        <h1>Welcome, {user.name}!</h1>
        <h2>Teacher Dashboard</h2>
        <ul>
          <li>Take attendance</li>
          <li>Manage student scores</li>
          <li>Approve enrollments</li>
          <li>Contact parents/guardians</li>
        </ul>
      </div>
    );
  }

  // Proxy (parent/guardian)
  return (
    <div className="homepage">
      <h1>Welcome, {user.name}!</h1>
      <h2>Parent/Guardian Dashboard</h2>
      <ul>
        <li>View your child's academic records</li>
        <li>View and pay school fees</li>
        <li>Contact school officials</li>
      </ul>
    </div>
  );
};

export { HomePage };
