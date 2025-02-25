package main

import "fmt"

// Define the Temperature struct with a Value field
type Temperature struct {
	Value float64
}

// Method to convert Celsius to Fahrenheit
func (t *Temperature) ToFahrenheit() float64 {
	return (t.Value * 9 / 5) + 32
}

// Method to convert Fahrenheit to Celsius
func (t *Temperature) ToCelsius() float64 {
	return (t.Value - 32) * 5 / 9
}

func main() {
	var temp float64
	var choice int

	// Ask the user for the temperature and conversion choice
	fmt.Print("Enter the temperature value: ")
	fmt.Scan(&temp)

	fmt.Println("Choose conversion:")
	fmt.Println("1. Celsius to Fahrenheit")
	fmt.Println("2. Fahrenheit to Celsius")
	fmt.Print("Enter your choice (1 or 2): ")
	fmt.Scan(&choice)

	tempStruct := &Temperature{Value: temp}

	if choice == 1 {
		fahrenheit := tempStruct.ToFahrenheit()
		fmt.Printf("%.2f Celsius is %.2f Fahrenheit\n", temp, fahrenheit)
	} else if choice == 2 {
		celsius := tempStruct.ToCelsius()
		fmt.Printf("%.2f Fahrenheit is %.2f Celsius\n", temp, celsius)
	} else {
		fmt.Println("Invalid choice")
	}
}
