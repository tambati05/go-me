package main

import "fmt"

// Defer example
func deferExample() {
	defer fmt.Println("Defer executed last")
	fmt.Println("Defer executed first")
}

// Pointer example
func pointerExample() {
	x := 10
	ptr := &x
	*ptr = 20
	fmt.Println("Value of x after pointer change:", x)
}

func main() {
	// Infinite loop with a break
	fmt.Println("Infinite Loop:")
	i := 0
	for {
		i++
		if i > 2 {
			break
		}
		fmt.Println(i)
	}

	// While-like loop
	fmt.Println("\nWhile-like Loop:")
	j := 1
	for j <= 3 {
		fmt.Println(j)
		j++
	}

	// If statement
	fmt.Println("\nIf Statement:")
	x := 10
	if x > 5 {
		fmt.Println("x is greater than 5")
	}

	// For loop with range (for slices)
	fmt.Println("\nFor Loop with Range:")
	numbers := []int{1, 2, 3}
	for _, num := range numbers {
		fmt.Println(num)
	}

	// Defer example
	fmt.Println("\nDefer Example:")
	deferExample()

	// Pointer example
	fmt.Println("\nPointer Example:")
	pointerExample()

	// Switch statement
	fmt.Println("\nSwitch Statement:")
	switch x {
	case 1:
		fmt.Println("x is 1")
	case 10:
		fmt.Println("x is 10")
	default:
		fmt.Println("x is something else")
	}
}
