# 小红书专辑乐评发布 Skill（中文版）

> 本文件是 `SKILL.md` 的中文对照版，面向中文读者。Agent 加载时读英文 `SKILL.md` 即可。

## 用途

把一张专辑的乐评整理成 3 图笔记，自动填好标题、正文、配图，最后存进小红书创作者中心。**默认存草稿箱**；只有用户本次明确说出"直接发布不需要经过人工同意"（或同等明确的直接发布指令），才点红色「发布」按钮。拿不准就存草稿然后问用户。

## 用户需要提供什么

* 艺人名 + 专辑名（例：`Karmanjakah - Diamond Morning`）
* 可选：用户自己的乐评观点。提供了就以此为种子**扩展**成完整乐评（见 `modules/03-write-review.md`），保留核心意思和立场，不能反转结论；没提供就由 AI 写第一人称听感。

## 流程

每个步骤一个独立模块文件，做到哪步读哪个。

每次跑之前先建一个 per-album 工作文件夹：`<项目根目录>/<artist>-<album-slug>/`。所有产物（封面、乐队照、曲目卡片、review.md、tracks.json）都放这个文件夹里。万一 Step 4 浏览器上传中途崩了，本地文件已经齐了。

| 步骤 | 做什么 | 读哪个文件 |
| --- | --- | --- |
| 1 | 在 Apple Music 找到专辑，用 iTunes Lookup API 拉完整曲目，下载封面，收集乐队资料/Genre/相似乐队，找乐队合影。 | `modules/01-collect-album-info.md` |
| 2 | 拼出 3 张图：官方封面、乐队宣传照、自制曲目卡片。 | `modules/02-build-images.md` |
| 3 | 按固定模板写乐评。用户给了原稿就扩展，写完过一遍去 AI 味规则。**动浏览器之前先把 review.md 存到工作文件夹。** | `modules/03-write-review.md` + `modules/deai-rules.md` |
| 4 | 打开小红书创作者中心，从工作文件夹传 3 张图，填标题正文，通过话题选择器插入话题胶囊。默认存草稿；只有用户明确说"直接发布不需要经过人工同意"才点发布。 | `modules/04-upload-draft.md` |
| 5 | 确认草稿存好了，把工作文件夹路径、图片路径和保存时间报给用户。 | `modules/05-verify.md` |

## 安全红线和踩过的坑

动浏览器之前先读 `modules/safety-and-pitfalls.md`。里面有红线（不碰 cookie、不代输账号密码、不批量发）和 DOM 层已经踩过的坑。

**默认结束状态是存进草稿箱，不是直接发出去。** 红色「发布」按钮只有在用户本次指令里明确说出"直接发布不需要经过人工同意"（或同等明确的直接发布指令）时才能点。其他任何说法，包括"发了吧""你看着办""看着不错"，都只能存草稿。拿不准就存草稿然后问用户。

## 目录结构

```
xhs-album-review-skill/
├── SKILL.md                          # 入口（路由）
├── SKILL.zh-CN.md                    # 本文件
├── README.md
├── modules/
│   ├── 01-collect-album-info.md      # 步骤 1
│   ├── 02-build-images.md            # 步骤 2
│   ├── 03-write-review.md             # 步骤 3
│   ├── deai-rules.md                 # 去 AI 味规则（步骤 3 引用）
│   ├── 04-upload-draft.md            # 步骤 4
│   ├── 05-verify.md                   # 步骤 5
│   └── safety-and-pitfalls.md        # 安全红线 + 踩坑
└── scripts/
    ├── build_tracklist.py
    └── tracks.example.json
```
