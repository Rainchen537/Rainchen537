# 个人主页维护

本仓库是 `Rainchen537/Rainchen537`，默认分支为 `main`。只维护 GitHub 个人主页，不修改其他项目源码。

## 文件职责

- `README.md`：唯一公开主页入口，由 `tools/build_readme.py` 生成；所有公开文案、替代文本、链接标签均使用英文。不要只修改生成后的 README。
- `tools/build_readme.py`：当前像素版主页的唯一布局、字体、配色、文案及资源生成入口，只依赖 Python 标准库。
- `assets/pixel/*.svg`：生成的桌面／手机卡片、轮播封面、静态封面、技术栈和页脚。修改生成器后重新生成并提交，资源必须自包含。
- `assets/pixel/source/portrait-scene.png`：从用户提供的完整 HTML 预览中恢复的原始静态场景，生成器通过 SVG 视口与裁切路径复用其中的像素头像。
- `assets/pixel/source/y-clip.svg`、`y-dock.svg`、`y-keys.svg`、`landirect.svg`：从用户预览恢复的像素插画源，供卡片和轮播复用。
- `assets/bnbu.png`：BNBU.ME 正式 macOS 应用图标；顶部轮播和项目卡片统一引用此品牌资源，保持比例，不重新绘制变形符号。
- `tools/render_profile.py`、`assets/atmosphere-card.template.svg`、`assets/profile-hero.svg`、`assets/project-*.svg`：旧雪山版生成器、模板与产物，保留作历史素材；不再控制当前主页。
- `assets/atmosphere.jpg`：旧版背景插画，作品 [A long walk](https://www.pixiv.net/artworks/139667080)，作者 [mmAir](https://www.pixiv.net/users/39363802)；若重新展示，README 必须同步恢复署名。
- `assets/polaris.png`、`assets/y-clip.png`、`assets/y-dock.png`、`assets/y-keys.png`：历史品牌素材；Polaris 当前不在主页展示。
- `log.md`：按日期倒序记录已经完成的维护和验证；本机预览、线上检查分别注明，待验证事项不得写成完成。
- `AGENTS.md`：维护本文档分工、当前生成入口与后续修改规则；布局或文件职责变化时同步更新。

## 设计与内容约束

- 采用用户提供的深色像素风格，保留像素块散开／聚合的动态风格，不可改成整张图淡入淡出；轮播仅包含头像和五个项目，共六个场景，ENTJ 只作为身份标签显示，不设独立场景；配色以深蓝、淡紫、青色为基础。
- 主页全英文；项目介绍用简短、准确的功能描述，避免口号、冗长的一句话推销和重复导语。
- 下方标题与正文保持克制：桌面项目像素标题 21px、正文 18px；手机使用专用布局，不直接缩放桌面长卡片。
- 使用 `picture` 的 `max-width: 600px` 选择手机资源，`prefers-reduced-motion` 选择静态封面；动画 SVG 自身也尊重减少动态效果偏好。
- 不添加心电图、虚构在线状态、硬编码粉丝／Stars／语言占比和容易过时的年龄或构建日期。
- 项目描述先核对公开产品入口或公开仓库；不要复制私有源码或内部运维数据。
- BNBU.ME 为首张重点卡片，保留非官方客户端及桌面预览状态；LanDirect 保留实验性及多人联机未验证说明，兼容性详情链接至公开仓库。
- 所有项目链接指向实际官网或公开仓库；所有图片有可读的英文替代文本。重新加入 Polaris 时先确认用户意图。
- 不增加 GitHub Actions；本机生成和验证即可。原始大体积 HTML 预览及临时截图放在仓库外或 `.local/`。

## 生成与验证

在仓库根目录运行 `python3 tools/build_readme.py`。旧 `tools/render_profile.py` 只用于历史雪山版资源。

修改后检查 SVG XML、README 资源引用、英文文案、生成结果可重复性和 `git diff --check`。在浏览器检查桌面与手机宽度，确认卡片文字完整、链接对应正确、手机资源实际加载且没有横向溢出；检查顶部轮播与减少动态效果静态回退。推送后复核 GitHub 渲染的 README，分别记录本机预览与线上验证。
