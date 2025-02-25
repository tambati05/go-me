package main

import "fmt"

// Function to generate Fibonacci sequence up to n terms
func fibonacci(n int) {
	first, second := 0, 1

	fmt.Println("Fibonacci Series:")
	for i := 0; i < n; i++ {
		fmt.Print(first, " ")
		next := first + second
		first = second
		second = next
	}
	fmt.Println() // Newline after the series
}

func main() {
	var n int
	fmt.Print("Enter the number of terms: ")
	fmt.Scan(&n)

	fibonacci(n)
}
