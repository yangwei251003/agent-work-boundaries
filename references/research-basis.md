# 研究依据与取舍

仅在维护本技能、设计评估或追溯理由时阅读；执行普通任务不必加载。

## 视频原始方法

[一只桌子的 5 分钟视频](https://www.douyin.com/video/7685681479640272180)围绕四个边界：项目文件夹保留经验和工具环境；对话按工序与过长任务交接；子 Agent 的价值在上下文隔离，作者用网页替身承担独立资料工作；同仓库多路写入时用 Worktree 隔离并在最后整合。作者演示了交接提醒与网页替身两项常驻 Skill，而不是要求每个任务都开子 Agent 或 Worktree。

证据来自页面章节、完整音轨自动转写、24 张抽样画面的 OCR，以及 Browser Use 对全片画面的逐段查看。自动转写有同音字错误；Browser Use 能看画面但不能听音频；画面未逐帧核对。工程扩展不要写成作者原话。

## 可借鉴的实现

| 来源 | 借鉴点 | 本技能的取舍 |
| --- | --- | --- |
| [Letta Code](https://github.com/letta-ai/letta-code/blob/main/src/agent/prompts/letta.md) | 可编辑的文件式记忆、近期上下文与外部记忆分层 | 沿用项目文件与交接分层，不安装新的记忆服务 |
| [Graphiti](https://github.com/getzep/graphiti) | 事实随时间变化，保留原始来源与有效期 | 用简短来源、核实时间和“已替代”记录，暂不引入图数据库 |
| [A-MEM 论文](https://arxiv.org/abs/2502.12110) | 新知识可以修订、连接旧记忆 | 更新现有权威条目；仅在确有导航价值时添加链接 |
| [LongMemEval 论文](https://arxiv.org/abs/2410.10813) | 长期记忆需要处理信息抽取、跨会话、时间更新与无法回答；过度压成孤立事实会失去上下文 | 保留适用条件、来源和决策理由；证据不足时不写成事实 |
| [Cline 子 Agent](https://github.com/cline/cline/blob/main/docs/features/subagents.mdx)、[Anthropic 多 Agent 经验](https://www.anthropic.com/engineering/multi-agent-research-system) | 独立上下文能隔离大量探索，但委派和整合有成本 | 只派可独立验收的工作，主 Agent 核对结果 |
| [Browser Use 子任务指南](https://github.com/browser-use/browser-use/blob/main/skills/cloud/references/guides/subagent.md) | 完整网页子任务可按“任务进入、结果返回”分流 | 网页替身限于有界资料任务；状态未知时防止重复提交 |
| [Git Worktree 文档](https://git-scm.com/docs/git-worktree) | 同一仓库可有多个独立工作目录，共享历史但各有工作区状态 | 并行写入才考虑 Worktree；共享文件指定唯一 writer |
| [OpenAI 关于精简技能的建议](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | 能力更强的模型可能被过细流程约束 | 入口保留触发与不变量，细节按需加载；简单任务跳过 |

## 保留的边界

这是一套供 Agent 判断和更新文件的技能，不是后台常驻进程、自动训练机制或新建网页账号的许可。首次采用时用真实任务对照验证：是否把记忆写到正确项目，是否更新过期事实，是否在上下文压缩前保留状态，是否只把有界独立工作交给网页替身/子 Agent，以及同仓库并行修改后是否完成集成验证。未做配对评估前不声称总体质量或 token 使用一定改善。
