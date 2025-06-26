import React from 'react';

// UserContext to provide user info and role
const UserContext = React.createContext({
  name: 'Student User',
  role: 'student', // 'admin', 'teacher', 'proxy'
});

export default UserContext;
