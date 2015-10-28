package main

import "fmt"
import "time"

func Channel() {
	messages := make(chan string)
	go func() {
		messages <- "ping"
	}()
	msg := <-messages
	fmt.Println(msg)
}

func Channel2() {
	messages := make(chan string, 2)
	messages <- "buffered"
	messages <- "channeld"
	fmt.Println(<-messages)
	fmt.Println(<-messages)
}

func worker(done chan bool) {
	fmt.Println("working...")
	time.Sleep(time.Second)
	fmt.Println("done")
	done <- true
}

func Channel3() {
	done := make(chan bool) //不带缓冲
	go worker(done)
	fmt.Println(<-done)
}

/*chan<-能写。<-chan能读*/
func ping(pings chan<- string, msg string) {
	pings <- msg
}

func pong(pings <-chan string, pongs chan<- string) {
	pongs <- <-pings
}

func Channel4() {
	pings := make(chan string, 1) //带缓冲
	pongs := make(chan string, 1)
	ping(pings, "passed message")
	pong(pings, pongs)
	fmt.Println(<-pongs)
}

func Channel5() {
	jobs := make(chan int, 5)
	done := make(chan bool)

	go func() {
		for {
			j, more := <-jobs
			if more {
				fmt.Println("receive job", j)
			} else {
				fmt.Println("receive all jobs")
				done <- true
				return
			}
		}
	}()

	for j := 1; j <= 3; j++ {
		jobs <- j
		fmt.Println("sent job", j)
	}
	close(jobs) //关闭通道
	fmt.Println("sent all jobs")
	<-done
}

func Channel6() {
	queue := make(chan string, 2)
	queue <- "one"
	queue <- "two"
	close(queue)

	for elem := range queue {
		fmt.Println(elem)
	}
}
