package main

import (
	"fmt"
	"sort"
)

func Sort() {
	strs := []string{"c", "a", "b"}
	sort.Strings(strs)
	fmt.Println("Strings:", strs)

	ints := []int{7, 2, 4}
	sort.Ints(ints)
	fmt.Println("Ints:", ints)
	fmt.Println("Sorted:", sort.IntsAreSorted(ints))
}

/*自定义结构排序*/
type test struct {
	id   int
	name string
}

type testSort []*test

func (t testSort) Len() int {
	return len(t)
}

func (t testSort) Swap(i, j int) {
	t[i], t[j] = t[j], t[i]
}

func (t testSort) Less(i, j int) bool {
	return t[i].id < t[j].id
}

func UseSort() {
	t := []*test{&test{id: 7, name: "hehe"}, &test{id: 2, name: "haha"}, &test{id: 4, name: "wuwu"}}
	sort.Sort(testSort(t))
	fmt.Println("Sorted:", t[0], t[1], t[2])
}
