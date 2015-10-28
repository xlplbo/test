package main

import "fmt"
import "time"

func work(id int, jobs <-chan int, results chan<- int) {
	for j := range jobs {
		fmt.Println("worker", id, "processing job", j)
		time.Sleep(time.Second)
		results <- j * 2
	}
}

func assignment(job int, jobs chan<- int) {
	fmt.Println("assignment job", job)
	jobs <- job
}

func WorkPool() {
	jobs := make(chan int, 100)
	results := make(chan int, 100)

	//启动n个goroutine
	for i := 1; i <= 10; i++ {
		go work(i, jobs, results)
	}

	//分配m个任务
	for i := 1; i <= 100; i++ {
		assignment(i, jobs)
	}

	//等待任务执行完再结束
	for {
		select {
		case <-results:
		case <-time.After(time.Second * 5):
			fmt.Println("timeout")
			return
		}
	}

	//	for j := 0; j < 100; j++ {
	//		<-results
	//	}
}
