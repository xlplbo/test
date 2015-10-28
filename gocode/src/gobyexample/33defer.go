package main

import "fmt"
import "os"

func Defer() {
	f := createFile("defer.txt")
	defer closeFile(f)
	writeFile(f)
}

func createFile(p string) *os.File {
	fmt.Println("create file")
	f, err := os.Create(p)
	if err != nil {
		panic(err)
	}
	return f
}

func closeFile(f *os.File) {
	fmt.Println("close file")
	f.Close()
}

func writeFile(f *os.File) {
	fmt.Println("write file")
	fmt.Fprintln(f, "data")
}
