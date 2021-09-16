import sys
from pypinyin import pinyin, lazy_pinyin, Style, load_phrases_dict, load_single_dict
import pypinyin
from wenbenpinyinhua import *
import copy
match_list = []     # 记录找出来的敏感词
total = 0           # 记录敏感词数量
def mgccf(a, b) -> list:  # 构建敏感词库       #自定义的列表相乘函数，用于组合拼音
    c_list = [a[0][0], b[0]]
    length = len(a)
    i = 1
    while i < len(a):
        d_list = []
        mgc_list = []
        d_list.append(a[i][0])
        d_list.append(b[i])
        for c in c_list:
            for d in d_list:
                mgc_list.append(f"{c}{d}")
        c_list = mgc_list
        i += 1
    return mgc_list
def try_file_path(file_path):
    try:
        f = open(file_path, encoding='utf-8')
    except Exception as msg:
        print(msg)
        exit(0)
    else:
        f.close()
def buildmgck(filepath):               #将汉字都变成拼音，构建各种组合与敏感词相对应的敏感词库，eg：‘flg’：‘法轮功’
    try_file_path(filepath)
    mgc={}
    with open(filepath, 'r', encoding='utf_8') as file_object:
        py = []
        for line in file_object:
            if line.rstrip() == lazy_pinyin(line.rstrip())[0]:     #单词变小写，加入敏感词库
                mgc[line.rstrip().lower()] = line.rstrip()
            else:                                                 #汉字，分别转化为拼音和首字母在进行排列组合
                a = pinyin(line.rstrip(), style=pypinyin.FIRST_LETTER)
                b = lazy_pinyin(line.rstrip())
                for t in mgccf(a, b):
                    mgc[t] = line.rstrip()
    return mgc

class DFA:            #用dfa算法寻找敏感词
    def __init__(self, keyword_list: list):
        self.state_event_dict = self._generate_state_event_dict(keyword_list)  # 创建查找字典树

    def match(self, content: str, txutnum):        #查找算法
        state_list = []
        temp_match_list = []
        ceshi_list = hang(content, 1)
        for char_pos in ceshi_list.keys():
            if ceshi_list[char_pos] in self.state_event_dict:  # 查找出第一个匹配的字
                state_list.append(self.state_event_dict)  # 把构建出来的查询字典加进去
                start = char_pos  # 找出的敏感词首部位置
                temp_match_list.append({  # 第几行
                    "match": ""
                })
            char = ceshi_list[char_pos]
            for index, state in enumerate(state_list):

                if char in state:
                    state_list[index] = state[char]  # 递进一层
                    temp_match_list[index]["match"] += char
                    if state[char]["is_end"]:
                        end = char_pos  # 找出的敏感词结束位置
                        if 1 < 2:
                            mgc_value = content[start - 1:end]
                            premgc = mgc[temp_match_list[index]["match"]]
                            match_list.append(f"line{txtnum}<{premgc}>:{mgc_value}")
                            global total
                            total = total + 1  # 找出的值
                            if len(state[char].keys()) == 1:
                                state_list.pop(index)
                                temp_match_list.pop(index)
                else:
                    state_list.pop(index)
                    temp_match_list.pop(index)
                    ceshimgc = ''

        return match_list

    @staticmethod
    def _generate_state_event_dict(keyword_list: list) -> dict:           #构建查找字典树
        state_event_dict = {}

        for keyword in keyword_list:
            current_dict = state_event_dict
            length = len(keyword)

            for index, char in enumerate(keyword):
                if char not in current_dict:
                    next_dict = {"is_end": False}
                    current_dict[char] = next_dict
                    current_dict = next_dict
                else:
                    next_dict = current_dict[char]
                    current_dict = next_dict
                if index == length - 1:
                    current_dict["is_end"] = True

        return state_event_dict

if __name__ == "__main__":
    mgcflie=checkfile=ansfile=''
    if len(sys.argv) == 1:
        path_words = "words.txt"
        path_org = "org.txt"
        path_ans = "ans.txt"
    elif len(sys.argv) == 4:
        path_words=str(sys.argv[1])
        path_org=str(sys.argv[2])
        path_ans=str[sys.argv[3]]
    else:
        print("wrong")
    mgc = buildmgck(path_words)
    dfa = DFA(mgc)
    txtnum = 1
    # 记录行数
    with open(path_org, 'r' , encoding='utf-8') as cstxt:
        # 一行一行的处理，查找敏感词
        for line in cstxt:
            dfa.match(line, txtnum)
            txtnum += 1
theans = open(path_ans, 'w', encoding='utf-8')
theans.write(f"total:{total}\n")
for value in match_list:
    theans.write(f'{value}\n')

