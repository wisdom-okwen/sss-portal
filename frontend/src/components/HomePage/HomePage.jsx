import React from "react";

import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import HomeIcon from "@mui/icons-material/Home";
import ManageAccountsIcon from "@mui/icons-material/ManageAccounts";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import NavBar from "../NavBar/NavBar";

function HomePage() {
  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "#f5f6fa" }}>
      <NavBar persona="admin" />
      {/* Main Layout */}
      <Box
        sx={{
          display: "flex",
          flexDirection: "row",
          maxWidth: 1400,
          mx: "auto",
          mt: 4,
          px: 2,
        }}
      >
        {/* Left Sidebar */}
        <Box
          sx={{
            width: { xs: 60, md: "20%" },
            minWidth: 60,
            bgcolor: "#fff",
            borderRadius: 2,
            boxShadow: 1,
            p: 2,
            mr: { md: 4, xs: 2 },
            display: "flex",
            flexDirection: { xs: "column", md: "column" },
            alignItems: "center",
            gap: 2,
            height: 320,
          }}
        >
          <IconButton color="primary">
            <HomeIcon />
          </IconButton>
          <IconButton color="primary">
            <ManageAccountsIcon />
          </IconButton>
          <IconButton color="primary">
            <AccountCircleIcon />
          </IconButton>
        </Box>

        {/* Main Content */}
        <Box
          sx={{
            flex: 1,
            maxWidth: { md: "70%", xs: "100%" },
            minWidth: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Card sx={{ minWidth: 320, maxWidth: 480, p: 2, boxShadow: 3 }}>
            <CardContent>
              <Typography
                variant="h5"
                align="center"
                fontWeight={600}
                gutterBottom
              >
                Welcome to SSS Portal
              </Typography>
              <Typography align="center" color="text.secondary">
                You are logged in as <b>Admin</b>.
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Box>
    </Box>
  );
};

export default HomePage;
