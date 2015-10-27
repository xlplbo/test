package main

import "fmt"

type person struct {
	name string
	age  int
	say  func(string, int) bool
}

func (p *person) sayhello() bool {
	fmt.Println("hello everyone")
	fmt.Printf("My name is %s, My age is %d\n", p.name, p.age)
	return true
}

func sayhello(name string, age int) bool {
	fmt.Println("hello everyone")
	fmt.Printf("My name is %s, My age is %d\n", name, age)
	return true
}

func Struct() {
	fmt.Println(person{"Bob", 20, sayhello})
	fmt.Println(person{name: "Alice", age: 30})
	fmt.Println(person{name: "Fred"})
	fmt.Println(&person{name: "Ann", age: 40})

	s := person{name: "Sean", age: 50, say: sayhello}
	fmt.Println(s.name)

	sp := &s
	fmt.Println(sp.age)

	sp.age = 51
	fmt.Println(s)

	sp.say(sp.name, sp.age)
	sp.sayhello()
}
