import React, { useEffect, useState } from "react";
import axios from "axios";

const Students = () => {
  const [students, setStudents] = useState([]);
  const [newStudent, setNewStudent] = useState({ name: "", email: "" });

  useEffect(() => {
    const fetchStudents = async () => {
      const token = localStorage.getItem("token");
      const response = await axios.get("http://localhost:5000/students", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setStudents(response.data);
    };

    fetchStudents();
  }, []);

  const handleAddStudent = async () => {
    const token = localStorage.getItem("token");
    await axios.post("http://localhost:5000/students", newStudent, {
      headers: { Authorization: `Bearer ${token}` },
    });
    setStudents([...students, newStudent]);
    setNewStudent({ name: "", email: "" });
  };

  return (
    <div className="container mt-5">
      <h2>Manage Students</h2>
      <div className="mb-3">
        <input
          type="text"
          placeholder="Name"
          className="form-control mb-2"
          value={newStudent.name}
          onChange={(e) => setNewStudent({ ...newStudent, name: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          className="form-control mb-2"
          value={newStudent.email}
          onChange={(e) => setNewStudent({ ...newStudent, email: e.target.value })}
        />
        <button onClick={handleAddStudent} className="btn btn-primary">
          Add Student
        </button>
      </div>
      <ul className="list-group">
        {students.map((student) => (
          <li key={student.id} className="list-group-item">
            {student.name} - {student.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Students;
