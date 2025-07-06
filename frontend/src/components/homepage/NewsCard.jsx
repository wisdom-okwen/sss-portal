import React from "react";
import Card from "@mui/material/Card";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

const NewsCard = ({ title, description, image, date }) => (
  <Card sx={{ maxWidth: 345, m: 1, boxShadow: 3 }}>
    <CardMedia
      component="img"
      height="160"
      image={image}
      alt={title}
      sx={{ objectFit: "cover" }}
    />
    <CardContent>
      <Typography gutterBottom variant="h6" component="div" fontWeight={700}>
        {title}
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
        {description}
      </Typography>
      <Typography variant="caption" color="text.secondary">
        {date}
      </Typography>
    </CardContent>
  </Card>
);

export default NewsCard;
