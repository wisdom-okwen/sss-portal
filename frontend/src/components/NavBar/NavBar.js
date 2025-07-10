import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import HomeIcon from "@mui/icons-material/Home";
import ManageAccountsIcon from "@mui/icons-material/ManageAccounts";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import Box from "@mui/material/Box";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";

const logoUrl =
  "https://upload.wikimedia.org/wikipedia/commons/4/4a/Logo_2013_Google.png"; // Replace with your logo

const personaTitles = {
  admin: "SSS Portal - Admin",
  student: "SSS Portal - Student",
  teacher: "SSS Portal - Teacher",
  proxy: "SSS Portal - Proxy",
};

const NavBar = ({ persona = "admin" }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  return (
    <AppBar position="static" color="primary" elevation={1}>
      <Toolbar sx={{ justifyContent: "space-between", px: 2 }}>
        {/* Left: Burger or Home/Manage/Profile icons */}
        {isMobile ? (
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
        ) : (
          <Box sx={{ display: "flex", gap: 1 }}>
            <IconButton color="inherit">
              <HomeIcon />
            </IconButton>
            <IconButton color="inherit">
              <ManageAccountsIcon />
            </IconButton>
            <IconButton color="inherit">
              <AccountCircleIcon />
            </IconButton>
          </Box>
        )}

        {/* Center: Title */}
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, textAlign: "center", fontWeight: 600 }}
        >
          {personaTitles[persona] || "SSS Portal"}
        </Typography>

        {/* Right: Logo */}
        <Box sx={{ display: "flex", alignItems: "center" }}>
          <img
            src={logoUrl}
            alt="Logo"
            style={{ height: 36, width: 36, borderRadius: "50%" }}
          />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default NavBar;
