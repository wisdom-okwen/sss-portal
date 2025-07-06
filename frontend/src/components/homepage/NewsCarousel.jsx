import React, { useState } from "react";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import NewsCard from "./NewsCard";

const NewsCarousel = ({ items }) => {
  const [index, setIndex] = useState(0);
  const visibleCount = 2;
  const maxIndex = Math.max(0, items.length - visibleCount);

  const handlePrev = () => setIndex((prev) => Math.max(prev - 1, 0));
  const handleNext = () => setIndex((prev) => Math.min(prev + 1, maxIndex));

  return (
    <Box sx={{ display: "flex", alignItems: "center", width: "100%", justifyContent: "center", mt: 2 }}>
      <IconButton onClick={handlePrev} disabled={index === 0}>
        <ArrowBackIosNewIcon />
      </IconButton>
      <Box sx={{ display: "flex", overflow: "hidden", width: { xs: 350, sm: 700 }, justifyContent: "center" }}>
        {items.slice(index, index + visibleCount).map((item) => (
          <NewsCard key={item.id} {...item} />
        ))}
      </Box>
      <IconButton onClick={handleNext} disabled={index === maxIndex}>
        <ArrowForwardIosIcon />
      </IconButton>
    </Box>
  );
};

export default NewsCarousel;
