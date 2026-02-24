import axios from "axios";

 const api = axios.create({
  baseURL: "https://trendexplore.onrender.com",
});
export default api;