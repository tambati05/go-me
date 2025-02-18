package main

import "fmt"

func main() {
	var num1, num2, choice int

	fmt.Print("Enter first number: ")
	fmt.Scan(&num1)
	fmt.Print("Enter second number: ")
	fmt.Scan(&num2)

	fmt.Println("\nChoose an operation:")
	fmt.Println("1. Add")
	fmt.Println("2. Subtract")
	fmt.Println("3. Multiply")
	fmt.Println("4. Divide")
	fmt.Print("Enter your choice: ")
	fmt.Scan(&choice)

	switch choice {
	case 1:
		fmt.Println("Sum:", add(num1, num2))
	case 2:
		fmt.Println("Subtract:", subtract(num1, num2))
	case 3:
		fmt.Println("Multiply:", multiply(num1, num2))
	case 4:
		fmt.Println("Divide:", divide(num1, num2))
	default:
		fmt.Println("Invalid choice")
	}

}
