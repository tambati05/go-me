package api

import (
	"database/sql"
	"encoding/json"
	"myapiprj/database" // Adjust the import path based on your project structure
	"net/http"
)

// CreateStudentLogic processes the creation of a student.
func CreateStudentLogic(db *sql.DB, w http.ResponseWriter, r *http.Request) error {
	// Call the database function to insert a student
	return database.CreateStudent(db, w, r)
}

// GetStudentsLogic retrieves all students and writes them as JSON.
func GetStudentsLogic(db *sql.DB, w http.ResponseWriter, r *http.Request) error {
	// Fetch all students from the database
	students, err := database.GetStudents(db)
	if err != nil {
		return err
	}

	// Set the response header to JSON format
	w.Header().Set("Content-Type", "application/json")

	// Encode the students as JSON and send as response
	return json.NewEncoder(w).Encode(students)
}
