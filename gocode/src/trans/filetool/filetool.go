package filetool

import (
	"bufio"
	"errors"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"sync"
)

type filetool struct{}

var instance *filetool
var once sync.Once

func GetInstance() *filetool {
	once.Do(func() {
		instance = &filetool{}
	})
	return instance
}

func (ft *filetool) ReadFileLine(name string) ([]string, error) {
	var context []string
	f, err := os.Open(name)
	defer f.Close()
	if err != nil {
		return context, err
	}
	readline := func(r *bufio.Reader) (string, error) {
		var (
			isPrefix        bool  = true
			err             error = nil
			line, realyline []byte
		)
		for isPrefix && err == nil {
			line, isPrefix, err = r.ReadLine()
			realyline = append(realyline, line...)
		}
		return string(realyline), err
	}
	r := bufio.NewReader(f)
	err = nil
	var line string
	for err == nil {
		line, err = readline(r)
		if len(line) > 0 {
			context = append(context, line)
		}
	}
	return context, nil
}

func (ft *filetool) SaveFileLine(name string, context []string) error {
	length := len(context)
	if length < 1 {
		return errors.New("context is empty!")
	}
	f, err := os.Create(name)
	defer f.Close()
	if err != nil {
		return err
	}
	w := bufio.NewWriter(f)
	if length > 2 {
		for _, v := range context[:length-1] {
			fmt.Fprintln(w, v)
		}
	}
	fmt.Fprint(w, context[length-1])
	return w.Flush()
}

func (ft *filetool) GetFilesMap(path, filter string) (map[string]string, error) {
	filemap := make(map[string]string)
	f := func(path string, info os.FileInfo, err error) error {
		if !info.IsDir() {
			path = strings.Replace(path, "\\", "/", -1)
			pathv := strings.Split(path, "/")
			exn := strings.Split(pathv[len(pathv)-1], ".")
			if strings.EqualFold(filter, exn[len(exn)-1]) {
				filemap[path] = path
			}
			return err
		} else {
			return nil
		}
	}
	fpErr := filepath.Walk(path, f)
	if fpErr != nil {
		return nil, errors.New("Walk path Failed!")
	}
	return filemap, nil
}

func (ft *filetool) ReadAll(name string) ([]byte, error) {
	f, err := os.Open(name)
	defer f.Close()
	if err != nil {
		return []byte{}, err
	}
	return ioutil.ReadAll(f)
}
