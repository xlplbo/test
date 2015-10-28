package main

import "fmt"
import "strings"

/*组合函数*/
func Any(vs []string, f func(string) bool) bool {
	for _, v := range vs {
		if f(v) {
			fmt.Println(v)
		}
	}
	return true
}

func CombinedFunc() {
	Any([]string{"test", "teach", "hello"}, func(v string) bool {
		return strings.HasPrefix(v, "t")
	})
}
