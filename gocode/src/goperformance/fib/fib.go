package fib

import "math"

func Fib(n int) int {
    if n < 2 {
        return n
    }
    return Fib(n-1) + Fib(n-2)
}

func Fib2(n int) int {
    if n < 2 {
        return n
    }
    a := 1
    b := 1
    c := 1
    for i := 2; i < n; i++ {
        c =  a + b
        a = b
        b = c
    }
    return c;
}

func Fib3(n int) int {
    gh5 := math.Sqrt(5)
    pow := math.Pow
    f := (float64)(n)
    return (int)(math.Ceil((pow(1+gh5, f) - pow(1-gh5,f)) / (pow(2.0, f) * gh5)))
}
