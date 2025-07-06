import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";

import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import AccountCircle from "@mui/icons-material/AccountCircle";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Stack from "@mui/material/Stack";


const NavBar = ({ onManageClick }) => {
  const [open, setOpen] = React.useState(false);

  const handleProfileClick = () => {
    setOpen(true);
  };
  const handleClose = () => {
    setOpen(false);
  };

  return (
    <AppBar position="static" color="primary" elevation={1}>
      <Toolbar>
        <Box sx={{ flexGrow: 1, display: 'flex', justifyContent: 'center', alignItems: 'center', position: 'relative', width: '100%' }}>
          <Typography variant="h6" component="div" sx={{ position: 'absolute', left: 0, right: 0, textAlign: 'center', width: '100%' }}>
            SSS Portal - Admin
          </Typography>
          <Box sx={{ position: 'absolute', right: 0, display: 'flex', alignItems: 'center', gap: 1 }}>
            <Button color="inherit" variant="outlined" onClick={onManageClick}>Manage</Button>
            <IconButton color="inherit" onClick={handleProfileClick} aria-label="profile">
              <AccountCircle />
            </IconButton>
          </Box>
        </Box>
      </Toolbar>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Sign Up or Login</DialogTitle>
        <DialogContent>
          <Stack spacing={2} direction="column" sx={{ mt: 1 }}>
            <Button variant="contained" color="primary" onClick={() => { handleClose(); /* trigger signup modal here */ }}>Sign Up</Button>
            <Button variant="outlined" color="primary" onClick={() => { handleClose(); /* trigger login modal here */ }}>Login</Button>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </AppBar>
  );
};

export default NavBar;
