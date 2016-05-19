package main

import (
	"fmt"
	"log"
	"trans/analysis"
	"trans/filetool"
)

func main() {
	text, err := filetool.GetInstance().ReadAll("./analysis/test.lua")
	if err != nil {
		log.Fatalln(err.Error())
	}
	cdm := analysis.GetInstance().Analysis(text)
	for _, v := range *cdm {
		fmt.Printf("%v\n", v)
	}
}
