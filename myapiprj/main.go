package main

import (
	"database/sql"
	"fmt"
	"log"
	"myapiprj/api"
	"net/http"

	_ "github.com/go-sql-driver/mysql"
)

func main() {

	dsn := "root:Agrambati@123@tcp(127.0.0.1:3306)/college?parseTime=true"

	// Open a connection to the MySQL database
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		log.Fatal("Error opening database: ", err)
	}
	defer db.Close()

	// Verify the connection is valid
	if err := db.Ping(); err != nil {
		log.Fatal("Error pinging database: ", err)
	}

	fmt.Println("Connection to the college database established successfully!")

	// Register API routes
	api.RegisterRoutes(db)
	fmt.Println("API routes registered successfully!")

	// Start the HTTP server on port 8080
	log.Println("Server is running on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
