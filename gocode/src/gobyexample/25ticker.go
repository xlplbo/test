package main

import "fmt"
import "time"

func Ticker() {
	ticker := time.NewTicker(time.Millisecond * 500)
	go func() {
		//通道遍历直到ticker停止
		for t := range ticker.C {
			fmt.Println("tick at", t)
		}
	}()

	time.Sleep(time.Second * 2)
	ticker.Stop()
	fmt.Println("ticker stopped")
}
