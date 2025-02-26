package main

import "fmt"

// Employee struct with ID, Name, and Salary fields
type Employee struct {
	ID     int
	Name   string
	Salary float64
}

// UpdateSalary updates the salary of an employee
func (e *Employee) UpdateSalary(newSalary float64) {
	e.Salary = newSalary
}

// Display prints employee details
func (e *Employee) Display() {
	fmt.Println("ID:", e.ID, "| Name:", e.Name, "| Salary:", e.Salary)
}

// AddEmployee adds an employee to the map
func AddEmployee(emp *Employee, db map[int]*Employee) {
	if _, exists := db[emp.ID]; exists {
		fmt.Println("Employee with ID", emp.ID, "already exists.")
		return
	}
	db[emp.ID] = emp
	fmt.Println("Employee added successfully!")
}

// RemoveEmployee removes an employee by ID
func RemoveEmployee(id int, db map[int]*Employee) {
	if _, exists := db[id]; exists {
		delete(db, id)
		fmt.Println("Employee with ID", id, "removed successfully!")
	} else {
		fmt.Println("Employee with ID", id, "not found.")
	}
}

func main() {
	// Initialize a map to store employees
	db := make(map[int]*Employee)

	// Adding some employees
	AddEmployee(&Employee{ID: 1, Name: "Tarun", Salary: 75000}, db)
	AddEmployee(&Employee{ID: 2, Name: "Uday", Salary: 82000}, db)
	AddEmployee(&Employee{ID: 3, Name: "Nitesh", Salary: 69000}, db)
	AddEmployee(&Employee{ID: 4, Name: "vyshnavi", Salary: 54000}, db)

	// Display employee list
	fmt.Println("\nEmployee List:")
	for _, emp := range db {
		emp.Display()
	}

	// Update salary for employee with ID 2
	fmt.Println("\nUpdating Salary for Employee ID 2:")
	if emp, exists := db[2]; exists {
		emp.UpdateSalary(87000)
		emp.Display()
	} else {
		fmt.Println("Employee not found!")
	}
	// Remove employee with ID 3
	fmt.Println("\nRemoving Employee with ID 3:")
	RemoveEmployee(3, db)

	// Display final employee list (After removal)
	fmt.Println("\nFinal List:")
	for _, emp := range db {
		emp.Display()
	}
}
