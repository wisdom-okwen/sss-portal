import React from "react";
import Box from "@mui/material/Box";
import Tooltip from "@mui/material/Tooltip";
import { Link, useLocation } from "react-router-dom";

const LeftNav = ({ navItems, onNavClick }) => {
  const location = useLocation();
  return (
    <Box sx={{ width: 240, bgcolor: 'background.paper', borderRight: 1, borderColor: 'divider', p: 0, pt: 2 }}>
      <Box sx={{ fontWeight: 'bold', mb: 2, pl: 3 }}>Actions</Box>
      <Box component="nav">
        {navItems.map((item) => (
          <Tooltip key={item.label} title={item.label} arrow placement="right">
            <Link
              to={item.path}
              style={{ textDecoration: 'none', color: 'inherit' }}
              onClick={() => onNavClick(item.label)}
            >
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  px: 3,
                  py: 1.5,
                  mb: 0.5,
                  borderRadius: 2,
                  cursor: 'pointer',
                  transition: 'background 0.2s',
                  backgroundColor: location.pathname === item.path ? 'primary.50' : 'inherit',
                  fontWeight: 500,
                }}
              >
                <Box sx={{ mr: 2 }}>{item.icon}</Box>
                {item.label}
              </Box>
            </Link>
          </Tooltip>
        ))}
      </Box>
    </Box>
  );
};

export default LeftNav;
