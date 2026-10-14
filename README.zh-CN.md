# xhs-album-review-skill

> 一个 Agent Skill，把艺人名 + 专辑名变成一篇可以直接发到 **Rednote（小红书）** 的 3 图专辑乐评笔记，并自动存进创作者中心草稿箱。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Agent%20Skill-lightgrey.svg)]()

[English](README.md) | [中文](README.zh-CN.md)

---

## 它能做什么

给它一个艺人名和专辑名（比如 `Karmanjakah - Diamond Morning`），它会：

1. **在 Apple Music 上找到专辑**，通过公开的 iTunes Lookup API 拉到完整曲目（无需登录、无登录墙）。
2. **下载 1200×1200 高清封面**，从 Apple CDN 直接拿。
3. **收集乐队资料**——城市、阵容、Genre 标签、相似乐队——通过网页搜索。
4. **找一张乐队宣传照**，通过图片搜索。
5. **生成一张自制曲目卡片**（深蓝底、≥6 首自动分两列、带每首时长），用 Pillow 渲染。
6. **写乐评**——如果你给了自己的原稿，它会以原稿为种子扩展成 2–3 段完整乐评，保留你的立场和判断；如果你没给，它从零写一段第一人称听感。写完之后还会过一遍内置的"去 AI 味"检查清单，避免读起来像聊天机器人。
7. **动浏览器之前先把所有东西存到本地**——每个专辑一个文件夹，里面有 `review.md`、封面、乐队照、曲目卡片。就算浏览器崩了，工作成果也不会丢。
8. **填好 Rednote 发布页**——标题、正文、3 张图、可点击的话题胶囊——然后存进草稿箱。红色的**发布**按钮永远留给你自己点。

## 为什么不用网易云音乐？

网易云网页搜索每次刷新都弹登录墙，而且独立/欧美金属曲库覆盖差。Apple Music + iTunes Lookup API 能拿到完整、机器可读的曲目，没有任何墙。

## 目录结构

```
xhs-album-review-skill/
├── SKILL.md                          # 入口：路由、输入要求、步骤表
├── SKILL.zh-CN.md                    # 中文对照
├── README.md                         # 英文说明
├── README.zh-CN.md                   # 本文件
├── modules/
│   ├── 01-collect-album-info.md     # 步骤 1：Apple Music、iTunes API、封面、乐队资料、照片
│   ├── 02-build-images.md            # 步骤 2：3 张图、曲目卡片脚本
│   ├── 03-write-review.md            # 步骤 3：固定模板 + 乐评写作规则
│   ├── deai-rules.md                 # 去 AI 味检查清单（步骤 3 引用）
│   ├── 04-upload-draft.md            # 步骤 4：浏览器自动化、DOM 填写、话题选择器
│   ├── 05-verify.md                 # 步骤 5：确认草稿、向用户汇报
│   └── safety-and-pitfalls.md       # 安全红线 + 踩过的坑
└── scripts/
    ├── build_tracklist.py             # 渲染 1080×1440 曲目卡片
    └── tracks.example.json             # 曲目输入示例
```

每个步骤一个独立模块文件，改哪个功能只动哪个文件，不影响其他部分。

## 每次跑都会在本地建一个文件夹

```
<项目根目录>/<artist>-<album-slug>/
├── review.md          # 最终笔记正文，动浏览器之前就存好
├── cover.jpg          # 1200×1200 官方封面
├── band-photo.jpg    # 乐队宣传照
├── tracklist.jpg      # 自制曲目卡片
└── tracks.json        # iTunes API 拉的完整曲目
```

就算浏览器上传失败，这些文件已经在本地了，可以重跑或者手动粘贴。

## 笔记正文模板

```
🎸 关于乐队       → 城市国家、成团年份、阵容、乐队自我描述
🎛️ Genre          → Genre 标签 + 乐评圈绰号（比如 "happy thall"）
🎧 相似乐队        → 3–5 个
💿 专辑信息        → 发行日期、独立/厂牌发行、在作品序列里的位置
✍️ 我的乐评        → 从用户原稿扩展，或从零写，写完过一遍去 AI 味
#话题              → 5–8 个话题，全部排在同一行，通过话题选择器插入
```

## 快速开始（只跑曲目卡片）

```bash
pip install pillow

python scripts/build_tracklist.py \
    --cover Karmanjakah_Diamond_morning_cover.jpg \
    --tracks scripts/tracks.example.json \
    --out tracklist.jpg \
    --artist Karmanjakah \
    --album "Diamond Morning" \
    --year 2026
```

## 硬规则

- **默认存草稿。** 笔记结束在创作者中心草稿箱。红色**发布**按钮只有在用户本次明确说出"直接发布不需要经过人工同意"时才能点。其他任何说法——"发了吧""你看着办""看着不错"——都只能存草稿。拿不准就存草稿然后问用户。
- 不碰 cookie、localStorage、session token、密码。
- Rednote 要登录时，把浏览器交给用户扫码，不代输账号密码。
- 不批量发，一次一篇。
- **话题不要当纯文本粘贴。** 直接往正文里打 `#tag` 只是黑色文字，不会变成可点击的话题胶囊。每个话题都要在编辑器里输入 `#` 然后从弹出的联想列表里选。所有话题排在同一行，之间用单个空格分隔，绝不一个话题占一行。

## 浏览器后端

Skill 不写死用哪个浏览器，根据用户本次的表述选：

| 用户说 | 后端 |
| --- | --- |
| _（没说，默认）_ | 内置浏览器（`computer_use_tool`，`plane="bu"`） |
| "用我 Chrome / 我 Edge / 我登录好的浏览器" | 用户自己的浏览器，走 `browser-skill`（bsk CLI + 扩展） |
| "用 Edge" / "用 Chrome"（明确指定） | 桌面自动化（`computer_use_tool`，`plane="cu"`），启动对应浏览器 |

DOM 层的坑（React 标题 input、tiptap 编辑器、隐藏 file input、话题选择器）三种后端都一样，只是调用语法不同。整个流程中途不换后端。

## 依赖

- Agent 运行时需要支持 `computer_use_tool`（`plane="bu"` 和 `plane="cu"` 都要）。`browser-skill` bsk CLI 是可选的。
- Python 3.9+，需要 `Pillow` 用来渲染曲目卡片。
- 不需要任何 API key。

## 协议

MIT，随便用，不担保。
