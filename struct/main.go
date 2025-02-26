package main

import "fmt"

// Define a struct called 'Car'
type Car struct {
	Make  string
	Model string
	Year  int
}

func main() {
	// Create an instance of the Car struct
	car1 := Car{Make: "Toyota", Model: "Corolla", Year: 2020}
	car2 := Car{Make: "Honda", Model: "Civic", Year: 2022}

	// Print details of the cars
	fmt.Println("Car 1 Details:")
	fmt.Println("Make:", car1.Make)
	fmt.Println("Model:", car1.Model)
	fmt.Println("Year:", car1.Year)

	fmt.Println("\nCar 2 Details:")
	fmt.Println("Make:", car2.Make)
	fmt.Println("Model:", car2.Model)
	fmt.Println("Year:", car2.Year)
}
