# Deep Learning环境配置常见问题

- 发布时间：2025-12-16 11:15
- 类型：图文（1 张图片）
- 点赞 175 · 收藏 196 · 评论 15 · 分享 13
- 链接：https://www.xiaohongshu.com/explore/6940ceb8000000000d036ce0
- 话题：深度学习 / 科研 / 计算机 / 代码 / 研究生 / 博士生

---

1. CUDA/cuDNN版本不匹配。应该严格对照PyTorch提供的表格，确认框架版本、CUDA Toolkit版本、cuDNN版本三者完全匹配。优先使用conda install pytorch torchvision torchaudio cudatoolkit=X.X来安装，让Conda自动处理依赖。
2. 驱动与CUDA不兼容。先查后装，使用nvidia-smi查看驱动支持的CUDA版本，然后安装低于或等于该版本的CUDA Toolkit。驱动版本通常越新越好，但要确保它能支持你需要的CUDA版本。
3. 每个项目需要的环境不一样。为每个项目创建一个独立的Conda环境，并指定所需的Python版本，例如conda create -n ResNet python=3.7。
4. Conda创建环境慢。配置中科大等国内镜像源，可以显著提高下载速度。
5. 有些包，数据集，依赖需要梯子，而很多服务器是没有配置的，所以我们可以在自己的笔记本上（开了梯子）下载完，然后再上传到服务器。
6. 详细阅读项目的Readme，尽量做到环境配置一样，否则如果复现失败了，你会怀疑是环境配置这一步就出错了，很难找到具体的原因。
7. 有些库只有在Linux系统上才有，在Windows系统上没有，所以要明确自己的项目是否有类似的限制，否则在自己的电脑上鼓捣半天也是白搭。
