import React from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();

  const handleAddStudent = () => {
    alert("Redirecting to Add Student page or function...");
    // navigate("/add-student"); // Uncomment if Add Student page exists
  };

  const handleAddClass = () => {
    alert("Redirecting to Add Class page or function...");
    // navigate("/add-class"); // Uncomment if Add Class page exists
  };

  const handleTakeAttendance = () => {
    alert("Redirecting to Take Attendance page or function...");
    // navigate("/take-attendance"); // Uncomment if Take Attendance page exists
  };

  return (
    <div className="container mt-5">
      <h2>Admin Dashboard</h2>
      <p>Welcome, Admin! Manage your system below:</p>
      <div className="d-grid gap-3 mt-4">
        <button className="btn btn-primary btn-lg" onClick={handleAddStudent}>
          Add Student
        </button>
        <button className="btn btn-secondary btn-lg" onClick={handleAddClass}>
          Add Class
        </button>
        <button className="btn btn-success btn-lg" onClick={handleTakeAttendance}>
          Take Attendance
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
