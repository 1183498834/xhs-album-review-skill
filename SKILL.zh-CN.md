# 小红书专辑乐评发布 Skill（中文版）

> 本文件是 
>
> `SKILL.md`
>
>  的中文对照版，面向中文读者。Agent 加载时读英文 
>
> `SKILL.md`
>
>  即可。

## 用途

把一张专辑的乐评整理成 3 图笔记，自动填好标题、正文、配图，最后**存进小红书创作者中心草稿箱**。最终红色的「发布」按钮永远由用户自己点。

## 用户需要提供什么



* 艺人名 + 专辑名（例：`Karmanjakah - Diamond Morning`）

* 可选：用户自己的乐评观点。提供了就保留核心意思只润色措辞；没提供就由 AI 写第一人称听感。

## 流程

### 1. 收集专辑和乐队资料

**不要用网易云音乐网页搜索**找独立 / 欧美 / 日系金属 —— 曲库覆盖差，而且每次刷新都弹登录墙。用以下来源：



1. 在 Apple Music 找到专辑页，从 URL 里拿到数字 `id`。

2. 用 iTunes Lookup API 拉完整元数据和曲目（无需登录）：



```
https://itunes.apple.com/lookup?id=<album_id>&country=us&entity=song
```

按 `trackNumber` 排序，保留 `trackName` 和 `trackTimeMillis`。注意豪华版 / 黑胶版可能有数字版没有的 bonus track—— 信 API，不要信搜索结果 snippet。



1. **专辑封面**：API 返回的 `artworkUrl100` 指向 mzstatic CDN，把后缀 `/100x100bb.jpg` 改成 `/1200x1200bb.jpg` 就是高清封面，直接下载。

2. **乐队信息 / Genre / 相似乐队**：用 general\_search 查 Last.fm、Metal Storm、Prog Propaganda、乐队官网。收集：城市国家、成团年份、当前阵容（吉他 / 贝斯 / 鼓 / 主唱）、乐队自我描述、genre 标签（如 Progressive Metal / Djent / Melodic Thall）、3–5 个相似乐队。

3. **乐队合影**：用 image\_search 找 `<band> members` 的宣传照，优先和封面视觉风格一致的。

### 2. 制作 3 张图



| 序号 | 图          | 来源                              |
| -- | ---------- | ------------------------------- |
| 1  | 官方专辑封面     | Apple Music CDN，1200×1200       |
| 2  | 乐队合影 / 宣传照 | image\_search 下载                |
| 3  | 自制曲目卡片     | 运行 `scripts/build_tracklist.py` |



```
python scripts/build_tracklist.py --cover <cover.jpg> --tracks tracks.json --out tracklist.jpg
```

脚本输出 1080×1440（3:4）竖图：深蓝底、封面居中、≥6 首曲目时自动分两列、每首带时长。

### 3. 写乐评（固定结构）



```
🎸 关于乐队
<城市国家、成团年份、成员、组队故事、乐队自我描述>

🎛️ Genre
<genre 标签，例如 Progressive Metal / Djent / Melodic Thall。如果乐评圈给这团起了绰号（如 "happy thall"），写进去。>

🎧 相似乐队
<3–5 个>

💿 专辑信息
<专辑名、发行日期、独立/厂牌发行、在作品序列里的位置、曲目数>

✍️ 我的乐评
<用户原话润色，不要改变核心意思；用户没给就写 2–3 段第一人称听感，别用"锁进年度备选""直接点收藏""个人评分 X/10"这种 AI 乐评套话。>

（**不要**在正文里直接写 `#话题` 字符串——话题标签要在第 4 步通过编辑器话题选择器插入，见下文。）
```

话题清单（5–8 个）单独列出来，不要拼进正文 execCommand 文本里。

### 4. 上传到小红书草稿箱

用 `browser-use-automation` skill（`computer_use_tool`，`plane="bu"`）。发布页是 React + tiptap，直接 `type()` 会被清空。



1. 切到小红书 tab，或打开 `https://creator.xiaohongshu.com/publish/publish`。

