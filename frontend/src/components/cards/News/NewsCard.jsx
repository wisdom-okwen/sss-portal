import React from "react";
import Card from "@mui/material/Card";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";


const NewsCard = ({ title, description, image, date }) => (
  <Card sx={{ maxWidth: 480, minWidth: 360, m: 2, boxShadow: 6 }}>
    <CardMedia
      component="img"
      height="240"
      image={image}
      alt={title}
      sx={{ objectFit: "cover" }}
    />
    <CardContent>
      <Typography gutterBottom variant="h5" component="div" fontWeight={700}>
        {title}
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
        {description}
      </Typography>
      <Typography variant="caption" color="text.secondary">
        {date}
      </Typography>
    </CardContent>
  </Card>
);

export default NewsCard;
