package database

import (
	"database/sql"
	"encoding/json"
	model "myapiprj/module" // Update to import the correct model package
	"net/http"
)

// CreateStudent inserts a new student record into the database.
func CreateStudent(db *sql.DB, w http.ResponseWriter, r *http.Request) error {
	var student model.Student

	// Decode the JSON request body into a Student struct.
	if err := json.NewDecoder(r.Body).Decode(&student); err != nil {
		return err
	}

	// Insert the student record into the "students" table.
	query := "INSERT INTO students(name, age, course) VALUES (?, ?, ?)"
	_, err := db.Exec(query, student.Name, student.Age, student.Course)
	if err != nil {
		return err
	}

	// Respond with the created student record.
	w.WriteHeader(http.StatusCreated)
	return json.NewEncoder(w).Encode(student)
}

// GetStudents retrieves all student records from the database.
func GetStudents(db *sql.DB) ([]model.Student, error) {
	rows, err := db.Query("SELECT id, name, age, course FROM students")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var students []model.Student
	for rows.Next() {
		var student model.Student
		if err := rows.Scan(&student.ID, &student.Name, &student.Age, &student.Course); err != nil {
			return nil, err
		}
		students = append(students, student)
	}
	return students, nil
}
