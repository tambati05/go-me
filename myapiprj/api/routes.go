package api

import (
	"database/sql"
	"net/http"
)

// RegisterRoutes sets up the HTTP routes for the college database.
func RegisterRoutes(db *sql.DB) {
	http.HandleFunc("/create", CreateStudentHandler(db))
	http.HandleFunc("/students", GetStudentsHandler(db))
}
