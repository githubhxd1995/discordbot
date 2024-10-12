### 关于项目

本项目是使用discord的机器人配合青龙的OpenAPI，实现在频道聊天中使用机器人更新环境变量。

### 推荐环境

1. Linux系统（mac应该也可以）
2. 能够访问discord的网络

### 需要的参数

1. 青龙项目地址,eg:xxx:5700
2. Discord机器人的token，可以参考这个高天老师视频中的前三分钟内容获取token，并且把机器人设置好

### 安装步骤

1. clone本项目并进入项目所在目录
2. 安装python虚拟环境&激活虚拟环境&安装依赖

```bash
python -m venv env
source env/bin/activate 
pip install -r requirements.txt
```

3. 配置环境变量

```bash
export QINGLONG_URL=''
export DISCORD_BOT_TOKEN='xxx'
```

> 上面两个环境变量是在参数步骤中获取的

4. 运行项目

```bash
nohup python discordbot.py > log.log 2&>1 & 
```

5. 在机器人所在的频道激活一下命令 !synccommands

到此就可以愉快的在discord中更新和修改青龙的环境变量了
![使用效果图](https://github.com/githubhxd1995/discordbot/blob/main/image/usescreen.png)

## 声明



- 本软件使用 [GNU Affero General Public License v3.0 only](https://spdx.org/licenses/AGPL-3.0-only.html) 开源。
- 本软件开源、免费，仅供学习交流使用。若您遇到商家使用本软件进行代挂并收费，产生的任何问题及后果与本软件无关。
