const express = require('express');
const app = express();
app.use(express.json());

// Hardcoded user data (for demonstration)
const users = [
  { role: 'admin', email: 'admin@gmail.com', password: 'admin123' },
  { role: 'student', usn: '4ni22cs057', password: 'student123' },
  { role: 'student', usn: '4ni22cs027', password: 'password456' }
];

// Admin login route
app.post('/admin-login', (req, res) => {
  const { email, password } = req.body;
  const user = users.find((u) => u.role === 'admin' && u.email === email && u.password === password);
  if (user) {
    res.json({ success: true, role: user.role, token: 'fake-admin-token' });
  } else {
    res.status(401).json({ success: false, message: 'Invalid email or password' });
  }
});

// Student login route
app.post('/student-login', (req, res) => {
  const { usn, password } = req.body;
  const user = users.find((u) => u.role === 'student' && u.usn === usn && u.password === password);
  if (user) {
    res.json({ success: true, role: user.role, token: 'fake-student-token' });
  } else {
    res.status(401).json({ success: false, message: 'Invalid USN or password' });
  }
});

// Start the server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
