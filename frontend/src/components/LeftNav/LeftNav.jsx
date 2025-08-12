import React from "react";
import Box from "@mui/material/Box";
import Tooltip from "@mui/material/Tooltip";
import Divider from "@mui/material/Divider";
import { Link, useLocation } from "react-router-dom";
import DashboardIcon from "@mui/icons-material/Dashboard";
import SettingsIcon from "@mui/icons-material/Settings";
import LogoutIcon from "@mui/icons-material/Logout";
import NewsIcon from "@mui/icons-material/Article";
import GroupIcon from "@mui/icons-material/Group";
import StudentsIcon from "@mui/icons-material/School";
import ClassIcon from "@mui/icons-material/Class";

const adminNavItems = [
  { label: "Dashboard", icon: <DashboardIcon />, path: "/home" },
  { label: "News", icon: <NewsIcon />, path: "/news" },
  { label: "Students", icon: <StudentsIcon />, path: "/students" },
  { label: "Teachers", icon: <GroupIcon />, path: "/teachers" },
  { label: "Classes", icon: <ClassIcon />, path: "/classes" },
  { label: "Settings", icon: <SettingsIcon />, path: "/settings" },
];

const teacherNavItems = [
  { label: "Dashboard", icon: <DashboardIcon />, path: "/home" },
  { label: "News", icon: <NewsIcon />, path: "/news" },
  { label: "Students", icon: <StudentsIcon />, path: "/students" },
  { label: "Classes", icon: <ClassIcon />, path: "/classes" },
  { label: "Settings", icon: <SettingsIcon />, path: "/settings" },
];

const studentNavItems = [
  { label: "Dashboard", icon: <DashboardIcon />, path: "/home" },
  { label: "News", icon: <NewsIcon />, path: "/news" },
  { label: "Classes", icon: <ClassIcon />, path: "/classes" },
  { label: "Organisations", icon: <GroupIcon />, path: "/organisations" },

  { label: "Settings", icon: <SettingsIcon />, path: "/settings" },
];

const guardianNavItems = [
  { label: "Dashboard", icon: <DashboardIcon />, path: "/home" },
  { label: "News", icon: <NewsIcon />, path: "/news" },
  { label: "Classes", icon: <ClassIcon />, path: "/classes" },
  { label: "Organisations", icon: <GroupIcon />, path: "/organisations" },
  { label: "Settings", icon: <SettingsIcon />, path: "/settings" },
]

const othersNavItems = [
  { label: "Dashboard", icon: <DashboardIcon />, path: "/home" },
  { label: "News", icon: <NewsIcon />, path: "/news" },
  { label: "Settings", icon: <SettingsIcon />, path: "/settings" },
]

const navMap = {
  administrator: adminNavItems,
  teacher: teacherNavItems,
  student: studentNavItems,
  guardian: guardianNavItems,
  other: othersNavItems,
};

function getNavItems(user) {
  return navMap[user?.user_type] || othersNavItems;
}

const SSSPortalLogo = () => (
  <Box sx={{
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    width: "100%",
    py: 1,
  }}>
    <Box sx={{
      fontSize: 28,
      fontWeight: 900,
      color: "#7bc043",
      letterSpacing: 2,
      fontFamily: 'Montserrat, Arial, sans-serif',
      textShadow: "0 2px 8px #222, 0 1px 0 #fff",
    }}>
      SSS Portal
    </Box>
  </Box>
);

const LeftNav = ({ user = {}, onNavClick }) => {
  const location = useLocation();
  const navItems = getNavItems(user);
  return (
    <Box
      sx={{
        width: 240,
        bgcolor: "#111",
        color: "#fff",
        height: "100vh",
        position: "fixed",
        top: 0,
        left: 0,
        display: "flex",
        flexDirection: "column",
        boxShadow: "2px 0 12px rgba(41,70,91,0.08)",
        p: 0,
        zIndex: 1200,
      }}
    >
      {/* User Info (replaced with logo) */}
      <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center", p: 3, pb: 2 }}>
        <SSSPortalLogo />
      </Box>
      <Divider sx={{ bgcolor: "#222", mb: 2 }} />
      {/* Navigation */}
      <Box
        component="nav"
        sx={{
          flexGrow: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        {navItems.map((item) => (
          <Tooltip key={item.label} title={item.label} arrow placement="right">
            <Link
              to={item.path}
              style={{ textDecoration: "none", color: "inherit" }}
              onClick={() => onNavClick && onNavClick(item.label)}
            >
              <Box
                sx={{
                  display: "flex",
                  alignItems: "center",
                  px: 3,
                  py: 1.5,
                  mb: 0.5,
                  borderRadius: location.pathname === item.path ? 8 : 2,
                  cursor: "pointer",
                  backgroundColor:
                    location.pathname === item.path ? "#7bc043" : "transparent",
                  color:
                    location.pathname === item.path ? "#111" : "#fff",
                  fontWeight: location.pathname === item.path ? 700 : 500,
                  boxShadow:
                    location.pathname === item.path
                      ? "0 2px 8px rgba(41,70,91,0.08)"
                      : "none",
                  transition: "background 0.2s, color 0.2s, border-radius 0.2s",
                  "&:hover": {
                    backgroundColor: "#222",
                  },
                  minWidth: 180,
                  justifyContent: "flex-start",
                  textAlign: "left",
                }}
              >
                <Box sx={{ mr: 2, minWidth: 32, display: "flex", justifyContent: "flex-start", color: location.pathname === item.path ? "#111" : "#fff" }}>
                  {item.icon}
                </Box>
                {item.label}
              </Box>
            </Link>
          </Tooltip>
        ))}
      </Box>
      <Divider sx={{ bgcolor: "#222", mt: 2 }} />
      {/* Logout */}
      <Box
        sx={{
          px: 3,
          py: 2,
          display: "flex",
          alignItems: "center",
          justifyContent: "flex-start",
          cursor: "pointer",
          color: "#7bc043",
          fontWeight: 500,
          minWidth: 180,
          margin: "0 auto",
          borderRadius: 2,
          transition: "background 0.2s, color 0.2s",
          "&:hover": { color: "#e53935" },
          "& .logout-icon": {
            color: "#7bc043",
            transition: "color 0.2s",
          },
          "&:hover .logout-icon": {
            color: "#e53935",
          },
        }}
        onClick={() => {
          // Add your logout logic here
        }}
      >
        <LogoutIcon className="logout-icon" sx={{ mr: 2, minWidth: 32, display: "flex", justifyContent: "flex-start" }} />
        Logout
      </Box>
    </Box>
  );
};

export default LeftNav;
