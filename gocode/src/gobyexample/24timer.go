package main

import "fmt"
import "time"

func Timer() {
	fmt.Println("Timer Begin")
	time.Sleep(time.Second) //单纯的等待

	fmt.Println("New Timer 1")
	timer1 := time.NewTimer(time.Second * 2)
	<-timer1.C //通道C，在定时器失效前一直阻塞
	fmt.Println("timer1 expired")

	fmt.Println("New Timer 2")
	timer2 := time.NewTimer(time.Second)
	go func() {
		<-timer2.C
		fmt.Println("timer2 expired")
	}()
	stop2 := timer2.Stop() //取消这个定时器
	if stop2 {
		fmt.Println("timer2 stoped")
	}
}
