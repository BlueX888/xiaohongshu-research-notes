# PaperBanana使用体验

- 发布时间：2026-02-25 20:39
- 类型：图文（4 张图片）
- 点赞 459 · 收藏 584 · 评论 42 · 分享 85
- 链接：https://www.xiaohongshu.com/explore/699eed6d0000000015032b20
- 话题：科研绘图 / ai / ai绘图 / vibe / 计算机 / paper

---

1. 安装教程，就是对照着Github一步步去操作就行，记得要有uv和streamlit工具，没有的话安装即可。但是很重要的一点是，这个项目适合在Linux部署，如果在Windows或者macOS部署，会出现time.tzset() 操作系统兼容性报错。在启动网页端时，utils/config.py 里直接调用了 Unix 系统特有的 API time.tzset()，而由于某些 Python 发行版的编译差异缺失了这个属性，直接引发了 AttributeError 崩溃。解决方案就是在代码中补充了一层检查逻辑 if hasattr(time, "tzset"):，如果环境不支持则跳过调用。
2. 在configs/model_config.yaml文件中要至少填写三个值，model_name: "gemini-3-pro-preview"  image_model_name: "gemini-3-pro-image-preview"   google_api_key: " " (引号内填写自己的API key)。
3. 别忘记下载数据集。在PaperBanana目录下创建data文件夹，然后把下载的PaperBananaBench放到data目录下。
4. 使用体验。第一张图是模型生成的结果图。第二张图到第四张图是模型迭代的第一轮到第三轮的图。总体来说，我也看不出来到底哪里进行了特别好的优化，而且生成的图里还是有比较明显的AI作图的痕迹，比如图标。简单看了下项目的开源代码，还是调用现有的模型进行生图，并没有专门拿顶会的图进行训练。只是配备了更加完备的prompt以及参考图样例。当然，多个智能体的协作可能还是有作用的，只是这也让生成单张图片的价格虚高，有的时候API还存在调用失败的情况。虽然还存在一些问题，但确实是在vibe research上做的切实的努力，很感谢这些大佬开源了这样优秀的成果。        research     banana
