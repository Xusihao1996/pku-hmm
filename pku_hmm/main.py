import sys
import math

A_dic = {}  # 状态转移概率矩阵
B_dic = {}  # 观测概率矩阵
Count_dic = {}  # 用于记录所有B、M、E、S的数量
Pi_dic = {}  # 初始概率矩阵，即记录了每个字是BMSE的概率
word_set = set()  # 所有词语的集合
state_list = ['B', 'M', 'E', 'S']
line_num = -1
INPUT_DATA = "trainCorpus.txt_utf8"
PROB_START = "prob_start.py"  # 初始状态概率
PROB_EMIT = "prob_emit.py"  # 发射概率
PROB_TRANS = "prob_trans.py"  # 转移概率


# 初始化字典，初始化的矩阵A全部为0
def init():
    for state in state_list:
        A_dic[state] = {}
        for state1 in state_list:
            A_dic[state][state1] = 0.0
    for state in state_list:
        Pi_dic[state] = 0.0
        B_dic[state] = {}
        Count_dic[state] = 0


# 输出观测状态
def getList(input_str):
    outpout_str = []
    if len(input_str) == 1:
        outpout_str.append('S')
    elif len(input_str) == 2:
        outpout_str = ['B', 'E']
    else:
        M_num = len(input_str) - 2
        M_list = ['M'] * M_num
        outpout_str.append('B')
        outpout_str.extend(M_list)  # 把M_list中的'M'分别添加进去
        outpout_str.append('E')
    return outpout_str


# 输出模型的三个矩阵
def Output():
    start_fp = open(PROB_START, 'w')
    emit_fp = open(PROB_EMIT, 'w')
    trans_fp = open(PROB_TRANS, 'w')
    for key in Pi_dic:  # 状态的初始概率
        Pi_dic[key] = float(Pi_dic[key]) / line_num
    print(Pi_dic, file=start_fp)
    for key in A_dic:  # 状态转移概率
        for key1 in A_dic[key]:
            A_dic[key][key1] = A_dic[key][key1] / Count_dic[key]
    print(A_dic, file=trans_fp)
    for key in B_dic:  # 观测概率，
        for word in B_dic[key]:
            B_dic[key][word] = B_dic[key][word] / Count_dic[key]
    print(B_dic, file=emit_fp)
    start_fp.close()
    emit_fp.close()
    trans_fp.close()


def main():
    ifp = open(INPUT_DATA, 'rb')
    init()
    global word_set
    global line_num
    for line in ifp.readlines():
        line_num += 1
        line = line.strip()
        if not line: continue
        line = line.decode("utf-8", "ignore")
        word_list = []
        for i in range(len(line)):
            if line[i] == " ": continue
            word_list.append(line[i])
        word_set = word_set | set(word_list)  # 训练预料库中所有字的集合
        lineArr = line.split(" ")  # 每一行的字符串
        line_state = []  # 用于存放每个字符的BMSE属性
        for item in lineArr:
            line_state.extend(getList(item))
        for i in range(len(line_state)):  # 遍历这个字符串的所有BMSE
            if i == 0:
                Pi_dic[line_state[0]] += 1
                Count_dic[line_state[0]] += 1  # 记录每一个状态的出现次数
            else:
                A_dic[line_state[i - 1]][line_state[i]] += 1  # 用于计算转移概率
                Count_dic[line_state[i]] += 1
                if word_list[i] not in B_dic[line_state[i]]:
                    B_dic[line_state[i]][word_list[i]] = 0.0
                else:
                    B_dic[line_state[i]][word_list[i]] += 1  # 用于计算发射概率
    Output()
    ifp.close()


if __name__ == "__main__":
    main()

