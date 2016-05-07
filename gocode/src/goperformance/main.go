package main

import (
	"goperformance/fib"
	"github.com/pkg/profile"
	// "flag"
	// "log"
	// "os"
	// "runtime/pprof"
)

// var cpuprofile = flag.String("cpuprofile", "cpu.prof", "write cpu profile to file")

func main() {
	defer profile.Start(profile.MemProfile).Stop()
	// flag.Parse()
	// f, err := os.Create(*cpuprofile)
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()
	println(fib.Fib(40))
	println(fib.Fib2(40))
	println(fib.Fib3(40))
}
