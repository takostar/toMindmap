# coding=utf-8
'''
@Author: tako star
@Date: 2020-04-10 10:02:04
@LastEditors: tako star
@LastEditTime: 2020-04-14 20:16:51
'''
import xml.etree.ElementTree as ET
from regex import match


class mm:
    idList = []
    map

    def __init__(self, textList, rootText='思维导图'):
        root = self.initTree(rootText)
        # 此函数运行完毕后,数已经生成,调用saveMap函数即可
        self.parseTree(textList, root)

    def initTree(self, title):
        # 在内存中创建一个空的文档
        self.map = ET.Element('map')
        root = ET.SubElement(self.map, 'node')
        root.set('ID', 'root')
        root.set('TEXT', title)
        return root
        # 创建一个根节点对象

    def parseTree(self, textList, Element):
        # *传入父元素
        # *无论字符串多个或零个,列表也可以有多个或零个,且一定在所有字符串后面
        # *因此,当有列表长为n>=2时,字符串数为n-1,而列表数为1或字符串数为n,列表数为0
        # *假如为文本则加入元素,否则加入下一层

        toDel = ['', '\u3000', '\x20']
        for signal in toDel:
            for i in range(0, textList.count(signal)):
                textList.remove(signal)
        strNum = 0
        length = len(textList)
        for text in textList:
            if (type(text) == str):
                strNum += 1
        for i in range(0, strNum):
            if (match('\\\s', textList[i])):
                textList[i] = textList[i][2:]
            subElement = ET.SubElement(Element, 'node')
            subElement.set('TEXT', textList[i])
        if (strNum != length):
            if (strNum == 0):
                subElement = Element
            for i in range(strNum, length):
                self.parseTree(textList[i], subElement)

    def saveMap(self, filename='output'):
        tree = ET.ElementTree(self.map)
        tree.write('output/' + filename + '.mm')

    def genID(self):
        # !由于对于freemind和xmind软件id都非必要,所以不设置了(其他属性如style,fork,position等同理)
        id = 0
        # *生成16位16进制id并比较idList中的已存在项
        return id


if __name__ == "__main__":
    testList = ['1', ['2', '3']]
    mindmap = mm(testList)
    mindmap.saveMap()
