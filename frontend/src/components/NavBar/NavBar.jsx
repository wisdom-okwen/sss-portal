import React from "react";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import InputBase from "@mui/material/InputBase";
import Avatar from "@mui/material/Avatar";
import Badge from "@mui/material/Badge";
import Tooltip from "@mui/material/Tooltip";
import NotificationsIcon from "@mui/icons-material/Notifications";
import MailOutlineIcon from "@mui/icons-material/MailOutline";
import SearchIcon from "@mui/icons-material/Search";

const NavBar = ({
  user = {
    avatar: "/avatar.png",
    name: "User",
  },
  sx = {},
}) => {
  return (
    <Box
      sx={{
        width: "100%",
        height: 72,
        bgcolor: "#ecf0f4ff",
        display: "flex",
        alignItems: "center",
        px: 4,
        zIndex: 1300,
        position: "fixed",
        top: 0,
        left: 0,
        right: 0,
        ...sx,
      }}
    >
      {/* Centered Search Box with icon - highlighted ellipse, longer and smaller */}
      <Box sx={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", mt: 1.5 }}>
        <Box sx={{
          display: "flex",
          alignItems: "center",
          bgcolor: "#c8d0d7ff",
          borderRadius: "32px",
          px: 2,
          py: 0.2,
          boxShadow: "0 2px 8px 0 rgba(0,0,0,0.04)",
          height: 36,
          width: 520,
          minWidth: 320,
          maxWidth: 600,
        }}>
          <SearchIcon sx={{ color: "#29465B", mr: 1, fontSize: 20 }} />
          <InputBase
            placeholder="Search"
            sx={{
              bgcolor: "transparent",
              px: 0,
              py: 0.2,
              borderRadius: 0,
              width: "100%",
              fontSize: 15,
              color: "#29465B",
              fontWeight: 500,
              border: "none",
              boxShadow: "none",
              "& input": {
                background: "transparent",
              },
            }}
            inputProps={{ "aria-label": "search" }}
          />
        </Box>
      </Box>
      {/* Icons - highlighted ellipses, smaller and spaced above */}
      <Box sx={{ display: "flex", alignItems: "center", gap: 2.2, mt: 1.5 }}>
        <Tooltip title="Messages">
          <Box sx={{ bgcolor: "#c8d0d7ff", borderRadius: "32px", px: 1, py: 0.2, boxShadow: "0 2px 8px 0 rgba(0,0,0,0.04)" }}>
            <IconButton sx={{ bgcolor: "transparent", borderRadius: 2, p: 0.5 }}>
              <MailOutlineIcon sx={{ fontSize: 20, color: "#29465B" }} />
            </IconButton>
          </Box>
        </Tooltip>
        <Tooltip title="Notifications">
          <Box sx={{ bgcolor: "#c8d0d7ff", borderRadius: "32px", px: 1, py: 0.2, boxShadow: "0 2px 8px 0 rgba(0,0,0,0.04)" }}>
            <IconButton sx={{ bgcolor: "transparent", borderRadius: 2, p: 0.5 }}>
              <Badge
                variant="dot"
                color="error"
                overlap="circular"
                anchorOrigin={{ vertical: "top", horizontal: "right" }}
              >
                <NotificationsIcon sx={{ fontSize: 20, color: "#29465B" }} />
              </Badge>
            </IconButton>
          </Box>
        </Tooltip>
        <Tooltip title={user.name}>
          <Box sx={{ bgcolor: "#c8d0d7ff", borderRadius: "32px", px: 1, py: 0.2, boxShadow: "0 2px 8px 0 rgba(0,0,0,0.04)" }}>
            <IconButton sx={{ bgcolor: "transparent", borderRadius: "50%", p: 0.5 }}>
              <Avatar
                src={user.avatar}
                alt={user.name}
                sx={{ width: 28, height: 28, border: "2px solid #29465B" }}
              />
            </IconButton>
          </Box>
        </Tooltip>
      </Box>
    </Box>
  );
};

export default NavBar;