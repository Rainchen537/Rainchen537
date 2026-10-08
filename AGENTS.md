# 个人主页维护

本仓库是 `Rainchen537/Rainchen537`，默认分支为 `main`。只维护 GitHub 个人主页，不修改其他项目源码。

## 文件职责

- `README.md`：唯一公开主页入口，由 `tools/build_readme.py` 生成；所有公开文案、替代文本、链接标签均使用英文。不要只修改生成后的 README。
- `tools/build_readme.py`：README 与下方 26 个像素 SVG 的布局、字体、配色、文案生成入口，只依赖 Python 标准库；不改写顶部 GIF。
- `assets/pixel/*.svg`：生成的桌面／手机无框项目索引、技术栈、点阵分隔、像素链接和页脚。修改生成器后重新生成并提交，资源必须自包含。
- `assets/pixel/source/confirmed-hero.gif`、`confirmed-hero-mobile.gif`：用户在 `preview (2).html` 中确认的原始动画，必须逐字节保留；剪接工具锁定其 SHA-256。
- `tools/trim_confirmed_animation.py`：剪除原 GIF 的独立 ENTJ 场景，修改指定菜单／计数区域，并调用 `bnbu_wordmark.py` 替换 BNBU.ME 字标。依赖固定版本 Pillow，见 `tools/requirements-animation.txt`；不得改写其余五场的原始画面、改变原帧节奏、重新量化颜色或用 SVG 替代顶部。
- `tools/bnbu_wordmark.py`：只在原 GIF 的 BNBU.ME 72 帧范围内，将被用户否定的应用图标替换为纯像素字标；转场使用原帧前景位置场，只放行明确的品牌画面矩形。
- `assets/pixel/hero.gif`、`hero-mobile.gif`、`hero-poster.png`、`hero-mobile-poster.png`：原 GIF 精确剪接后的发布资源与首帧静态回退，需提交。GIF 是主页必要素材，不属于忽略的临时大体积构建产物。
- `assets/pixel/source/portrait-scene.png`：早期预览恢复的静态场景，保留作历史素材，当前顶部动画不再引用。
- `assets/pixel/source/y-clip.svg`、`y-dock.svg`、`y-keys.svg`、`landirect.svg`：从用户预览恢复的像素插画源，供卡片和轮播复用。
- `assets/bnbu.png`：BNBU.ME 历史应用图标，保留作素材；当前顶部与项目索引均使用纯像素文字 `BNBU.ME`，不展示应用图标。
- `tools/render_profile.py`、`assets/atmosphere-card.template.svg`、`assets/profile-hero.svg`、`assets/project-*.svg`：旧雪山版生成器、模板与产物，保留作历史素材；不再控制当前主页。
- `assets/atmosphere.jpg`：旧版背景插画，作品 [A long walk](https://www.pixiv.net/artworks/139667080)，作者 [mmAir](https://www.pixiv.net/users/39363802)；若重新展示，README 必须同步恢复署名。
- `assets/polaris.png`、`assets/y-clip.png`、`assets/y-dock.png`、`assets/y-keys.png`：历史品牌素材；Polaris 当前不在主页展示。
- `log.md`：按日期倒序记录已经完成的维护和验证；本机预览、线上检查分别注明，待验证事项不得写成完成。
- `AGENTS.md`：维护本文档分工、当前生成入口与后续修改规则；布局或文件职责变化时同步更新。

## 设计与内容约束

- 顶部沿用用户确认版原始 GIF 的细密粒子、扫描线转场和原节奏；BNBU.ME 场景按用户明确要求替换为像素字标，其余五场保持原帧；禁止用自行实现的 SVG 方块动效、整图淡入淡出或其他近似动画替代。只保留头像和五个项目，共六场；第一项为 `PERSONA / ENTJ`，ENTJ 与头像同屏，无独立场景。
- 主页全英文；项目介绍用简短、准确的功能描述，避免口号、冗长的一句话推销和重复导语。
- 下方采用早期个人主页的像素排版：所有可见文字使用内置位图字形、小型原像素图标与点阵细分隔；不使用卡片面板、现代系统字体、额外导语或完整句子的项目说明。项目用途用简短标签，保留必要状态与技术信息；手机使用独立布局。
- 使用 `picture` 的 `max-width: 600px` 选择手机资源，`prefers-reduced-motion` 选择PNG 静态封面。
- 不添加心电图、虚构在线状态、硬编码粉丝／Stars／语言占比和容易过时的年龄或构建日期。
- 项目描述先核对公开产品入口或公开仓库；不要复制私有源码或内部运维数据。
- BNBU.ME 为首张重点卡片，保留非官方客户端及桌面预览状态；LanDirect 保留实验性及多人联机未验证说明，兼容性详情链接至公开仓库。
- 所有项目链接指向实际官网或公开仓库；所有图片有可读的英文替代文本。重新加入 Polaris 时先确认用户意图。
- 不增加 GitHub Actions；本机生成和验证即可。原始大体积 HTML 预览及临时截图放在仓库外或 `.local/`。

## 生成与验证

在仓库根目录运行 `python3 tools/build_readme.py`，只重新生成 README 与下方 SVG。旧 `tools/render_profile.py` 只用于历史雪山版资源。

只有确需重新剪接顶部动画时，使用本机隔离环境：

```sh
python3 -m venv .local/gif-tools
.local/gif-tools/bin/pip install -r tools/requirements-animation.txt
.local/gif-tools/bin/python tools/trim_confirmed_animation.py
python3 tools/build_readme.py
```

剪接保留原始帧 `0–57` 和 `130–503`（零起始），删除独立 ENTJ 所在的 72 帧，输出 432 帧，每帧 50ms、总长 21.6 秒。只修改脚本明确列出的菜单／计数矩形，以及原始 `130–201` 帧内的 BNBU.ME 字标区域；脚本在写入前及 GIF 重新解码后逐帧验证：放行矩形之外像素必须与对应原帧完全相同。其他场景不增加品牌区域例外。比对报告写入 `.local/verification/confirmed-animation.json`。原始 GIF 摘要和输出确定性均须验证。

修改后检查 SVG XML、README 资源引用、英文文案、生成结果可重复性和 `git diff --check`。在浏览器检查桌面与手机宽度，确认卡片文字完整、链接对应正确、手机资源实际加载且没有横向溢出；检查顶部轮播与减少动态效果静态回退。推送后复核 GitHub 渲染的 README，分别记录本机预览与线上验证。
