package main

import (
	"fmt"
	"os/exec"
)

func testCommad() {
	dateCmd := exec.Command("notepad")
	dateOut, err := dateCmd.Output()
	if err != nil {
		panic(err)
	}
	fmt.Println(string(dateOut))
}
