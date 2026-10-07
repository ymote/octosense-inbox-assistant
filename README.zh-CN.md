# Inbox Assistant

[English](README.md) | 简体中文

这是 OctoSense 的 macOS **开发预览应用**。通过主机读取 Gmail，Email／Reply／Chat
共用一份已保存草稿；发送前由主机原生界面审核完整内容。可选应用代理针对重要
新邮件生成 Glance 卡片。应用 ID 为 `org.octosense.samples.inbox`，已发布版本 `0.1.1`（发布者已签名预览）。

此分支是**尚未签名、尚未发布的 `0.1.2-ux.1` 布局候选版**。邮件标题、发件人与正文
一起滚动；Reply 将可用空间留给正文编辑器，下方集中放置 Details、Save 与 Review。
Details 可展开编辑收件人和主题。应用与 Glance 共用同一控制器。手机验收尚未完成，
列表截图仍是旧版界面。参见[候选版范围与验证](review/UX-CANDIDATE.md)。

## 所需主机

安装 [OctoSense desktop-v0.1.0-beta.2 macOS Apple Silicon 预览版](https://github.com/OctoSense-org/OctoSense/releases/tag/desktop-v0.1.0-beta.2)。
签名版本 `0.1.1` 已进入官方 App Hub 目录
（[目录序号 10，App Hub #133](https://github.com/OctoSense-org/OctoSense-App-Hub/pull/133)）。在 OctoSense 中打开 **App Hub → Search**，
搜索 **Inbox Assistant**，审阅权限后依次点击 **Get → Install → Open**。
`v0.1.1` 及之前的 `v0.1.0` 标签保持不变。

旧版 Shell 与独立 `card-host` 不提供这些 OAuth／Gmail／代理服务。本仓库只包含
脚本应用包，不含独立桌面程序。

主机需配置 Google 桌面 OAuth 客户端、Gmail API 和适用的同意／测试用户设置，
参见[固定版本的配置说明](https://github.com/OctoSense-org/OctoSense/blob/desktop-v0.1.0-beta.2/crates/oauth-service/README.md)。
无需另建 OctoSense 账户；Connect Google 使用主机／浏览器授权，应用只接收绑定
账户的句柄，不接收密码或令牌。

## 使用

初始收件箱和两张商店截图均使用明确标注的虚构数据。无需登录即可编辑，不能
发送邮件。兼容主机上可以连接 Google，手工读取和编辑不依赖模型。AI sort、
Chat 和后台分流会将相关数据发送至主机配置的模型，详见[隐私说明](PRIVACY.zh-CN.md)。

Google 登录与应用代理同意分别控制。允许代理后，保持收件箱列表打开，等待
**New-mail baseline ready**；此本地状态每三秒刷新。主机通常在允许执行时每五
分钟检查新邮件，不为全部旧邮件补发通知。基线就绪不等于代理目前仍已启用。

打开相关 Glance 卡片，直接编辑 Reply，或通过 Chat 修改同一份草稿。请核对
实际保存内容，再打开 **Review & Send**；只有主机原生控件的物理批准可以授权
提交，模型和自动点击不能批准。Gmail 接受提交不等于收件人已收到。

默认关注医疗、物流、日程、学校／工作和家庭事项，普通营销通常静默。**静默邮件
也需要先由代理／模型读取，才能判断相关性。** Pin 是手工操作；AI sort 是前台
辅助功能，与自动新邮件事件不同。

## 验证边界

历史[集成证据](https://github.com/OctoSense-org/OctoScript-App-Design-Flow/blob/5b0fde7ed0e9e4131751d16f55ba3d8a3180dd95/examples/connected-apps/inbox/evidence/integrated/README.md)
及 [Mac 持续测试](https://github.com/OctoSense-org/OctoScript-App-Design-Flow/blob/5b0fde7ed0e9e4131751d16f55ba3d8a3180dd95/examples/connected-apps/inbox/evidence/soak/README.md)
使用真实 DeepSeek 和模拟 Gmail，完成 610 秒内 33 轮功能流程、共享草稿、审核
取消、阻止自动批准及冷启动恢复。**仍存在两次尚未解决的帧提交确认错误**，不能
把功能完成称为无渲染／性能问题的验收。

真实 Google OAuth、Gmail 读取／发送／送达及物理发送批准尚未验证。Android
的 Google 授权适配器尚未实现，不声明 Android、Windows 或 Linux 已验证。跨
应用日历预约、附件、全部回复、富文本、超过首批 30 行的分页和共享系统记忆
汇总均不在本应用已实现范围内。

已发布的 0.1.1 调整了通知 schema、代理／技能指导与发布元数据；应用／模板界面和原始
截图在该版本保持不变。应用摘要因此发生变化，历史测试并非 0.1.1 摘要的执行证据。[来源说明](ATTRIBUTION.md)与
[源码核对](review/SOURCE-AUDIT.json)记录该边界，不把旧测试改称为新签名发布验证。

## 验证发布包

0.1.1 的历史签名检查见 [review/GATE.txt](review/GATE.txt)、[发布记录](review/RELEASE.json)及
[八项扫描问题](review/QUESTIONS.json)；官方目录准入仍是独立步骤。

先运行 `git worktree add --detach ../inbox-release-0.1.1 v0.1.1` 创建独立的
不可变发布检出，再从该目录 `publisher.json` 的 `public_key` 读取公钥至
`YMOTE_PUBLIC_KEY`，执行
`"$HUB" check ../inbox-release-0.1.1/bundle --publisher-key "ymote=$YMOTE_PUBLIC_KEY"`
验证发布包。不要为了通过检查而给发布包重新 `stamp`；无签名检查不能替代签名验证。

## 开发

此分支已是明确的无签名开发副本。从签名标签开始开发时，只从开发副本的
manifest 删除 `integrity.signature`。
修改 `src/workspace.splash` 后执行 `python3 build_bundle.py`，使用匹配的 Hub
运行 `stamp`、`check --allow-unsigned` 和 `scan --packet build/review.json`。只
提交 `bundle/`；密钥、账户／模型配置、真实邮件截图及扫描包不应进入 Git。
测试脚本需显式指定自有隐藏实例和隔离路径，不会批准发送。完整命令见英文说明。

发布者：[ymote](https://github.com/ymote)；[反馈](https://github.com/ymote/octosense-inbox-assistant/issues)；
[隐私](PRIVACY.zh-CN.md)；[审核问答](review/ANSWERS.md)；[Apache-2.0](LICENSE)。
请勿在公开问题中发送私人邮件、凭据或未清理的日志。

## 已发布的 0.1.1 契约修正

通知工具现在必须提供已准入的 `glance-workspace.splash` 模板、`initial.message`、
标题、摘要及是否通知的决定，不再接受 `script`、`source` 或 `data` 替代参数。
代理负责重要性与内容判断，已签名模板提供原有 Email／Reply／Chat 工作区。
在 0.1.1 发布中，应用／模板界面及原始截图与 0.1.0 的字节一致；这次声明修正不构成
新的真实 Gmail、发送或模型性能验证。0.1.1 已签名并进入官方目录；本分支候选版尚未发布。
运行 `python3 -m unittest discover -s tests -v` 检查发布契约，再运行匹配 Hub 的准入检查。

旧 `0.1.0` 签名记录保存在 `review/releases/0.1.0/`，不用于验证 `0.1.1`。签名
0.1.1 记录已在 `review/` 中提供；它们不验证当前无签名候选版。

0.1.1 的包哈希变化包括通知 schema、代理／技能指令；该版本的原始 UI、模板和截图保持不变。`review/SOURCE-AUDIT.json` 是 0.1.0 的历史来源记录，不验证本次新包。

[收录后目录记录](review/CATALOG-0.1.1.json) 验证默认公开目录、签名包与列表资源。
它只增加发布证据，不增加原生、模型或真实服务验收声明。标签中的发布记录仍保留签名时的历史状态。
