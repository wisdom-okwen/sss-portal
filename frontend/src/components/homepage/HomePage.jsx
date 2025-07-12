
import React from "react";

import Box from "@mui/material/Box";
import NavBar from "../NavBar/NavBar";
import { Link, Routes, Route } from "react-router-dom";
import DashboardIcon from '@mui/icons-material/Dashboard';
import SchoolIcon from '@mui/icons-material/School';
import PeopleIcon from '@mui/icons-material/People';
import ClassIcon from '@mui/icons-material/Class';
import SettingsIcon from '@mui/icons-material/Settings';
import NewspaperIcon from '@mui/icons-material/Newspaper';
import LeftNav from "../LeftNav/LeftNav";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";
import NewsCarousel from "../cards/News/NewsCarousel";
import { newsItems } from "../../assets/newsData";


function HomePage() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const [pageTitle, setPageTitle] = React.useState("News");
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
      <NavBar title={pageTitle} />
      <Box sx={{ display: 'flex', height: 'calc(100vh - 64px)' }}>
        {/* Left Navigation (hidden on mobile) */}
        {!isMobile && (
          <LeftNav navItems={navItems} onNavClick={setPageTitle} />
        )}
        {/* Right Content (Routed Pages) */}
        <Box sx={{ flexGrow: 1, p: 4, bgcolor: 'background.default' }}>
          <Routes>
            <Route path="/" element={<NewsPage setPageTitle={setPageTitle} />} />
            <Route path="/dashboard" element={<DashboardPage setPageTitle={setPageTitle} />} />
            <Route path="/students" element={<StudentsPage setPageTitle={setPageTitle} />} />
            <Route path="/teachers" element={<TeachersPage setPageTitle={setPageTitle} />} />
            <Route path="/classes" element={<ClassesPage setPageTitle={setPageTitle} />} />
            <Route path="/settings" element={<SettingsPage setPageTitle={setPageTitle} />} />
            <Route path="*" element={<NewsPage setPageTitle={setPageTitle} />} />
          </Routes>
        </Box>
      </Box>
    </Box>
  );

  function DashboardPage() {
    return <Box />;
  }
  function StudentsPage() {
    return <Box />;
  }
  function TeachersPage() {
    return <Box />;
  }
  function ClassesPage() {
    return <Box />;
  }
  function SettingsPage() {
    return <Box />;
  }
  function NewsPage() {
    return (
      <Box>
        <NewsCarousel items={newsItems} />
      </Box>
    );
  }
};

export default HomePage;
