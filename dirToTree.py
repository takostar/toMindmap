# coding=utf-8
'''
@Author: tako star
@Date: 2020-04-13 10:26:07
@LastEditors: tako star
@LastEditTime: 2020-04-14 21:03:57
'''
from freemind import mm
import os
# learn:改变控制台背景颜色的模块
from colorama import init
# learn:改变控制台字体颜色的模块
from termcolor import colored
from listToXmind import listToXmind


class Dir:
    dirList = []

    def __init__(self, topPath=os.getcwd()):
        self.dirList = self.check_file(topPath, self.dirList)

    def check_file(self, path, dirList, call=1):
        folders_and_files = os.listdir(path)
        subList = []
        # *开始遍历目录
        for element in folders_and_files:
            if os.path.isfile(path + "/" + element):
                subList.append(element)
                print(colored("- " * call + " " + element, 'blue'))
        # *分两次为了实现"字符串在列表前面"
        # TODO:考虑优化freemind模块适配列表字符串的前后关系
        # TODO:其他数据结构
        for element in folders_and_files:
            if os.path.isdir(path + "/" + element):
                print(colored("- " * call + " " + element, 'green'))
                leastList = []
                leastList.append(element)
                self.check_file(path + "/" + element, leastList, call + 1)
                subList.append(leastList)
        # *目录遍历结束
        dirList.append(subList)
        return dirList


if __name__ == "__main__":
    tree = Dir()
    print(tree.dirList)
    # freemindMap = mm(tree.dirList, '文件目录树')
    # freemindMap.saveMap('文件目录树')
    xmind = listToXmind(tree.dirList)
    xmind.saveMap("文件目录树")
    print("成功完成文件目录树文件的输出!")