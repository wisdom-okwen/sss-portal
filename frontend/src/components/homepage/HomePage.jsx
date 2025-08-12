import React, { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { getUser } from "../../utils/auth";

function HomePage() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    getUser().then(setUser);
  }, []);

  return (
    <Box sx={{ p: { xs: 2, sm: 4 }, bgcolor: "#ecf0f4ff", minHeight: "100vh" }}>
      <Typography variant="h4" fontWeight={700} sx={{ mb: 2, color: "#222" }}>
        Hello{user?.first_name ? `, ${user.first_name}` : ""}! 👋
      </Typography>
      <Typography variant="body1" sx={{ mb: 4, color: "#555" }}>
        Welcome to your dashboard. Here is your account information:
      </Typography>
      <Box sx={{ bgcolor: "#fff", borderRadius: 3, boxShadow: 2, p: 3, maxWidth: 400 }}>
        <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 1 }}>
          Name: {user?.first_name || "-"}
        </Typography>
        <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 1 }}>
          Email: {user?.email || "-"}
        </Typography>
        <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 1 }}>
          UserType: {user?.user_type || "-"}
        </Typography>
      </Box>
    </Box>
  );
}

export default HomePage;
