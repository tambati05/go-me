package model

// Student represents a student entity.
type Student struct {
	ID     int    `json:"id"`
	Name   string `json:"name"`
	Age    int    `json:"age"`
	Course string `json:"course"`
}
