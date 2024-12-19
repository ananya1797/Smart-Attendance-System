import React from "react";

const Attendance = () => {
  const studentDetails = {
    name: "John Doe",
    usn: "1DS19CS001",
    semester: 5,
    enrolledClasses: [
      { subject: "Mathematics", attendance: "85%" },
      { subject: "Computer Science", attendance: "90%" },
      { subject: "Physics", attendance: "80%" },
    ],
  };

  return (
    <div>
      <h2 className="mb-4">Student Attendance</h2>
      <div className="card mb-4">
        <div className="card-body">
          <h5>Student Details</h5>
          <p><strong>Name:</strong> {studentDetails.name}</p>
          <p><strong>USN:</strong> {studentDetails.usn}</p>
          <p><strong>Semester:</strong> {studentDetails.semester}</p>
        </div>
      </div>
      <h5>Enrolled Classes</h5>
      <table className="table table-striped table-bordered">
        <thead className="table-primary">
          <tr>
            <th>Subject</th>
            <th>Attendance</th>
          </tr>
        </thead>
        <tbody>
          {studentDetails.enrolledClasses.map((classItem, index) => (
            <tr key={index}>
              <td>{classItem.subject}</td>
              <td>{classItem.attendance}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Attendance;
