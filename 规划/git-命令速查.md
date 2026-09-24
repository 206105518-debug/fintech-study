# git 命令速查（2026.9.24 起用）

> 用途：忘了命令时翻这一页。参考 Git 官方文档或《Pro Git》前两章。
> 你不用背，一天敲三次，一周就熟了。

---

## 一、先理解四个区域

git 管代码，本质上是「把文件在四个地方之间搬运」：

| 位置 | 是什么 | 常用命令 |
| --- | --- | --- |
| 工作区 | 你正在编辑的文件 | 直接改文件 |
| 暂存区 | 挑出来、准备存档的那批改动 | `git add` |
| 本地仓库 | 一次次的存档记录（历史） | `git commit` |
| 远程仓库 | GitHub 上的那份备份 | `git push` |

日常动作就是：**改文件 → 挑一批 → 存档 → 上传**。

---

## 二、建仓库（一辈子只做一次）

```bash
cd ~/Documents/Codex/金融科技学习
git init                       # 初始化，生成 .git 目录
git add .
git commit -m "第一次提交"
```

`.gitignore` 里写这两行，把不该上传的东西排除掉：

```
__pycache__/
.DS_Store
```

---

## 三、每天都要用的三条

```bash
git status                     # 先看现在什么状态（最常用，不确定就敲它）
git add .                      # 把改动挑进暂存区
git commit -m "说清这次改了什么"
```

`commit -m` 后面那句话是写给未来的自己看的。**别写 update、修改、提交这种废话**，
写「完成 CSV 统计脚本，处理缺失值」这种，半年后你还看得懂。

---

## 四、和 GitHub 同步

```bash
git remote add origin 仓库地址   # 第一次关联远程仓库，只做一次
git push -u origin main         # 把本地存档上传（第一次带 -u，以后直接 git push）
git pull                        # 把远程的变动拉下来（换电脑写代码时用）
```

看远程地址：`git remote -v`

---

## 五、看历史与看改动

```bash
git log --oneline               # 一行一条的提交历史
git diff                        # 看工作区里改了什么但还没 add
git diff --staged               # 看已经 add、还没 commit 的内容
git show 某个提交号              # 看某一次提交具体改了什么
```

---

## 六、分支（9.28 会学）

```bash
git branch                      # 看有哪些分支，星号是当前所在
git checkout -b 新分支名          # 建一个分支并切过去
git checkout main               # 切回主分支
git merge 某个分支               # 把这个分支合并进当前分支
```

---

## 七、手滑了怎么办

```bash
git restore 文件名                # 丢弃这个文件还没 add 的改动（改坏了才用）
git restore --staged 文件名       # 从暂存区拿出来，改动本身还留着
git commit --amend -m "新说明"    # 刚提交完发现说明写错了，改掉重提
```

⚠️ 前两条会**真的丢掉东西**，用之前先 `git diff` 看一眼，确认不要了再敲。

---

## 八、常见报错对照

| 报错 / 现象 | 什么意思 | 怎么办 |
| --- | --- | --- |
| `not a git repository` | 你不在仓库目录里 | `cd` 到 金融科技学习 再敲 |
| `nothing to commit` | 没有新改动 | 正常，说明该提交的都提交了 |
| 提示要先 `git pull` | 远程有你本地没有的提交 | 先 `git pull` 再 `git push` |
| `Permission denied (publickey)` | 没配 SSH key，或 key 没加到 GitHub | 换 HTTPS 方式推，或在 GitHub 里添加公钥 |
| 密码框里输密码推不上去 | GitHub 早就不收账号密码了 | 用 Personal Access Token 当密码，或改用 SSH |
| `rejected ... non-fast-forward` | 远程比本地新 | `git pull` 合并后再推 |

---

## 九、三条纪律

1. **一个功能一次提交。** 别攒一周提交一次，出问题时回不去。
2. **提交前先 `git status`。** 看一眼自己要提交什么，别把密码、数据集、几百 MB 的文件传上去。
3. **提交信息写清「做了什么」。** 它是对未来自己的交代。
