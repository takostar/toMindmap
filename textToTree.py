# coding=utf-8
'''
@Author: tako star
@Date: 2020-04-09 13:37:48
@LastEditors: tako star
@LastEditTime: 2020-05-17 15:29:41
'''
from regex import sub, match, split
from freemind import mm
import yaml
from listToXmind import listToXmind
# from re import match, split


class mindmap:
    text = ''
    sortSignal = []
    textList = []
    tree = []

    def __init__(self):
        self.textInput()
        self.initSignal()
        self.addNewlines()
        self.saveToList()

    def textInput(self):
        with open('src/心理学与生活.txt', 'r', encoding='utf-8') as f:
            self.text = f.read()

    def initSignal(self):
        def charSignalInit(signal,
                           chars=[
                               '一', '二', '三', '四', '五', '六', '七', '八', '九',
                               '十', '十一', '十二', '十三', '十四', '十五', '十六', '十七',
                               '十八', '十九', '二十'
                           ]):
            charSignal = []
            for char in chars:
                charSignal.append(signal.format(char))
            self.sortSignal.append(charSignal)

        def numSignalInit(preSignal, intRange):
            numSignal = []
            for i in range(intRange[0], intRange[1]):
                numSignal.append(preSignal.format(i))
            self.sortSignal.append(numSignal)

        file = open('signal.yml', 'r', encoding="utf-8")
        file_data = file.read()
        data = yaml.load(file_data)
        serials = data['serials']
        single = serials['single']
        # todo:single待处理
        multiple = serials['multiple']
        seqSentences = data['seqSentence']
        for multi in multiple:
            multiList = []
            multiList = multi.split()
            for seqSentence in seqSentences:
                # todo:回忆此处\s的作用
                seqSentence = '\s' + seqSentence
                numSignalInit(seqSentence, (1, 20))
                charSignalInit(seqSentence, multiList)
        # *由于只匹配句首,所以不必担心与小数混淆

    def addNewlines(self):
        # 匹配分类字符,并对字符进行替换
        for signaList in self.sortSignal:
            for signal in signaList:
                self.text = sub(signal, '\n' + signal, self.text)

    def saveToList(self):
        self.textList = split('\n|\x20{4,10}|\u3000\u3000', self.text)

    def saveToTree(self, textList):
        def findSignals(textList):
            for text in textList:
                for signaList in self.sortSignal:
                    if (match(signaList[0][2:], text[2:]) is not None):
                        # 此时成功匹配
                        return textList.index(text), signaList
            return -1, -1

        def findSignal(textList, signaList):
            info = []
            for text in textList:
                for signal in signaList:
                    if (match(signal[2:], text[2:]) is not None):
                        info.append(
                            (textList.index(text), signaList.index(signal)))
            return info

        index, signaList = findSignals(textList)
        if (index == -1):
            return textList
        parentList = []
        childList = []
        for i in range(0, index):
            parentList.append(textList[i])
        for i in range(index, len(textList)):
            childList.append(textList[i])
        # *先确定各种划分符号个数,再进行处理
        info = findSignal(childList, signaList)

        def delInSeq(info, top=0, corrent=1):
            # TODO:假如只有一个(理论上不可能出现,因为这么做没意义)
            # TODO:但实际上会出现这种情况
            if (len(info) - 1 > corrent and corrent != 0):
                if (info[corrent - 1][1] == info[corrent + 1][1] - 1
                        and (info[corrent][1] == info[corrent - 1][1]
                             or info[corrent][1] == info[corrent - 1][1] + 1)):
                    return corrent, corrent
            if (info[corrent][1] != info[corrent - 1][1] + 1):
                # *假如当前与前一个非顺位,更新top
                top = corrent
            if (len(info) <= corrent + 1):
                return top, corrent
            if (info[corrent][1] == info[corrent + 1][1] - 1):
                return delInSeq(info, top, corrent + 1)
            else:
                return top, corrent

        while (len(info) != info[len(info) - 1][1] + 1):
            top, bottom = delInSeq(info)
            # if (info[0][1] == info[1][1] and info[1][1] + 1 == info[2][1]):
            #     info.pop[0]
            for i in range(top, bottom + 1):
                # !由于每次弹出后顺序都会改变
                info.pop(top)
            if (len(info) == 0):
                List = []
                List.append(childList[0])
                for i in range(1, len(childList)):
                    List.append(childList[i])
                parentList.append[List]
        # *到此成功获取了相应符号的位置
        info.append((len(childList), -1))
        for i in range(1, len(info)):
            subList = []
            for n in range(info[i - 1][0] + 1, info[i][0]):
                subList.append(childList[n])
            List = []
            # 此处添加的为字符串
            List.append(childList[info[i - 1][0]])
            subList = self.saveToTree(subList)
            List.append(subList)
            parentList.append(List)
        return parentList

    # learn:字典数组等为引用变量!


if __name__ == "__main__":
    map = mindmap()
    filename = '心理学与生活'
    tree = map.saveToTree(map.textList)
    # freemindMap = mm(tree)
    # freemindMap.saveMap(filename)
    xmindfile = listToXmind(tree)
    xmindfile.saveMap(filename)
    print("成功完成" + filename + "文件的输出!")
