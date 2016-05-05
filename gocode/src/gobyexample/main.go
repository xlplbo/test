package main

import (
	"fib"
	"github.com/pkg/profile"
	"time"
	//"flag"
	//"log"
	//"os"
	//"runtime/pprof"
)

//var cpuprofile = flag.String("cpuprofile", "cpu.prof", "write cpu profile to file")

func memtest(exit chan<-int) {
	tmp := make([]uint32, 1000000)
	for kk, _ := range tmp {
		tmp[kk] = 0
	}
	tmp = append(tmp, 1)
	println(len(tmp), cap(tmp))
	time.Sleep(5 * time.Second)
	exit <- 1
}

func main() {
	defer profile.Start(profile.MemProfile).Stop()
	//os.Setenv("GODEBUG", "gctrace=1")
	// for _, v := range os.Environ() {
	// 	println(v)
	// }
	// flag.Parse()
	// f, err := os.Create(*cpuprofile)
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()
	exit := make(chan int)
	go memtest(exit)
	println(fib.Fib(40))
	println(fib.Fib2(40))
	println(fib.Fib3(40))
	<-exit
	return
}
