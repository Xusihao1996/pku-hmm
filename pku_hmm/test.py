# -*- coding: utf-8 -*-
def load_model(f_name):
    ifp = open(f_name, 'rb').read()
    ifp = ifp.decode('GB2312', "ignore")
    return eval(ifp)


import chardet

file = open("prob_emit.py", 'rb').read()
f_charInfo = chardet.detect(file)
print(f_charInfo)
prob_start = load_model("prob_start.py")
prob_trans = load_model("prob_trans.py")
prob_emit = load_model("prob_emit.py")


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
    for y in states:  # 初始值
        V[0][y] = start_p[y] * emit_p[y].get(obs[0], 0)
        path[y] = [y]
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
        for y in states:  # 从y0 -> y状态的递归
            (prob, state) = max(
                [(V[t - 1][y0] * trans_p[y0].get(y, 0) * emit_p[y].get(obs[t], 0), y0) for y0 in states if
                 V[t - 1][y0] > 0])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath  # 记录状态序列
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])  # 在最后一个位置，以y状态为末尾的状态序列的最大概率
    return (prob, path[state])  # 返回概率和状态序列


def cut(sentence):
    prob, pos_list = viterbi(sentence, ('B', 'M', 'E', 'S'), prob_start, prob_trans, prob_emit)
    return (prob, pos_list)

def main():
    sentence = '我爱中国'
    result = cut(sentence)
    final = open("test.txt", 'w')
    print(result, file=final)


if __name__ == "__main__":
    main()
