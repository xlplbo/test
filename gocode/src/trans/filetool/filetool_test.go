package filetool_test

import (
	"fmt"
	"testing"
	"trans/filetool"
)

func Test_example1(t *testing.T) {
	ft := filetool.GetInstance()
	context, _ := ft.ReadFileLine("test.txt")
	fmt.Println(len(context))
	for k, v := range context {
		fmt.Println(k, v)
	}
	ft.SaveFileLine("test.txt", context)
}

func Test_example2(t *testing.T) {
	ft := filetool.GetInstance()
	context1, _ := ft.ReadFileLine("test1.txt")
	fmt.Println(len(context1))
	for k, v := range context1 {
		fmt.Println(k, v)
	}
	ft.SaveFileLine("test1.txt", context1)
}

func Test_example3(t *testing.T) {
	ft1 := filetool.GetInstance()
	ft2 := filetool.GetInstance()
	if ft1 != ft2 {
		t.Error("GetInstance diffrent value")
	}
}

func Test_example4(t *testing.T) {
	ft := filetool.GetInstance()
	bv, _ := ft.ReadAll("t.txt")
	fmt.Println(bv)
}

func Benchmark_example(b *testing.B) {
	ft := filetool.GetInstance()
	for i := 0; i < b.N; i++ {
		context, _ := ft.ReadFileLine("test.txt")
		ft.SaveFileLine("test.txt", context)
	}
}
