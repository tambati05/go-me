package main

import "fmt"

func add(a int, b int) int {
	return a + b
}
func subtract(a int, b int) int {
	return a - b
}
func multiply(a int, b int) int {
	return a * b
}
func divide(a int, b int) float64 {
	if b != 0 {
		return float64(a) / float64(b)
	} else {
		fmt.Println("Error: Division by zero")
		return 0
	}
}
