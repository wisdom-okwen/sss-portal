// Mock news data for the carousel
import mfantsipim from "./mfantsipim.jpeg";
import scitechfair from "./sci-techfair.avif";
import ptameeting from "./pta-meeting.JPG";
import sports from "./sports.jpg";
import library from "./library.jpeg";

export const newsItems = [
  {
    id: 1,
    title: "Welcome Back to School!",
    description:
      "We are excited to welcome all students and staff to a new academic year. Let's make it a great one!",
    image: mfantsipim,
    date: "2025-09-01",
  },
  {
    id: 2,
    title: "Science Fair Winners Announced",
    description:
      "Congratulations to the winners of the annual Science Fair. Check out the winning projects in the main hall.",
    image: scitechfair,
    date: "2025-10-15",
  },
  {
    id: 3,
    title: "Parent-Teacher Conferences",
    description:
      "Parent-Teacher conferences will be held next week. Please book your slots online.",
    image: ptameeting,
    date: "2025-11-05",
  },
  {
    id: 4,
    title: "New Library Books Arrived",
    description:
      "Our library has received a new collection of books across all genres. Visit and explore!",
    image: library,
    date: "2025-11-20",
  },
  {
    id: 5,
    title: "Sports Day Highlights",
    description:
      "Relive the excitement of Sports Day with photos and results now available on the portal.",
    image: sports,
    date: "2025-12-01",
  },
];
