package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

func testSignal() {
	sigs := make(chan os.Signal, 1)
	done := make(chan bool, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		sig := <-sigs
		fmt.Println(sig)
		done <- true
	}()
	fmt.Println("awaiting signal")
	<-done
	fmt.Println("exiting")

	defer fmt.Println("test") //当使用 os.Exit 时 defer 将不会 执行，所以这里的 fmt.Println将永远不会被调用。
	os.Exit(3)
}
