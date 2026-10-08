# OctoSense Inbox Assistant

[English](README.md) | 简体中文

这是 **macOS 开发预览版**，用于读取 Gmail，在 Email／Reply／Chat 中编辑同一份草稿，并在发送前审阅宿主保存的完整内容。
发布者为 [ymote](https://github.com/ymote)，新应用 ID 为 `io.github.ymote.inboxassistant`，
可编辑源码版本为 **0.2.0**。这是独立示例，不是 Google 官方产品。

新版本通过 GitHub 发布证明确认发布者身份，无需开发者签名私钥或仓库签名机密。
它与旧应用 `org.octosense.samples.inbox` 分别安装，账户授权和本地数据不会自动迁移。
旧 `v0.1.0`／`v0.1.1` 标签、签名和验收记录不变；`publisher.json` 仅描述历史身份。

## 安装与连接

新版本需要 **应用契约 1.8.0／`publisher-github-v1`** 及兼容的 OctoSense
连接服务主机。旧 desktop beta.2 无法安装 GitHub 证明发行包。创建标签不等于
App Hub 收录；先查看提交 issue 的目录／发行状态。已收录且主机兼容时，使用
**App Hub → Search → Inbox Assistant → Get → Install → Open**，审阅请求的权限。

Google 登录由宿主浏览器／提供方流程完成，应用不收集密码。宿主维护者配置
OAuth 客户端和对应 API，普通用户无需注册开发者客户端，也无需另建 OctoSense
账户。参见[宿主 OAuth 指南](https://github.com/OctoSense-org/OctoSense/blob/main/crates/oauth-service/README.md)。
应用仅获得绑定应用与账户的不透明句柄，不接收凭据。

**发布流程测试不验证真实 Google 登录、读取／写入或物理确认。** Android Google
授权仍不可用，本版本不宣称支持 Android、Linux 或 Windows。独立 `card-host`
只能验证本地界面和明确的服务不可用状态。

## 使用

1. 无需登录即可使用明确标注的虚构收件箱。选中邮件后点击 **Compose reply**；
   虚构草稿不能发送邮件。
2. **Reply** 编辑正文，**Details** 展开收件人和主题，**Save** 保存本地修改。
   Email／Reply／Chat 共用同一份草稿。
3. 已配置宿主上 **Connect Google** 启用手工读取／编辑。使用 AI sort、Chat 或
   后台分流前请阅读[隐私说明](PRIVACY.zh-CN.md)。
4. 应用代理同意与 Google 登录独立。启用后建立只关注新邮件的基线，在宿主允许
   执行时通常每五分钟检查；不会为全部旧邮件补发通知。账户代理判断哪些邮件值得
   生成 Glance 卡片，营销邮件通常静默。**静默邮件也可能发送给模型以判断重要性。**
5. **Review & Send** 展示宿主保存的账户、收件人、主题和正文。只有原生宿主批准
   控件上的物理操作能授权发送，模型和自动输入不能批准。Gmail 接受不等于送达。

代理只有账户内私有的读取、草稿和通知工具，没有发送别名。本版本不实现跨应用
日历预订、附件、Reply All、富文本回复、超过前 30 条的分页或系统记忆提升。
AI sort 是独立的前台模型操作；关闭后台代理不等于禁用该按钮。

## 发布和本地检查

可编辑 `bundle/` 不含发行证明。[GitHub 工作流](.github/workflows/publish-app.yml)
固定已审阅的 Hub 工具版本。完成源码测试和审阅后推送全新 `v<manifest.version>`
标签，GitHub 准备、证明、验证并上传 `app.bundle.pack.json`。不要把已封存包覆盖
回开发源码，不要移动已有标签。

```sh
python3 -m unittest discover -s tests -v
python3 build_bundle.py
"$HUB" stamp bundle
"$HUB" check bundle --allow-unsigned
mkdir -p build
"$HUB" scan bundle --packet build/review.json
```

通过 [App Hub issue](https://github.com/OctoSense-org/OctoSense-App-Hub/issues) 请求
发布，提供 ID、源码、权限、截图和审核答案。issue 可先于标签创建；完成后补充
成功工作流、确切提交和包哈希。管理员审阅和目录发布与创建发行版是不同步骤。
下载包使用 `hub publisher-unpack`／`hub publisher-verify` 验证，不重新 stamp
或移除证明。

## 证据边界

本版本保留当前功能代码，使用新身份及发布流程。`review/`、已有 `evidence/`
和旧标签中的记录保留原始源码／二进制身份，不能当作 0.2.0 的新验收。发行前只用
新实际原生截图替换列表图，并逐张审视。

Email／Reply／Chat 布局来自未发布的 `0.1.2-ux.1`，没有重做控制器。历史 Mac
测试使用模拟 Gmail 和 DeepSeek，仍保留两次帧提交错误。私有 Android 候选曾完成
30 轮流程，但这不代表 Android Google 支持或本包验收。参见[布局历史](review/UX-CANDIDATE.md)
和[固定版本 README](https://github.com/ymote/octosense-inbox-assistant/blob/5025af76a4928b526111ea35b1b1300588ca6bd8/README.md)。

连接账户或启用 AI 前请阅读[隐私说明](PRIVACY.zh-CN.md)。
[公开支持](https://github.com/ymote/octosense-inbox-assistant/issues) 中不要提交私人邮件／事件、凭据
或原始日志。采用 [Apache-2.0](LICENSE)。

当前源码检查：[原生离线记录](review/releases/0.2.0/NATIVE.json)、[准入输出](review/releases/0.2.0/GATE.txt)、[八项审核答案](review/ANSWERS.md)。
