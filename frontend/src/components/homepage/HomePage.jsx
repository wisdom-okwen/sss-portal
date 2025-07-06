
import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";

const HomePage = () => {
  return (
    <AppBar position="static" color="primary" elevation={1}>
      <Toolbar>
        <Box sx={{ flexGrow: 1, display: 'flex', justifyContent: 'center', alignItems: 'center', position: 'relative', width: '100%' }}>
          <Typography variant="h6" component="div" sx={{ position: 'absolute', left: 0, right: 0, textAlign: 'center', width: '100%' }}>
            SSS Portal - Admin
          </Typography>
          <Box sx={{ position: 'absolute', right: 0 }}>
            <Button color="inherit" variant="outlined">Manage</Button>
          </Box>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default HomePage;
