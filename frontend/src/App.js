import React, { useState, useEffect } from "react";
import { Container, Typography, TextField, Button, Box } from "@mui/material";
import axios from "axios";

function App() {
  const [studentId, setStudentId] = useState("");
  const [student, setStudent] = useState(null);
  const [concept, setConcept] = useState("");
  const [explanation, setExplanation] = useState("");

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
  }, [studentId]);

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

  return (
    <Container maxWidth="md">
      <Typography variant="h4" align="center" gutterBottom>
        Personalized Learning Assistant
      </Typography>

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
          {/* Display other student profile details */}
        </Box>
      )}

      <TextField
        label="Concept to Explain"
        value={concept}
        onChange={(e) => setConcept(e.target.value)}
        fullWidth
        margin="normal"
      />

      <Button
        variant="contained"
        color="primary"
        onClick={handleGenerateExplanation}
      >
        Generate Explanation
      </Button>

      {explanation && (
        <Box mt={2}>
          <Typography variant="h6">Explanation</Typography>
          <Typography>{explanation}</Typography>
        </Box>
      )}
    </Container>
  );
}

export default App;
