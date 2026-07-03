# 金融与 UI Skills 集成方案

## 目标

本项目要从“热点聚合看板”升级为“每日投资研究工作台”。新接入的 skills 不替代人工判断，而是增强数据抓取、信号跟踪、短线复盘、报告生成和 UI 质量检查。

安装后的 skills 需要重启 Codex 才会在新会话中自动可用。

## 金融研究 Skills

- `alphaear-news`：每天 08:00 刷新时抓取多源财经热榜、新闻和预测市场线索，用于发现新主题。
- `alphaear-search`：对热点方向做二次检索，补充来源链接，避免只靠关键词命中。
- `alphaear-stock`：补齐 A 股、港股、美股代码、价格、涨跌幅、市值、PE 等公司详情。
- `alphaear-sentiment`：对新闻标题、公告摘要和研报线索做情绪评分，区分利好、利空和中性信息。
- `alphaear-signal-tracker`：跟踪“存储芯片、CPO、半导体气体、刻蚀、光刻胶、氟化工”等主题是否继续增强、减弱或被证伪。
- `alphaear-predictor`：只作为时间序列辅助工具，输出概率和情景，不作为直接买卖信号。
- `alphaear-deepear-lite`：拉取高频金融信号，作为短线热点雷达的补充源。
- `alphaear-reporter`：把每日数据汇总成 A 股、港股、美股三市场报告和候选池说明。
- `alphaear-logic-visualizer`：为复杂产业链生成逻辑图，例如“AI 算力 -> HBM -> 先进封装 -> 设备材料”。

## 每日工作流

1. `08:00` 运行基础爬虫，更新三市场热点、公司详情和候选池。
2. 开盘前后使用 `news/search/deepear-lite` 做短线主题扫描，重点捕捉细分题材。
3. 收盘后用 `signal-tracker` 复盘主题强弱变化，记录哪些逻辑被价格或新闻验证。
4. 用 `reporter` 输出结构化日报：热点排名、证据、龙头、新贵、风险和明日跟踪项。

短线方向必须更细：月度看产业主线，周度看分支景气，日内看事件催化和资金确认。

## 分时点调度

项目已提供 `scripts/run_pipeline_slot.sh` 和 `scripts/install_market_cron.sh`。

- `08:00 morning`：`news + search + stock + sentiment + signal-tracker + reporter`。
- `09:25 auction`：`stock + news + sentiment`。
- `11:40 midday`：`signal-tracker + reporter`。
- `15:15 close`：`stock + signal-tracker + logic-visualizer + reporter`。
- `21:00 us_premarket`：`news + stock + sentiment + predictor`，其中 predictor 按异步队列处理。

网站 API：

- `/api/skill-pipeline`：查看四层 skills 和五个时点计划。
- `/api/intraday-brief`：输出短线雷达、持仓去留、预测面板和逻辑链。
- `/api/pipeline-runs`：查看最近分时点运行记录。

## UI Skills 使用

- `ui-skills-root`：每次 UI 改版前选择最小必要 UI skill。
- `baseline-ui`：先修层级、间距、字体、数据密度和加载状态。
- `fixing-accessibility`：检查弹窗、按钮、公司详情抽屉和键盘可访问性。
- `fixing-motion-performance`：限制果冻风格动效只使用 `transform` 和 `opacity`，避免刷新和滚动卡顿。
- `fixing-metadata`：完善页面标题、说明和私有站点索引策略。

UI 改版方向是“Apple 风格的轻量金融工作台”：减少杂乱卡片，保留清晰分区、半透明层次、柔和动效和高可读数据表。

## 风险边界

所有 skills 输出都必须保留来源、日期和置信度。若行情、估值或新闻无法交叉验证，页面应标为“待核验”，不能展示成确定结论。任何预测只能用于制定观察计划，不应直接转化为满仓、追涨或融资交易。
