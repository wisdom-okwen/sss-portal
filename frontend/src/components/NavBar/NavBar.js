import React, { useState } from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import CloseIcon from "@mui/icons-material/Close";
import HomeIcon from "@mui/icons-material/Home";
import ManageAccountsIcon from "@mui/icons-material/ManageAccounts";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import Tooltip from "@mui/material/Tooltip";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";
import { Link } from "react-router-dom";

const logoUrl =
  "https://upload.wikimedia.org/wikipedia/commons/4/4a/Logo_2013_Google.png"; // Replace with your logo

const personaTitles = {
  admin: "SSS Portal - Admin",
  student: "SSS Portal - Student",
  teacher: "SSS Portal - Teacher",
  proxy: "SSS Portal - Proxy",
};

const NavBar = ({ persona = "admin", onProfileClick }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  // Nav items for drawer and desktop
  const navItems = [
    { label: "News", icon: <HomeIcon />, path: "/" },
    { label: "Dashboard", icon: <ManageAccountsIcon />, path: "/dashboard" },
    { label: "Students", icon: <AccountCircleIcon />, path: "/students" },
    // Add more as needed
  ];

  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleDrawerOpen = () => setDrawerOpen(true);
  const handleDrawerClose = () => setDrawerOpen(false);

  return (
    <AppBar position="static" color="primary" elevation={1}>
      <Toolbar sx={{ px: 2 }}>
        {/* Left: Logo */}
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <img
            src={logoUrl}
            alt="Logo"
            style={{ height: 36, width: 36, borderRadius: "50%" }}
          />
        </Box>

        {/* Center: Title */}
        <Typography
          variant="h5"
          component="div"
          sx={{
            flexGrow: 1,
            textAlign: "center",
            fontWeight: 800,
            letterSpacing: 1,
          }}
        >
          {personaTitles[persona] || "SSS Portal"}
        </Typography>

        {/* Right: Menu or Icons */}
        {isMobile ? (
          <>
            <IconButton
              edge="end"
              color="inherit"
              aria-label="menu"
              sx={{ ml: 2 }}
              onClick={handleDrawerOpen}
            >
              <MenuIcon />
            </IconButton>
            <Drawer
              anchor="right"
              open={drawerOpen}
              onClose={handleDrawerClose}
              transitionDuration={400}
            >
              <Box
                sx={{ width: 250, position: "relative", height: "100%" }}
                role="presentation"
                onKeyDown={handleDrawerClose}
              >
                <IconButton
                  color="inherit"
                  aria-label="close drawer"
                  onClick={handleDrawerClose}
                  sx={{ position: "absolute", top: 8, right: 8, zIndex: 1 }}
                >
                  <CloseIcon />
                </IconButton>
                <List sx={{ mt: 5 }}>
                  {navItems.map((item) => (
                    <ListItem key={item.label} disablePadding>
                      <ListItemButton
                        component={Link}
                        to={item.path}
                        onClick={handleDrawerClose}
                      >
                        <ListItemIcon>{item.icon}</ListItemIcon>
                        <ListItemText primary={item.label} />
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </Box>
            </Drawer>
          </>
        ) : (
          <Box sx={{ display: "flex", gap: 1 }}>
            <Tooltip title="Home" arrow>
              <IconButton color="inherit">
                <HomeIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Manage" arrow>
              <IconButton color="inherit">
                <ManageAccountsIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Profile" arrow>
              <IconButton color="inherit" onClick={onProfileClick}>
                <AccountCircleIcon />
              </IconButton>
            </Tooltip>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;
