# LaTeX参考文献注意事项

- 发布时间：2025-12-30 10:26
- 类型：图文（1 张图片）
- 点赞 169 · 收藏 158 · 评论 24 · 分享 10
- 链接：https://www.xiaohongshu.com/explore/69533863000000002102b319
- 话题：参考文献 / 科研 / 科研工具 / 研究生 / 计算机

---

我相信很多同学是这样来整理参考文献的。首先建一个bib文件，然后在学术网站查找文章，点cite，找到BibTeX，复制到bib文件中。紧接着就是在正文中用\cite{name}这样的命令来进行引用。总体流程是对的，但是细节上缺漏了。很多同学并不知道学术网站提供的BibTeX不一定是格式规范且一致的。这边举个常见的例子。title这一项，有的时候每个单词首字母大写，有的时候却没有。journal或者booktitle这一项经常不一致，CVPR有时候是这样：Proceedings of the IEEE/CVF International Conference on Computer Vision，有时候是这样：Proceedings of the Computer Vision and Pattern Recognition Conference，有时候又是这样：Proceedings of the computer vision and pattern recognition conference。无论是大小写，还是具体的描述都有差别，导致参考文献的格式混乱。还有，大部分情况下不需要publisher这一项。

这边有两种方式来解决。第一种就是自行按照要求去统一，把同一个会议的booktitle都设置为一样的描述和大小写。第二种就是根据你自己要投的期刊或者会议中正式出版的文章的参考文献来微调你的BibTeX。这边还有一点值得注意，有些地方有要求journal这一项是缩写，那么我们就需要去WOS上或者是其他文章的参考文献部分找到具体是如何缩写的，然后弄到我们的bib文件中。大部分审稿人会看下参考文献，看下涉及的新的文献多不多，因此也很容易注意到格式不一致的问题，没有处理好的话，容易给审稿人留个不好的印象哦。