2. 点 **「上传图文」** tab（不是默认的「上传视频」）。

3. **不要点红色「上传图片」按钮上传**—— 它是 div 不是 file input。直接对隐藏的 `<input type=file>` 用 `bu.upload_file()`：



```
bu.upload_file("input[type=file]", r"E:\path\to\img1.jpg")
bu.upload_file("input[type=file]", r"E:\path\to\img2.jpg")
bu.upload_file("input[type=file]", r"E:\path\to\img3.jpg")
```

第一次上传后页面切到编辑态，旧 input 可能卸载，每次都重新查 `input[type=file]`。



1. **标题**：标题 input 是 React 受控的，直接 `bu.type()` 失焦会被清掉。用原生 setter + 派发事件：



```
const inp = document.querySelector('input[placeholder*=标题]');
const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
setter.call(inp, '标题');
inp.dispatchEvent(new Event('input', {bubbles:true}));
inp.dispatchEvent(new Event('change', {bubbles:true}));
```



1. **正文**：编辑器是 tiptap `ProseMirror` div，直接改 innerText 不生效。focus 后用 execCommand。**正文里不要带&#x20;**`#tag`**&#x20;字符串**：



```
const ed = document.querySelector('.tiptap.ProseMirror');
ed.focus(); ed.innerHTML = '';
document.execCommand('insertText', false, '正文（不含话题）');
```



1. **话题标签必须通过话题选择器插入，不要直接粘贴&#x20;**`#xxx`**&#x20;文本。**

   把 `#金属 #djent` 这种字符串直接粘进正文只是黑色纯文本，**不会**渲染成可点击的蓝色话题胶囊，点了也跳不到话题页。小红书只在通过编辑器话题流程创建时才生成真正的 tag。每个 tag 的插入步骤：

* 光标移到正文末尾（或换行后）。

* 输入 `#`，约 400ms 后弹出话题联想下拉。

* 输入话题关键词，等候选列表稳定后按 `Enter` 选第一个（或直接点想要的那行）。

* 此时插入的是蓝色高亮话题胶囊。打一个空格，重复下一个 tag。

* 备选路径：点编辑器下方工具栏的 **「话题」** 按钮（在 "用户"" 表情 " 旁边），在弹出框里搜关键词选结果。

* **验证**：插完后 tag 必须是一个独立的高亮样式片段，不能是普通正文黑字。如果长得像 `#xxx` 纯文本，就是插错了，不会跳话题页。

1. **替换已上传的图**：hover 缩略图，角落出现 `.close-btn.hoverShow` 关闭 X，点对应索引删掉再重传。

2. **存草稿**：点右下角 **「暂存离开」**（红色「发布」按钮左边那个）。**不要点「发布」**。UI 会弹「保存成功」，草稿列表里能看到新条目。

### 5. 验证

确认草稿列表里有这条新草稿、标题对、时间戳是新的。把 3 张本地图片路径和草稿保存时间报给用户。

## 安全红线



* 不读、不导出 cookie、localStorage、session token、密码。

* 页面要登录时调 `interaction.request_action`（`type="browserControl"`），让用户自己扫码。不要代输账号密码。

* 红色「发布」按钮是用户的。停在草稿箱为止。

* 一次只存一篇草稿，让用户在手机上自己过目后再发。

## 实战踩过的坑



* 「上传图片」按钮是 div，不是 file input——`bu.upload(button_ref, path)` 会报 `Node is not a file input element`。永远直连隐藏的 `<input type=file>`。

* 直接 `bu.type()` 填标题，失焦后内容会被清空。必须用 native setter + dispatchEvent。

* tiptap 编辑器不认程序化的 innerText 赋值，必须走 `document.execCommand('insertText')`。

* 网易云网页搜索每次刷新弹登录墙，且独立 / 欧美金属曲库覆盖差。专辑事实优先 Apple Music + general search。

* Apple Music snippet 里曲目经常截断。信 iTunes Lookup API（`entity=song`），它返回完整曲目包括 bonus track。

* 「暂存离开」就是存草稿，不是 "不保存离开"，一定要显式点。