import React, { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import { getUser } from "../../utils/auth";
import LeftNav from "../LeftNav/LeftNav";
import NavBar from "../NavBar/NavBar";

const DashboardLayout = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    getUser().then(setUser);
  }, []);

  return (
    <Box sx={{ display: 'flex', height: '100vh', bgcolor: "#c8d0d7ff" }}>
      <Box sx={{ width: 240, minWidth: 240, height: "100vh", position: "fixed", left: 0, top: 0, zIndex: 1200 }}>
        <LeftNav user={user || {}} />
      </Box>
      <Box sx={{ flexGrow: 1, ml: "240px", display: "flex", flexDirection: "column", height: "100vh" }}>
        <NavBar
          user={user || {}}
          sx={{
            left: "240px",
            width: "calc(100% - 240px)",
          }}
        />
        <Box sx={{ flexGrow: 1, mt: "72px" }}>
          {children}
        </Box>
      </Box>
    </Box>
  );
};

export default DashboardLayout;