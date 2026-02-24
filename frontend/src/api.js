import axios from "axios";

export const api = axios.create({
  baseURL: "https://trendexplore.onrender.com",
});
