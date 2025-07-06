import React, { useState, useEffect, useRef } from "react";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import NewsCard from "./NewsCard";

const NewsCarousel = ({ items }) => {
  const visibleCount = 2;
  const [index, setIndex] = useState(visibleCount);
  const cardWidth = 430;
  const total = items.length;
  const intervalRef = useRef();

  // Prepare cyclic items: [last N] + items + [first N]
  const cyclicItems = [
    ...items.slice(-visibleCount),
    ...items,
    ...items.slice(0, visibleCount),
  ];
  // removed unused maxIndex

  const handlePrev = () => {
    setIndex((prev) => prev - 1);
  };
  const handleNext = () => {
    setIndex((prev) => prev + 1);
  };

  // Auto-play effect
  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setIndex((prev) => prev + 1);
    }, 4000);
    return () => clearInterval(intervalRef.current);
  }, [total]);

  // Looping effect for seamless transition
  useEffect(() => {
    if (index > total) {
      setTimeout(() => {
        setIndex(visibleCount);
      }, 600); // match transition duration
    } else if (index === 0) {
      setTimeout(() => {
        setIndex(total);
      }, 600);
    }
  }, [index, total, visibleCount]);

  return (
    <Box sx={{ display: "flex", alignItems: "center", width: "100%", justifyContent: "center", mt: 6 }}>
      <IconButton onClick={handlePrev} sx={{ mx: 3 }}>
        <ArrowBackIosNewIcon fontSize="large" />
      </IconButton>
      <Box
        sx={{
          overflow: "hidden",
          width: { xs: cardWidth * visibleCount + 15, sm: cardWidth * visibleCount + 300 },
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Box
          sx={{
            display: "flex",
            transition: (index === 0 || index > total) ? "none" : "transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)",
            transform: `translateX(-${index * cardWidth}px)`,
          }}
        >
          {cyclicItems.map((item, i) => (
            <NewsCard key={i + '-' + item.id} {...item} />
          ))}
        </Box>
      </Box>
      <IconButton onClick={handleNext} sx={{ mx: 3 }}>
        <ArrowForwardIosIcon fontSize="large" />
      </IconButton>
    </Box>
  );
};

export default NewsCarousel;
