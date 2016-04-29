package fib_test

import (
    "testing"
    "fmt"
    "fib"
)

func Test_Fib(t *testing.T) {
    for i := 1; i <= 30; i++ {
        fmt.Println(i, fib.Fib(i))
    }
}

func Test_Fib2(t *testing.T)  {
    for i := 1; i <= 30; i++ {
        fmt.Println(i, fib.Fib2(i))
    }
}

func Test_Fib3(t *testing.T)  {
    for i := 1; i <= 30; i++ {
        fmt.Println(i, fib.Fib3(i))
    }
}

func Benchmark_Fib(b *testing.B) {
    for i := 0; i < b.N; i++ {
        fib.Fib(30)
    }
}

func Benchmark_Fib2(b *testing.B) {
    for i := 0; i < b.N; i++ {
        fib.Fib2(30)
    }
}

func Benchmark_Fib3(b *testing.B) {
    for i := 0; i < b.N; i++ {
        fib.Fib3(30)
    }
}
