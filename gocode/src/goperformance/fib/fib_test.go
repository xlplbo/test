package fib_test

import (
    "testing"
    "goperformance/fib"
)

func Test_Fib(t *testing.T) {
    println(fib.Fib(40))
}

func Test_Fib2(t *testing.T)  {
    println(fib.Fib2(40))
}

func Test_Fib3(t *testing.T)  {
    println(fib.Fib3(40))
}

func Benchmark_Fib(b *testing.B) {
    for i := 0; i < b.N; i++ {
        fib.Fib(i%40)
    }
}

func Benchmark_Fib2(b *testing.B) {
    for i := 0; i < b.N; i++ {
        fib.Fib2(i%40)
    }
}

func Benchmark_Fib3(b *testing.B) {
    for i := 0; i < b.N; i++ {
        fib.Fib3(i%40)
    }
}
