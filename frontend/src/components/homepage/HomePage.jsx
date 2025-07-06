
import React from "react";

import Box from "@mui/material/Box";
import NavBar from "../NavBar/NavBar";
import { Link, Routes, Route } from "react-router-dom";
import Tooltip from "@mui/material/Tooltip";
import DashboardIcon from '@mui/icons-material/Dashboard';
import SchoolIcon from '@mui/icons-material/School';
import PeopleIcon from '@mui/icons-material/People';
import ClassIcon from '@mui/icons-material/Class';
import SettingsIcon from '@mui/icons-material/Settings';
import NewspaperIcon from '@mui/icons-material/Newspaper';
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";
import NewsCarousel from "../cards/News/NewsCarousel";
import { newsItems } from "../../assets/newsData";

function HomePage() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const [authOpen, setAuthOpen] = React.useState(false);
  const [isSignup, setIsSignup] = React.useState(false);
  const navItems = [
    { label: 'News', icon: <NewspaperIcon />, path: '/' },
    { label: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
    { label: 'Students', icon: <SchoolIcon />, path: '/students' },
    { label: 'Teachers', icon: <PeopleIcon />, path: '/teachers' },
    { label: 'Classes', icon: <ClassIcon />, path: '/classes' },
    { label: 'Settings', icon: <SettingsIcon />, path: '/settings' },
  ];

  return (
    <Box>
      <NavBar onProfileClick={() => { setAuthOpen(true); setIsSignup(false); }} />
      <Box sx={{ display: 'flex', height: 'calc(100vh - 64px)' }}>
        {/* Left Navigation (hidden on mobile) */}
        {!isMobile && (
          <Box sx={{ width: 240, bgcolor: 'background.paper', borderRight: 1, borderColor: 'divider', p: 0, pt: 2 }}>
            <Box sx={{ fontWeight: 'bold', mb: 2, pl: 3 }}>Actions</Box>
            <Box component="nav">
              {navItems.map((item) => (
                <Tooltip key={item.label} title={item.label} arrow placement="right">
                  <Link
                    to={item.path}
                    style={{ textDecoration: 'none', color: 'inherit' }}
                  >
                    <Box
                      sx={{
                        display: 'flex',
                        alignItems: 'center',
                        px: 3,
                        py: 1.5,
                        mb: 0.5,
                        borderRadius: 2,
                        cursor: 'pointer',
                        transition: 'background 0.2s',
                        '&:hover': {
                          backgroundColor: 'primary.50',
                        },
                        fontWeight: 500,
                      }}
                    >
                      <Box sx={{ mr: 2 }}>{item.icon}</Box>
                      {item.label}
                    </Box>
                  </Link>
                </Tooltip>
              ))}
            </Box>
          </Box>
        )}
        {/* Right Content (Routed Pages) */}
        <Box sx={{ flexGrow: 1, p: 4, bgcolor: 'background.default' }}>
          <Routes>
            <Route path="/" element={<NewsPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/students" element={<StudentsPage />} />
            <Route path="/teachers" element={<TeachersPage />} />
            <Route path="/classes" element={<ClassesPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<NewsPage />} />
          </Routes>
        </Box>
      </Box>
    </Box>
  );

  // Dummy page components for demonstration
  function DashboardPage() {
    return <Box sx={{ fontSize: 24, fontWeight: 'bold' }}>Dashboard</Box>;
  }
  function StudentsPage() {
    return <Box sx={{ fontSize: 24, fontWeight: 'bold' }}>Students</Box>;
  }
  function TeachersPage() {
    return <Box sx={{ fontSize: 24, fontWeight: 'bold' }}>Teachers</Box>;
  }
  function ClassesPage() {
    return <Box sx={{ fontSize: 24, fontWeight: 'bold' }}>Classes</Box>;
  }
  function SettingsPage() {
    return <Box sx={{ fontSize: 24, fontWeight: 'bold' }}>Settings</Box>;
  }
  function NewsPage() {
    return (
      <Box>
        <Box sx={{ fontSize: 24, fontWeight: 'bold', mb: 2 }}>News</Box>
        <NewsCarousel items={newsItems} />
      </Box>
    );
  }
};

export default HomePage;
