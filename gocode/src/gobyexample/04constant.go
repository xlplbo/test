package main

import "fmt"
import "math"

const cs string = "constant"

func constant() {
	fmt.Println(cs)

	const n = 500000000

	const d = 3e20 / n
	fmt.Println(d)
	fmt.Println(int64(d))
	fmt.Println(math.Sin(n))
}
