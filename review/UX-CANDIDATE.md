# Unpublished phone layout candidate

English / 简体中文

`0.1.2-ux.1` is an unsigned development candidate based on
[the published 0.1.1 repository state](https://github.com/ymote/octosense-inbox-assistant/commit/ee431d570b5c305f00a9896b6cbe24c995aa1808).
It is not a release or an App Hub submission. The immutable `v0.1.1` tag,
release assets, historical screenshots and signed review records are unchanged.

The observed phone problem was a reply editor and actions crowded below the
keyboard. The candidate puts the full message context in the Email scroll area,
gives the reply body the remaining viewport, and groups Details, Save and
Review & Send below it. Details reveals the resident recipient and subject
editors. It removes duplicate heading/status rows; it does not reconstruct the
draft on tab changes. `src/workspace.splash` generates both the app and Glance
workspace. Agent declarations, tool schemas, skills, provider requests and the
physical-send approval boundary are unchanged.

## Validation boundary

| Check | Result and scope |
| --- | --- |
| Source generation | Contract test regenerates both entries in an isolated directory and compares their exact bytes. |
| Agent/privacy boundary | Contract tests compare the agent, tools and skills with the signed 0.1.1 record; no capabilities or account authority were added. |
| Native layout probe | With Android styling at 390 × 320 logical points, the editor measured 121.25 points high and the fixed actions occupied y=257–301. Exact draft, editor identity and focus survived height changes to 430 and 700. This extracted-UI probe used inert callbacks and emitted callback-stub warnings; it is geometry evidence, not a full controller or phone pass. |
| Runtime text wrapping | A separate host defect lost Label wrapping during an in-place theme change. The corresponding host repair is required; this bundle does not claim to fix that runtime bug. |
| Original phone pixels, IME, repeated interaction and cold restart | Pending for this candidate. Earlier app screenshots and earlier model runs do not validate these changed bytes. |
| Live Gmail, physical sending and delivery | Not verified. No automated input may approve a send. Android Google authorization remains unavailable. |

The native layout measurement used a local OctoSense validation build. The
private signed fixture used for upcoming phone validation has the same
controller and generated UI bytes, but different private listing/signing
metadata; it is not this unsigned public package and is not an official release.
No profile, credential, device identifier, private message, raw log or signing
key is included here. The existing listing screenshots remain historical and
must be replaced with reviewed current captures before publication.

## 中文

`0.1.2-ux.1` 是基于上述 0.1.1 仓库状态的无签名开发候选版，尚未发布或提交 App Hub。
`v0.1.1` 标签、发布附件、历史截图和签名审核记录不变。

手机上曾出现回复编辑器和操作区被键盘挤出可用空间的问题。此候选版让 Email
中的标题、发件人与正文一起滚动，Reply 正文占用剩余高度，并将 Details、Save、
Review & Send 集中在下方。Details 展开原有收件人与主题编辑器，移除重复标题和
状态行。切换标签不重建草稿；应用和 Glance 仍由同一源文件生成。代理、工具
schema、技能、服务请求和物理发送批准边界均不变。

生成一致性和契约测试覆盖当前源码。Android 风格的原生布局探针在 390 × 320
逻辑点测得正文编辑器高 121.25 点，固定操作区位于 y=257–301；高度变为 430、700
时草稿、控件身份和焦点保持。该探针使用抽取的界面和无功能回调，并出现回调桩
警告，因此仅证明布局，不代表完整控制器或手机验收。另一个主机缺陷会在原地
切换主题时丢失 Label 换行，需要独立的主机修复，本应用没有绕过该问题。

此候选版的手机原始像素、软键盘、持续操作和冷启动验收仍待完成。历史截图及
旧模型测试不验证本次新字节。真实 Gmail、物理发送批准及送达未验证；Android
Google 授权仍不可用。即将用于手机测试的私有签名样本与本候选版控制器和生成
界面字节一致，但其列表和签名元数据不同，不是官方发布。本仓库不包含账户、
凭据、设备标识、私人邮件、原始日志或签名密钥。正式发布前需替换为已审阅的
当前截图。
