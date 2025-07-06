import React, { useState, useEffect, useRef } from "react";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import NewsCard from "./NewsCard";

const NewsCarousel = ({ items }) => {
  const [index, setIndex] = useState(0);
  const visibleCount = 2;
  const maxIndex = Math.max(0, items.length - visibleCount);


  const intervalRef = useRef();

  const handlePrev = () => setIndex((prev) => Math.max(prev - 1, 0));
  const handleNext = () => setIndex((prev) => Math.min(prev + 1, maxIndex));

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setIndex((prev) => (prev < maxIndex ? prev + 1 : 0));
    }, 4000);
    return () => clearInterval(intervalRef.current);
  }, [maxIndex]);

  return (
    <Box sx={{ display: "flex", alignItems: "center", width: "100%", justifyContent: "center", mt: 4 }}>
      <IconButton onClick={handlePrev} disabled={index === 0} sx={{ mx: 2 }}>
        <ArrowBackIosNewIcon fontSize="large" />
      </IconButton>
      <Box sx={{ display: "flex", overflow: "hidden", width: { xs: 400, sm: 900 }, justifyContent: "center" }}>
        {items.slice(index, index + visibleCount).map((item) => (
          <NewsCard key={item.id} {...item} />
        ))}
      </Box>
      <IconButton onClick={handleNext} disabled={index === maxIndex} sx={{ mx: 2 }}>
        <ArrowForwardIosIcon fontSize="large" />
      </IconButton>
    </Box>
  );
};

export default NewsCarousel;
