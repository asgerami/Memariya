import React, { useState, useEffect } from "react";
import { Container, Typography, TextField, Button, Box } from "@mui/material";
import axios from "axios";
import StudentForm from "./StudentForm";
import SignUp from "./SignUp";
import SignIn from "./SignIn";

function App() {
  const [studentId, setStudentId] = useState("");
  const [student, setStudent] = useState(null);
  const [concept, setConcept] = useState("");
  const [explanation, setExplanation] = useState("");

  const [createdStudent, setCreatedStudent] = useState(null);
  const [token, setToken] = useState(null);
  const [showSignUp, setShowSignUp] = useState(false);
  const [showSignIn, setShowSignIn] = useState(false);

  useEffect(() => {
    const fetchStudent = async () => {
      if (studentId) {
        try {
          const response = await axios.get(
            `http://localhost:8000/students/${studentId}`
          );
          setStudent(response.data);
        } catch (error) {
          console.error("Error fetching student:", error);
          setStudent(null);
        }
      }
    };
    fetchStudent();
  }, [studentId, createdStudent]);

  const handleGenerateExplanation = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/content/generate?concept=${concept}&student_id=${studentId}`
      );
      setExplanation(response.data.explanation);
    } catch (error) {
      console.error("Error generating explanation:", error);
      setExplanation("Error generating explanation.");
    }
  };

  const handleStudentCreated = (newStudent) => {
    setCreatedStudent(newStudent);
    setStudentId(newStudent.student_id);
  };

  const handleSignInSuccess = (token) => {
    setToken(token);
    setShowSignIn(false);
  };
  
  return (
    <Container maxWidth="md">
        <Typography variant="h4" align="center" gutterBottom>Personalized Learning Assistant</Typography>

        {token ? (
            // App content when user is logged in
            <>
                <StudentForm onCreate={handleStudentCreated} />
                <TextField
                    label="Student ID"
                    value={studentId}
                    onChange={(e) => setStudentId(e.target.value)}
                    fullWidth
                    margin="normal"
                />

                {student && (
                    <Box mt={2}>
                        <Typography variant="h6">Student Profile</Typography>
                        <Typography>Learning Style: {student.learning_style}</Typography>
                    </Box>
                )}

                <TextField
                    label="Concept to Explain"
                    value={concept}
                    onChange={(e) => setConcept(e.target.value)}
                    fullWidth
                    margin="normal"
                />

                <Button variant="contained" color="primary" onClick={handleGenerateExplanation}>
                    Generate Explanation
                </Button>

                {explanation && (
                    <Box mt={2}>
                        <Typography variant="h6">Explanation</Typography>
                        <Typography>{explanation}</Typography>
                    </Box>
                )}
            </>
        ) : (
            // Sign-up / Sign-in options if not logged in
            <Box textAlign="center">
                <Button variant="contained" color="primary" onClick={() => setShowSignUp(true)} sx={{ margin: 1 }}>
                    Sign Up
                </Button>
                <Button variant="outlined" color="primary" onClick={() => setShowSignIn(true)} sx={{ margin: 1 }}>
                    Sign In
                </Button>

                {showSignUp && <SignUp />}
                {showSignIn && <SignIn onSignIn={handleSignInSuccess} />}
            </Box>
        )}
    </Container>
);
}

export default App;