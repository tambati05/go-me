package main

import "fmt"

func main() {
	// Create a slice with initial values
	numbers := []int{10, 20, 30}

	// Append a new number to the slice
	numbers = append(numbers, 40)

	// Print each number in the slice
	for _, num := range numbers {
		fmt.Println(num)
	}
}
