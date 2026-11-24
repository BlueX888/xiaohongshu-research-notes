# 模型参数量，FLOPs和推理时间

- 发布时间：2026-03-23 15:20
- 类型：图文（1 张图片）
- 点赞 765 · 收藏 1080 · 评论 120 · 分享 154
- 链接：https://www.xiaohongshu.com/explore/69c0e9d900000000210126a9
- 话题：深度学习 / 计算机 / 科研 / 科研日常 / 计算机视觉 / 博士生 / 数据分析

---

为了实验的完整性，尤其是AI审稿的大环境下，即使不是做轻量化的文章也会要求做这些实验。分享一些代码。

1. 参数量

total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Total params: {total_params:,}")
print(f"Trainable params: {trainable_params:,}")

2. FLOPs(推荐facebookresearch/fvcore)，pip install fvcore

import torch
from fvcore.nn import FlopCountAnalysis, parameter_count_table
model.eval()
dummy = torch.randn(1, 3, 224, 224)
flops = FlopCountAnalysis(model, dummy)
print("Total FLOPs:", flops.total())
print(parameter_count_table(model))

3. Inference Time

import torch
import torch.utils.benchmark as benchmark
model.eval().cuda()
x = torch.randn(1, 3, 224, 224, device='cuda')
t = benchmark.Timer(
stmt='model(x)',
globals={'model': model, 'x': x},
)
result = t.blocked_autorange(min_run_time=1.0)
print(result)
