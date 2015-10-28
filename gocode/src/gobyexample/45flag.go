package main

import (
	"flag"
	"fmt"
	"os"
	"strings"
)

func testFlag() {
	wordPtr := flag.String("word", "foo", "a string")
	numbPtr := flag.Int("numb", 42, "an int")
	boolPtr := flag.Bool("fork", false, "a bool")
	var svar string
	flag.StringVar(&svar, "svar", "bar", "a string var")
	flag.Parse()

	fmt.Println(*wordPtr, *numbPtr, *boolPtr, svar, flag.Args())
}

func testEnv() {
	os.Setenv("FOO", "1")
	fmt.Println("FOO:", os.Getenv("FOO"))
	fmt.Println("BAR:", os.Getenv("BAR"))

	// 使用 `os.Environ` 来列出所有环境变量键值队。这个函数
	// 会返回一个 `KEY=value` 形式的字符串切片。你可以使用
	// `strings.Split` 来得到键和值。这里我们打印所有的键。
	fmt.Println()
	for _, e := range os.Environ() {
		pair := strings.Split(e, "=")
		fmt.Println(pair[0])
	}
}
