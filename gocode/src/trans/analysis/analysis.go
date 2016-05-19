package analysis

import (
	"sync"
)

type analysis struct{}

var instance *analysis
var once sync.Once

func GetInstance() *analysis {
	once.Do(func() {
		instance = &analysis{}
	})
	return instance
}

var (
	ap byte = 0x27 //单引号'
	dq byte = 0x22 //双引号"
	sl byte = 0x5c //转义斜杠\\
	bs byte = 0x2d //横杠-
	bl byte = 0x5b //左中括号[
	br byte = 0x5d //右中括号]
	cr byte = 0x0d //回车CR
	lf byte = 0x0a //换行LF
	eq byte = 0x3d //等于号=

)

const (
	state_normal          = iota //正常状态
	state_note_line              //注释一行
	state_note_section           //注释段落
	state_apostrophe             //'单引号'字符串
	state_double_quotes          //"双引号"字符串
	state_double_brackets        //[[中括号]]字符串
)

type ChData struct {
	nStart int
	nEnd   int
	szText string
}

type ChDataMap map[string]*ChData

func (a *analysis) Analysis(text []byte) *ChDataMap {
	cdm := make(ChDataMap)
	record := func(text []byte, nStart int, nEnd int) *ChData {
		bIsChinese := false
		for i := nStart; i <= nEnd; i++ {
			if text[i]&0x80 != 0 {
				bIsChinese = true
				break
			}
		}
		if bIsChinese {
			return &ChData{nStart, nEnd, string(text[nStart : nEnd+1])}
		} else {
			return nil
		}
	}
	nState := state_normal
	nStateStart := 0
	nSize := len(text)
	for i := 0; i < nSize; i++ {
		if i+1 < nSize && text[i] == sl &&
			(text[i+1] == ap || text[i+1] == dq) {
			i++
			continue
		}
		switch nState {
		case state_normal:
			switch text[i] {
			case bs:
				if i+1 < nSize && text[i+1] == bs {
					if i+3 < nSize && text[i+2] == bl {
						nPos := i + 3
						for nPos < nSize && text[nPos] == eq {
							if text[nPos] == cr || text[nPos] == lf {
								break
							}
							nPos++
						}
						if text[nPos] == bl {
							i += (nPos - i)
							nState = state_note_section
						} else {
							i += 1
							nState = state_note_line
						}
					} else {
						i += 1
						nState = state_note_line
					}
				}
			case ap:
				if i+1 < nSize && text[i+1] == ap {
					i += 1
				} else {
					nStateStart = i + 1
					nState = state_apostrophe
				}
			case dq:
				if i+1 < nSize && text[i+1] == dq {
					i += 1
				} else {
					nStateStart = i + 1
					nState = state_double_quotes
				}
			case bl:
				if i+1 < nSize && text[i+1] == bl {
					if i+3 < nSize && text[i+2] == br && text[i+3] == br {
						i += 3
					} else {
						nStateStart = i + 2
						nState = state_double_brackets
						i += 1
					}
				}
			}
		case state_note_line:
			if i+1 < nSize && text[i] == cr && text[i] == lf {
				i += 1
				nState = state_normal
			} else if text[i] == cr || text[i] == lf {
				nState = state_normal
			}
		case state_note_section:
			if text[i] == br {
				nPos := i + 1
				for nPos < nSize && text[nPos] == eq {
					if text[nPos] == cr || text[i] == lf {
						break
					}
					nPos++
				}
				if text[nPos] == br {
					i += (nPos - i)
					nState = state_normal
				}
			}
		case state_apostrophe:
			if i+1 < nSize && text[i] == cr && text[i] == lf {
				cd := record(text, nStateStart, i-1)
				if cd != nil {
					cdm[cd.szText] = cd
				}
				i += 1
				nStateStart = i + 1
			} else if text[i] == cr || text[i] == lf {
				cd := record(text, nStateStart, i-1)
				if cd != nil {
					cdm[cd.szText] = cd
				}
				nStateStart = i + 1
			} else if text[i] == ap {
				cd := record(text, nStateStart, i-1)
				if cd != nil {
					cdm[cd.szText] = cd
				}
				nState = state_normal
			}
		case state_double_quotes:
			if i+1 < nSize && text[i] == cr && text[i] == lf {
				cd := record(text, nStateStart, i-1)
				if cd != nil {
					cdm[cd.szText] = cd
				}
				i += 1
				nStateStart = i + 1
			} else if text[i] == cr || text[i] == lf {
				cd := record(text, nStateStart, i-1)
				if cd != nil {
					cdm[cd.szText] = cd
				}
				nStateStart = i + 1
			} else if text[i] == dq {
				cd := record(text, nStateStart, i-1)
				if cd != nil {
					cdm[cd.szText] = cd
				}
				nState = state_normal
			}
		case state_double_brackets:
			if i+1 < nSize && text[i] == cr && text[i] == lf {
				cd := record(text, nStateStart, i-1)
				if cd != nil {
					cdm[cd.szText] = cd
				}
				i += 1
				nStateStart = i + 1
			} else if text[i] == cr || text[i] == lf {
				cd := record(text, nStateStart, i-1)
				if cd != nil {
					cdm[cd.szText] = cd
				}
				nStateStart = i + 1
			} else if text[i] == br {
				if i+1 < nSize && text[i+1] == br {
					cd := record(text, nStateStart, i-1)
					if cd != nil {
						cdm[cd.szText] = cd
					}
					i += 1
					nState = state_normal
				}
			}
		}
	}
	return &cdm
}
