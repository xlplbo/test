package main

import "os"

func Panic() {
	panic("a problem")

	_, err := os.Create("file")
	if err != nil {
		panic(err)
	}
}
