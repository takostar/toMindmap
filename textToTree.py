# coding=utf-8
'''
@Author: tako star
@Date: 2020-04-09 13:37:48
@LastEditors: tako star
@LastEditTime: 2020-05-19 11:55:21
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

    def __init__(self, path):
        '''初始化'''
        def textInput(path):
            '''读取文本'''
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()

        def saveToList(text):
            '''根据空格等符号将文本划分成list'''
            return split('\n|\x20{4,10}|\u3000\u3000', text)

        def addNewlines(text, sortSignal):
            '''匹配文本中的结构性符号,添加换行以便之后划分成list'''
            for signaList in sortSignal:
                for signal in signaList:
                    text = sub(signal, '\n' + signal, text)
            return text

        self.text = textInput(path)
        self.initSignal()
        self.text = addNewlines(self.text, self.sortSignal)
        self.textList = saveToList(self.text)

    def initSignal(self):
        '''初始化结构性字段'''
        def charSignalInit(signal,
                           chars=[
                               '一', '二', '三', '四', '五', '六', '七', '八', '九',
                               '十', '十一', '十二', '十三', '十四', '十五', '十六', '十七',
                               '十八', '十九', '二十'
                           ]):
            '''传入模板和顺序字符序列,生成结构性字段添加到类中'''
            charSignal = []
            for char in chars:
                charSignal.append(signal.format(char))
            self.sortSignal.append(charSignal)

        def numSignalInit(preSignal, intRange):
            '''传入模板和数字范围,生成结构性字段添加到类中'''
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

    def saveToTree(self, textList):
        '''核心部分,将list转换成list树为转换导图做准备'''
        def findSignals(textList):
            '''寻找第个出现的结构性符号,返回该符号在的行列,及匹配到的符号所在列表'''
            for text in textList:
                for signaList in self.sortSignal:
                    if (match(signaList[0][2:], text[2:]) is not None):
                        # 此时成功匹配
                        return textList.index(text), signaList
            return -1, -1

        def findSignal(textList, signaList):
            '''返回查找结构符号后,返回结构信息:元组(表示从一个符号在文本列表的位置,符号索引)'''
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
        # *到此完成初步划分(此处可能有缺陷)
        # *先确定各种划分符号个数,再进行处理
        info = findSignal(childList, signaList)

        def delInSeq(info, top=0, current=1):
            '''
            最重要的核心函数(待改进)
            获取结构符号中导致序列非连续的子部分的位置(如123123456->123[1234]456)
            '''
            # *current表示当前的符号次序
            # TODO:假如只有一个(理论上不可能出现,因为这么做没意义)
            # TODO:但实际上会出现这种情况
            # *特殊结束条件
            if (len(info) - 1 > current and current != 0):
                if (info[current - 1][1] == info[current + 1][1] - 1
                        and (info[current][1] == info[current - 1][1]
                             or info[current][1] == info[current - 1][1] + 1)):
                    return current, current
            if (info[current][1] != info[current - 1][1] + 1):
                # *假如当前结构符号与前一个非顺位,更新top
                top = current

            if (len(info) <= current + 1):
                # *当current超出范围则返回(优先判断)
                return top, current
            elif (info[current][1] == info[current + 1][1] - 1):
                # *如果与后一个顺位,则递归
                return delInSeq(info, top, current + 1)
            else:
                return current, len(info) - 1

        while (len(info) != info[-1][1] + 1):
            # *当存在的结构符号数不等于findSignal函数查找到的最后符号数(索引+1),此时需要获取多余的符号位置信息方便排除,应注意的是才此处info信息是属于childeList的

            # *此处top,bottom为要删除的部分的上限和下限
            top, bottom = delInSeq(info)
            # if (info[0][1] == info[1][1] and info[1][1] + 1 == info[2][1]):
            #     info.pop[0]
            for i in range(top, bottom + 1):
                # !进行排除(由于每次弹出后顺序都会改变)
                info.pop(top)
            if (len(info) == 0):
                # *此种情况所有结构符号均被排除,只好结束分排,悉数添加
                List = []
                List.append(childList[0])
                for i in range(1, len(childList)):
                    List.append(childList[i])
                parentList.append(List)
                break
        # *到此成功获取了相应符号的位置
        info.append((len(childList), -1))
        for i in range(1, len(info)):
            # *若len(info)<=1则不会进行,此时应该将childList中的文本行直接添加到parentList中
            subList = []
            for n in range(info[i - 1][0] + 1, info[i][0]):
                subList.append(childList[n])
            List = []
            # *此处添加的为字符串,即结构符号所在文本行,用作树的父节点
            List.append(childList[info[i - 1][0]])
            # *此处进入递归,完成subList中文本行的排布
            subList = self.saveToTree(subList)
            List.append(subList)
            # *到此,将初步划分到一起的childList细致划分成List
            parentList.append(List)
        if (len(info) <= 1):
            parentList.append(childList)
        return parentList

    # learn:字典数组等为引用变量!


if __name__ == "__main__":
    map = mindmap('myOwn/SQL.txt')
    filename = 'SQL'
    tree = map.saveToTree(map.textList)
    # freemindMap = mm(tree)
    # freemindMap.saveMap(filename)
    xmindfile = listToXmind(tree)
    xmindfile.saveMap(filename)
    print("成功完成" + filename + "文件的输出!")
