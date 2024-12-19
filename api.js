import axios from "axios";

const API = axios.create({ baseURL: "http://localhost:5000" }); // Replace with backend URL

export const login = (data) => API.post("/login", data);
export const fetchStudents = () => API.get("/students");
export const markAttendance = (data) => API.post("/attendance", data);
export const generateReport = () => API.get("/report");

