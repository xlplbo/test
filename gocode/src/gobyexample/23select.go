package main

import "time"
import "fmt"

func Select() {
	c1 := make(chan string)
	c2 := make(chan string)

	go func() {
		time.Sleep(time.Second * 2)
		c1 <- "one"
	}()

	go func() {
		time.Sleep(time.Second * 1)
		c2 <- "two"
	}()

	/*通道选择器select，同时等待多个通道操作，执行后结束等待*/
	for i := 0; i < 2; i++ {
		select {
		case msg1 := <-c1:
			fmt.Println(msg1)
		case msg2 := <-c2:
			fmt.Println(msg2)
		case <-time.After(time.Second * 1): //等待超时
			fmt.Println("timeout")
		}
	}
}
