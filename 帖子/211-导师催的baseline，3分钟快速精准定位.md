# 导师催的baseline，3分钟快速精准定位

- 发布时间：2025-11-11 17:21
- 类型：图文（1 张图片）
- 点赞 501 · 收藏 677 · 评论 38 · 分享 31
- 链接：https://www.xiaohongshu.com/explore/69130005000000000302df0b
- 话题：研究生 / 计算机 / 科研 / 深度学习

---

Google Scholar -> 顶会文章 -> Github搜代码 -> 测试文件/主文件看import -> 定位核心模块
1. 打开Google Scholar，输入你的研究方向，比如 Occluded Person re-identification。左侧边栏选择 按日期排序，新的文章就一目了然啦！这样能保证你找到的baseline满足新这个要求。
2. 看到心仪的文章，别急着下载！点击引用按钮，就能看到发表的期刊或会议名称。如果是CVPR, ICCV, ECCV, AAAI, NeurIPS这类领域内知名的会议，果断记录下来！这些文章的代码才具有复现价值！
3. 假设你锁定了一篇神作，比如 Attention is all you need，直接在Google输入Attention is all you need Github （中间有个空格），95%有开源代码的项目能被找到！把这些带Github链接的文章整理出来，你的baseline候选池就建立起来啦！
4. 接下来是快速定位核心模型代码。先看测试文件（test.py/eval.py），因为测试通常比训练简单很多，代码结构更清晰。目光锁定最顶部的 import 部分。通常，作者会创建一个以文章缩写命名的模块（比如 from models import vit），这个就是你要找的核心模型！
5. 如果在测试文件里没找到，这说明模型导入可能放在了主文件里，比如 main.py，按照第4的步骤，继续执行。
6. 如果以上两步都失败了，那就只能上终极绝招了。在代码编辑器（如VSCode）里，直接搜索文章的缩写，比如 ViT，选择搜索范围为 .py 文件，这样，定义或者调用该模型的所有地方会被全部列出来。
