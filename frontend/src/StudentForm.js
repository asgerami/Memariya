// frontend/src/StudentForm.js
import React, { useState } from 'react';
import { TextField, Button, Container, Box } from '@mui/material';
import axios from 'axios';

function StudentForm({ onCreate }) {  // Add onCreate prop
    const [learningStyle, setLearningStyle] = useState('');
    const [preferredSubjects, setPreferredSubjects] = useState('');
    const [interests, setInterests] = useState('');
    const [academicLevel, setAcademicLevel] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault(); // Prevent default form submission
        try {
            const newStudent = {
                learning_style: learningStyle,
                preferred_subjects: JSON.parse(preferredSubjects),
                interests: JSON.parse(interests),
                academic_level: JSON.parse(academicLevel),
            };

            const response = await axios.post('http://localhost:8000/students/', newStudent);

            if (response.status === 200) {
                console.log('Student created successfully:', response.data);
                //Reset the form
                setLearningStyle('');
                setPreferredSubjects('');
                setInterests('');
                setAcademicLevel('');

                if (onCreate) {
                    onCreate(response.data);  // Call the onCreate function
                }

                alert("Student created successfully!")
            } else {
                console.error('Failed to create student:', response.status);
                alert(`Failed to create student: ${response.status}`)
            }
        } catch (error) {
            console.error('Error creating student:', error);
            alert(`Error creating student: ${error.message}`);
        }
    };

    return (
        <Container maxWidth="md">
            <Typography variant="h4" align="center" gutterBottom>Create New Student</Typography>
            <form onSubmit={handleSubmit}>
                <TextField
                    label="Learning Style"
                    fullWidth
                    margin="normal"
                    required
                    value={learningStyle}
                    onChange={(e) => setLearningStyle(e.target.value)}
                />
                <TextField
                    label="Preferred Subjects (JSON)"
                    fullWidth
                    margin="normal"
                    required
                    value={preferredSubjects}
                    onChange={(e) => setPreferredSubjects(e.target.value)}
                    placeholder='{"Math": "Advanced", "Science": "Intermediate"}'
                />
                <TextField
                    label="Interests (JSON)"
                    fullWidth
                    margin="normal"
                    required
                    value={interests}
                    onChange={(e) => setInterests(e.target.value)}
                    placeholder='["Coding", "Robotics", "Gaming"]'
                />
                <TextField
                    label="Academic Level (JSON)"
                    fullWidth
                    margin="normal"
                    required
                    value={academicLevel}
                    onChange={(e) => setAcademicLevel(e.target.value)}
                    placeholder='{"Math": "12", "Science": "11"}'
                />
                <Button variant="contained" color="primary" type="submit">
                    Create Student
                </Button>
            </form>
        </Container>
    );
}

export default StudentForm;