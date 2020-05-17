# 文本转思维导图

## 说明

### textToTree 模块说明

- 将文本依据一、二、三、四、或 1.2.3.等标识进行划分并转换成列表树,可以进一步通过 freemind 模块转化成思维导图 freemind 的 mm 格式

- 适合将排布严密的电子书直接转化成列表树,通过 freemind 模块转化成思维导图,便于学习
- 可能会出现排布错误,进一步处理自行导入 xmind 进行自行处理

### dirToTree 模块说明

- 遍历指定的目录,生成列表树
- 在这个[模块]上稍作修改得到的

[模块]: https://github.com/jakub0301/DirectoryTree

### freemind 模块说明

- 将制定格式的列表树转化成 mm 格式的思维导图文件输出

### listToXmind 模块说明

- 将制定格式的列表树转化成 xmind 格式的思维导图文件输出

## 其他

程序测试使用的[文本]

输出的效果:

[文本输出]: /output/心理学与生活.xmind
[目录输出]: /output/文件目录树.xmind

- [文本输出]
  ![输出效果_文本.png](/src/输出效果_文本.png)
- [目录输出]
  ![输出效果_目录.png](/src/输出效果_目录.png)

[文本]: /src/心理学与生活.txt

## TODO

- [x] 添加通过 yaml 从外部控制 textToTree 中划分符号的设置功能
- [ ] 优化 textToTree 中部分深度分支未划分的问题
- [ ] 为 dirToTree 模块添加文件类型和文件名排除功能
- [x] 使用 python 的 xmind 模块添加对 xmind 导出的实现
- [ ] 增强模块的范用性
- [ ] 修复dirToTree中目录判断的问题

<!--
 * @Author: tako star
 * @Date: 2020-04-11 12:48:00
 * @LastEditors: tako star
 * @LastEditTime: 2020-04-14 21:05:36
 -->
