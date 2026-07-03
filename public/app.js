const labels = {
  day: "接下来一天",
  week: "接下来一周",
  month: "接下来一个月",
};

let selectedMarket = "all";
let currentReports = [];
let currentCandidatePool = { candidates: [], limits: {} };
let currentWorkflow = { stages: [], tracked_signals: [] };
let currentIntradayBrief = { radar: [], holdings: [], signals: [], predictions: [], logic_chains: [] };
let currentPipelineStatus = { slots: [] };
let currentPipelineRuns = [];
let candidateCollapsed = true;
let candidateMetricsRequestId = 0;

function formatNumber(value) {
  if (value === null || value === undefined) return "暂无数据";
  return new Intl.NumberFormat("zh-CN", { maximumFractionDigits: 2 }).format(value);
}

function formatMarketCap(value, currency) {
  if (!value) return "暂无数据";
  const units = [
    { label: "万亿", divisor: 1_000_000_000_000 },
    { label: "亿", divisor: 100_000_000 },
    { label: "万", divisor: 10_000 },
  ];
  const unit = units.find((item) => value >= item.divisor) || { label: "", divisor: 1 };
  return `${formatNumber(value / unit.divisor)}${unit.label} ${currency || ""}`.trim();
}

function formatPercent(value) {
  if (value === null || value === undefined) return "暂无数据";
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

function percentClass(value) {
  if (value > 0) return "up";
  if (value < 0) return "down";
  return "";
}

function formatTime(value) {
  if (!value) return "未知时间";
  return new Date(value).toLocaleString("zh-CN", { hour12: false });
}

function marketDisplayName(market) {
  return { ch: "A 股", hk: "港股", us: "美股" }[market] || market;
}

function latestReportTime(reports) {
  return reports
    .map((report) => report.generated_at)
    .filter(Boolean)
    .sort()
    .at(-1);
}

function hostLabel(url) {
  try {
    return new URL(url).host.replace("www.", "");
  } catch {
    return url;
  }
}

function renderReports(reports) {
  currentReports = reports;
  const container = document.querySelector("#reports");
  const visible = selectedMarket === "all" ? reports : reports.filter((item) => item.market === selectedMarket);

  if (visible.length === 0) {
    container.innerHTML = '<div class="empty">暂无数据。点击“立即更新”生成第一批本地报告。</div>';
    return;
  }

  container.innerHTML = visible
    .map((report) => {
      const discoveries = renderDiscoveries(report.discovered_themes || []);
      const horizons = ["day", "week", "month"]
        .map((horizon) => {
          const rows = (report.horizons[horizon] || [])
            .map(
              (item) => {
                const sourceRows = (item.evidence_sources || [])
                  .map(
                    (source) => `
                      <a class="evidence-source" href="${source.url}" target="_blank" rel="noreferrer">
                        <strong>${source.title || hostLabel(source.url)}</strong>
                        <span>${(source.matched_keywords || []).slice(0, 4).join(" / ")}</span>
                      </a>`,
                  )
                  .join("");
                return `
                  <article class="direction">
                    <div class="direction-title">
                      <strong>${item.name}</strong>
                      <span class="score">${item.score}</span>
                    </div>
                    <details class="direction-detail">
                      <summary>公司清单、证据与风险</summary>
                      <div class="company-groups">
                        ${renderCompanyGroup("代表龙头", item.leaders || [])}
                        ${renderCompanyGroup("高弹性标的", item.challengers || [])}
                      </div>
                      <div class="evidence">${item.evidence}</div>
                      <div class="risk">风险：${item.risk}</div>
                      <div class="evidence-sources">
                        ${sourceRows || '<span class="no-source">本轮未命中可展示来源</span>'}
                      </div>
                    </details>
                  </article>`;
              },
            )
            .join("");
          return `<section class="horizon"><h3>${labels[horizon]}</h3>${rows}</section>`;
        })
        .join("");

      const sources = (report.sources || [])
        .map((source) => `<a href="${source}" target="_blank" rel="noreferrer">${hostLabel(source)}</a>`)
        .join("");

      return `
        <article class="market-card">
          <div class="market-head">
            <div>
              <h2>${report.market_name}</h2>
              <p>${report.summary}</p>
            </div>
            <div class="generated">${formatTime(report.generated_at)}</div>
          </div>
          ${discoveries}
          <div class="horizon-grid">${horizons}</div>
          <details class="source-wrap">
            <summary>数据来源</summary>
            <div class="sources">${sources}</div>
          </details>
        </article>`;
    })
    .join("");
}

function renderCompanyGroup(title, companies) {
  const rows = companies
    .slice(0, 5)
    .map(
      (company) =>
        `<button class="leader" type="button" data-name="${company.name}" data-symbol="${company.ticker}" data-detail="${company.detail}">
          <strong>${company.name}</strong><span>${company.ticker}</span>
        </button>`,
    )
    .join("");
  return `
    <div class="company-group">
      <strong>${title}</strong>
      <div class="leaders">
        ${rows || '<span class="no-source">暂无高置信标的</span>'}
      </div>
    </div>`;
}

function renderDiscoveries(discoveredThemes) {
  if (!discoveredThemes.length) {
    return '<div class="discovery-empty">主动发现：本轮未捕捉到额外高频新主题</div>';
  }
  return `
    <section class="discovery-panel">
      <div class="discovery-title">
        <strong>主动发现</strong>
      </div>
      <div class="discovery-grid">
        ${discoveredThemes
          .map(
            (theme) => `
              <details class="discovery-chip">
                <summary><strong>${theme.name}</strong><span>${theme.score}</span></summary>
                <p>${theme.risk}</p>
                <div class="keyword-line">${(theme.matched_keywords || []).slice(0, 6).join(" / ")}</div>
              </details>`,
          )
          .join("")}
      </div>
    </section>`;
}

function flattenDirections(reports) {
  return reports.flatMap((report) =>
    ["day", "week", "month"].flatMap((horizon) =>
      (report.horizons?.[horizon] || []).map((direction) => ({
        ...direction,
        horizon,
        market: report.market,
        marketName: report.market_name,
        generatedAt: report.generated_at,
      })),
    ),
  );
}

function renderDecisionSummary(plan, reports, pool) {
  const container = document.querySelector("#decisionSummary");
  const updated = document.querySelector("#insightUpdated");
  const candidates = pool.candidates || [];
  const directions = flattenDirections(reports).sort((a, b) => (b.score || 0) - (a.score || 0));
  const topDirection = directions[0];
  const riskDirection =
    directions.find((item) => /高波动|估值|追高|回撤|风险|波动/.test(`${item.risk || ""}${item.name || ""}`)) || directions[1];
  const lowPosition =
    directions.find((item) => item.score < 180 || /材料|光刻胶|电子特气|氟化工|刻蚀/.test(item.name || "")) || directions[2];
  const noChase =
    directions.find((item) => item.horizon === "day" && (item.score || 0) > 220) || directions.find((item) => item.horizon === "day");
  const latestTime = latestReportTime(reports);
  const dayThemes = reports.reduce((sum, report) => sum + (report.horizons?.day || []).length, 0);
  const highRiskCount = candidates.filter((item) => (item.risk_tags || []).some((tag) => tag.includes("高波动"))).length;
  const singleLimit = plan.guardrails?.max_single_position_amount;
  const themeLimit = plan.guardrails?.max_theme_amount;

  updated.textContent = latestTime ? `更新于 ${formatTime(latestTime)}` : "等待更新";

  if (!reports.length) {
    container.innerHTML = '<div class="empty">暂无报告。点击“立即更新”生成今日市场摘要。</div>';
    return;
  }

  container.innerHTML = `
    <div class="summary-grid">
      ${renderDecisionTile("今日最强方向", topDirection, "focus-tile")}
      ${renderDecisionTile("风险最高方向", riskDirection)}
      ${renderDecisionTile("可埋伏方向", lowPosition)}
      ${renderDecisionTile("不能追方向", noChase)}
    </div>
    <div class="decision-meta-row">
      <span>今日主题 ${dayThemes} 个</span>
      <span>候选池 ${candidates.length} 个</span>
      <span>高波动 ${highRiskCount} 个</span>
      <span>单标的上限 ${formatMarketCap(singleLimit, "CNY")}</span>
      <span>单主题上限 ${formatMarketCap(themeLimit, "CNY")}</span>
    </div>
    <div class="summary-action">
      <strong>执行顺序：</strong>
      先看持仓纪律，再看题材证据；没有公告、财报或估值验证前，不把热点当买入信号。
    </div>`;
}

function renderDecisionTile(title, direction, className = "") {
  return `
    <div class="summary-tile ${className}">
      <span>${title}</span>
      <strong>${direction ? direction.name : "暂无方向"}</strong>
      <small>${direction ? `${direction.marketName} · ${labels[direction.horizon]} · 热度 ${direction.score}` : "等待刷新"}</small>
    </div>`;
}

function renderMarketStatus(reports, pipelineRuns) {
  const chips = document.querySelector("#marketStatusBar");
  const globalUpdated = document.querySelector("#globalUpdated");
  const dataHealth = document.querySelector("#dataHealth");
  if (!chips) return;
  const latestTime = latestReportTime(reports);
  const latestRun = pipelineRuns?.[0]?.payload;
  const resultRows = latestRun?.skill_results || [];
  const degradedCount = resultRows.filter((item) => ["error", "degraded"].includes(item.status)).length;
  const okCount = resultRows.filter((item) => ["ok", "agentic", "queued_async"].includes(item.status)).length;
  globalUpdated.textContent = latestTime ? `数据 ${formatTime(latestTime)}` : "等待刷新";
  dataHealth.textContent = resultRows.length ? `数据源 ${okCount}/${resultRows.length}` : "数据源待检";
  dataHealth.classList.toggle("warn", degradedCount > 0);
  chips.innerHTML = ["ch", "hk", "us"]
    .map((market) => {
      const report = reports.find((item) => item.market === market);
      const dayCount = report?.horizons?.day?.length || 0;
      const top = report?.horizons?.day?.[0]?.name || "等待数据";
      return `<span class="market-status-chip ${report ? "is-live" : ""}"><strong>${marketDisplayName(market)}</strong><em>${dayCount} 方向</em><small>${top}</small></span>`;
    })
    .join("");
}

function renderResearchWorkflow(workflow) {
  currentWorkflow = workflow || { stages: [], tracked_signals: [] };
  const container = document.querySelector("#researchWorkflow");
  if (!container) return;
  const stages = currentWorkflow.stages || [];
  const signals = currentWorkflow.tracked_signals || [];
  const visibleSignals =
    selectedMarket === "all" ? signals.slice(0, 8) : signals.filter((item) => item.market === selectedMarket).slice(0, 8);

  if (!stages.length && !signals.length) {
    container.innerHTML = '<div class="empty compact-empty">等待每日刷新后生成研究工作流。</div>';
    return;
  }

  container.innerHTML = `
    <div class="workflow-strip">
      ${stages
        .map(
          (stage, index) => `
            <div class="workflow-step">
              <span>${String(index + 1).padStart(2, "0")}</span>
              <strong>${stage.name}</strong>
              <small>${(stage.skills || []).join(" / ")}</small>
            </div>`,
        )
        .join("")}
    </div>
    <div class="signal-board">
      <div class="signal-head">
        <strong>短线信号雷达</strong>
        <span>${currentWorkflow.refresh_cadence || "08:00 daily"} · ${formatTime(currentWorkflow.latest_update)}</span>
      </div>
      <div class="signal-list">
        ${
          visibleSignals.length
            ? visibleSignals
                .map(
                  (signal) => `
                    <article class="signal-row">
                      <div>
                        <strong>${signal.name}</strong>
                        <span>${signal.market_name} · ${signal.horizons?.join(" / ") || signal.primary_horizon}</span>
                      </div>
                      <div class="signal-status ${signal.status === "增强" ? "hot" : ""}">${signal.status}</div>
                      <p>${signal.next_action}</p>
                    </article>`,
                )
                .join("")
            : '<div class="empty compact-empty">当前筛选市场暂无信号。</div>'
        }
      </div>
    </div>`;
}

function renderPipelineSlots(status) {
  currentPipelineStatus = status || { slots: [] };
  const container = document.querySelector("#pipelineSlots");
  if (!container) return;
  const slots = currentPipelineStatus.slots || [];
  if (!slots.length) {
    container.innerHTML = '<div class="empty compact-empty">等待加载分时点计划。</div>';
    return;
  }
  container.innerHTML = slots
    .map(
      (slot) => `
        <div class="slot-chip">
          <strong>${slot.time}</strong>
          <span>${slot.title}</span>
          <small>${(slot.skills || []).length} skills${slot.async_only ? " · 异步" : ""}</small>
        </div>`,
    )
    .join("");
}

function renderSkillRunStatus(runs) {
  currentPipelineRuns = runs || [];
  const container = document.querySelector("#skillRunStatus");
  if (!container) return;
  const latest = currentPipelineRuns[0]?.payload;
  if (!latest) {
    container.innerHTML = '<div class="empty compact-empty">暂无分时点运行记录。</div>';
    return;
  }
  const rows = latest.skill_results || [];
  container.innerHTML = `
    <div class="skill-run-head">
      <strong>最近运行：${latest.time} ${latest.title}</strong>
      <span>${formatTime(latest.generated_at)}</span>
    </div>
    <div class="skill-run-grid">
      ${
        rows.length
          ? rows
              .map(
                (item) => `
                  <div class="skill-run-chip ${item.status}">
                    <strong>${item.skill}</strong>
                    <span>${item.status}</span>
                    <small>${item.summary || "暂无摘要"}</small>
                  </div>`,
              )
              .join("")
          : '<div class="empty compact-empty">该次运行未启用外部 skill adapter。</div>'
      }
    </div>`;
}

function renderIntradayBrief(brief) {
  currentIntradayBrief = brief || { radar: [], holdings: [], signals: [], predictions: [], logic_chains: [] };
  const container = document.querySelector("#intradayBrief");
  if (!container) return;

  container.innerHTML = `
    <div class="intraday-grid">
      <section class="intraday-card">
        <h3>今日短线雷达</h3>
        ${(currentIntradayBrief.radar || [])
          .map(
            (group) => `
              <div class="radar-group">
                <strong>${group.name}</strong>
                <span>${(group.items || []).join(" / ") || "等待信号"}</span>
                <small>${group.rule}</small>
              </div>`,
          )
          .join("")}
      </section>
      <section class="intraday-card">
        <h3>持仓去留</h3>
        ${(currentIntradayBrief.holdings || [])
          .map(
            (item) => `
              <div class="holding-row action-${item.action}">
                <div class="holding-title">
                  <strong>${item.name}</strong>
                  <span>${item.symbol}</span>
                </div>
                <b>${item.action}</b>
                <div class="holding-metrics">
                  <span>成本 ${formatNumber(item.cost)}</span>
                  <span>数量 ${formatNumber(item.shares)}</span>
                  <span>纪律线 ${formatNumber(item.stop_loss)}</span>
                </div>
                <small>${item.trigger || item.reason}</small>
              </div>`,
          )
          .join("")}
      </section>
      <section class="intraday-card">
        <h3>信号追踪</h3>
        ${(currentIntradayBrief.signals || [])
          .slice(0, 5)
          .map(
            (item) => `
              <div class="tracking-row">
                <div><strong>${item.name}</strong><span>${item.market_name} · ${item.horizons?.join(" / ") || item.primary_horizon}</span></div>
                <b class="${item.status === "增强" ? "hot" : ""}">${item.status}</b>
                <small>${item.next_action}</small>
              </div>`,
          )
          .join("")}
      </section>
      <section class="intraday-card">
        <h3>预测面板</h3>
        ${(currentIntradayBrief.predictions || [])
          .slice(0, 4)
          .map(
            (item) => `
              <div class="prediction-row">
                <strong>${item.name}</strong>
                <span>1日 ${formatProbability(item.horizons?.["1d"])} · 3日 ${formatProbability(item.horizons?.["3d"])} · 5日 ${formatProbability(item.horizons?.["5d"])}</span>
                <small>${item.summary}</small>
              </div>`,
          )
          .join("")}
      </section>
      <section class="intraday-card">
        <h3>逻辑链</h3>
        ${(currentIntradayBrief.logic_chains || [])
          .slice(0, 4)
          .map(
            (item) => `
              <div class="logic-row">
                <strong>${item.name}</strong>
                <span>${(item.chain || []).join(" → ")}</span>
              </div>`,
          )
          .join("")}
      </section>
    </div>`;
}

function formatProbability(item) {
  if (!item) return "待跑";
  return `${Math.round((item.probability || 0) * 100)}% ${item.bias || ""}`.trim();
}

function renderDataSnapshot(snapshot) {
  const container = document.querySelector("#dataSnapshot");
  if (!container) return;
  const status = snapshot.status || {};
  const aShareCount = (snapshot.a_share || []).length;
  const hkCount = (snapshot.hk || []).length;
  const errors = snapshot.errors || [];
  const samples = [...(snapshot.a_share || []).slice(0, 3), ...(snapshot.hk || []).slice(0, 3)]
    .map(
      (item) => `
        <div class="snapshot-row">
          <strong>${item.name || item.symbol}</strong>
          <span>${item.symbol}</span>
          <span>${formatNumber(item.price)}</span>
          <span class="${percentClass(item.change_pct)}">${formatPercent(item.change_pct)}</span>
        </div>`,
    )
    .join("");

  container.innerHTML = `
    <div class="${status.available ? "data-ok" : "warning"}">${status.message || "数据源状态未知"}</div>
    ${errors.length ? `<div class="warning">${errors.join("<br>")}</div>` : ""}
    <div class="data-counts">
      <div><span>A 股快照</span><strong>${aShareCount}</strong></div>
      <div><span>港股快照</span><strong>${hkCount}</strong></div>
    </div>
    ${samples ? `<div class="snapshot-list">${samples}</div>` : '<div class="empty">安装 AKShare 后可显示 A 股/港股增强行情快照。</div>'}`;
}

function renderSnapshotLoading() {
  const container = document.querySelector("#dataSnapshot");
  if (container) container.innerHTML = '<div class="empty compact-empty">行情快照加载中...</div>';
}

function renderSnapshotIdle() {
  const container = document.querySelector("#dataSnapshot");
  if (container) container.innerHTML = '<div class="empty compact-empty">行情快照按需加载，不影响首屏速度。</div>';
}

function renderCandidates(pool) {
  currentCandidatePool = pool;
  const container = document.querySelector("#candidatePool");
  const limit = document.querySelector("#candidateLimit");
  const panel = document.querySelector(".candidate-panel");
  const candidates =
    selectedMarket === "all"
      ? pool.candidates || []
      : (pool.candidates || []).filter((item) => item.market === selectedMarket);
  limit.textContent = `${candidateCollapsed ? "折叠显示前排" : "完整显示"} · 共 ${candidates.length} 个 · 单标的上限 ${formatMarketCap(pool.limits?.max_single_position_amount, "CNY")}`;
  panel.classList.toggle("is-collapsed", candidateCollapsed);
  updateCandidateToggle();

  if (!candidates.length) {
    container.innerHTML = '<div class="empty">当前市场暂无候选标的。先点击“立即更新”生成最新报告。</div>';
    return;
  }

  const visibleCandidates = candidateCollapsed ? candidates.slice(0, 12) : candidates;
  container.innerHTML = `
    <div class="candidate-grid">
    ${visibleCandidates
      .map(
        (item) => `
          <article class="candidate-card">
            <button class="leader candidate-company" type="button" data-name="${item.name}" data-symbol="${item.symbol}" data-detail="${item.leader_detail}">
              <strong>${item.name}</strong><span>${item.symbol}</span>
            </button>
            <div class="candidate-meta">
              <span>${item.market_name}</span>
              <strong>${item.action}</strong>
              <span>${formatMarketCap(item.max_observation_amount, "CNY")}</span>
            </div>
            <div class="candidate-fundamentals" data-symbol="${item.symbol}">
              <span>市值：加载中</span>
              <span>PE：加载中</span>
              <span class="candidate-updated">更新：加载中</span>
            </div>
            <p>${item.themes.slice(0, 2).join(" / ")}</p>
            <small>${item.risk_tags.join("、")}</small>
          </article>`,
      )
      .join("")}
    </div>`;
  hydrateCandidateFundamentals(visibleCandidates);
}

function updateCandidateToggle() {
  const button = document.querySelector("#candidateToggle");
  if (!button) return;
  button.textContent = candidateCollapsed ? "展开" : "收起";
  button.setAttribute("aria-expanded", String(!candidateCollapsed));
}

async function hydrateCandidateFundamentals(candidates) {
  const requestId = (candidateMetricsRequestId += 1);
  let nextIndex = 0;
  const workerCount = Math.min(6, candidates.length);

  async function hydrateOne(item) {
    const target = Array.from(document.querySelectorAll(".candidate-fundamentals")).find(
      (element) => element.dataset.symbol === item.symbol,
    );
    if (!target) return;

    try {
      const params = new URLSearchParams({ symbol: item.symbol, name: item.name });
      const response = await fetch(`/api/company?${params.toString()}`);
      const metrics = await response.json();
      if (requestId !== candidateMetricsRequestId) return;
      const marketCap = formatMarketCap(metrics.market_cap, metrics.currency);
      const peValue = metrics.trailing_pe ?? metrics.forward_pe;
      const pe = peValue === null || peValue === undefined ? "不适用" : formatNumber(peValue);
      target.innerHTML = `<span>市值：${marketCap}</span><span>PE：${pe}</span><span class="candidate-updated">更新：${formatTime(metrics.fetched_at)}</span>`;
    } catch {
      if (requestId !== candidateMetricsRequestId) return;
      target.innerHTML = '<span>市值：暂无数据</span><span>PE：暂无数据</span><span class="candidate-updated">更新：暂无数据</span>';
    }
  }

  async function worker() {
    while (nextIndex < candidates.length) {
      const item = candidates[nextIndex];
      nextIndex += 1;
      await hydrateOne(item);
    }
  }

  await Promise.allSettled(Array.from({ length: workerCount }, worker));
}

function showCompanyLoading(name, symbol) {
  document.querySelector("#companyTitle").textContent = `${name} ${symbol}`;
  document.querySelector("#companyBody").innerHTML = '<div class="empty">正在从本机服务查询公司行情...</div>';
  document.querySelector("#companyOverlay").hidden = false;
}

function renderCompany(metrics, detail) {
  const returns = metrics.returns || {};
  const peValue = metrics.trailing_pe ?? metrics.forward_pe;
  const pe = peValue === null || peValue === undefined ? "不适用" : formatNumber(peValue);
  const forwardPe = metrics.forward_pe === null || metrics.forward_pe === undefined ? "不适用" : formatNumber(metrics.forward_pe);
  document.querySelector("#companyTitle").textContent = `${metrics.name || ""} ${metrics.symbol || ""}`;
  document.querySelector("#companyBody").innerHTML = `
    <div class="metric-grid">
      <div><span>当前价格</span><strong>${formatNumber(metrics.price)} ${metrics.currency || ""}</strong></div>
      <div><span>市值</span><strong>${formatMarketCap(metrics.market_cap, metrics.currency)}</strong></div>
      <div><span>PE</span><strong>${pe}</strong></div>
      <div><span>Forward PE</span><strong>${forwardPe}</strong></div>
      <div><span>近 3 天</span><strong class="${percentClass(returns.three_day)}">${formatPercent(returns.three_day)}</strong></div>
      <div><span>近 1 周</span><strong class="${percentClass(returns.one_week)}">${formatPercent(returns.one_week)}</strong></div>
      <div><span>近 1 个月</span><strong class="${percentClass(returns.one_month)}">${formatPercent(returns.one_month)}</strong></div>
      <div><span>近 6 个月</span><strong class="${percentClass(returns.six_month)}">${formatPercent(returns.six_month)}</strong></div>
      <div><span>股息率</span><strong>${metrics.dividend_yield ? formatPercent(metrics.dividend_yield * 100) : "暂无数据"}</strong></div>
      <div><span>52 周高点</span><strong>${formatNumber(metrics.fifty_two_week_high)}</strong></div>
      <div><span>52 周低点</span><strong>${formatNumber(metrics.fifty_two_week_low)}</strong></div>
    </div>
    <div class="company-note">
      <p><strong>入选理由：</strong>${detail || "暂无补充说明"}</p>
      <p><strong>数据源：</strong>${metrics.source || "Yahoo Finance"}；更新时间：${formatTime(metrics.fetched_at)}</p>
      <p><strong>使用限制：</strong>行情字段可能延迟或缺失，买入前仍需核验交易所公告、财报和估值。</p>
    </div>`;
}

async function openCompanyPanel(button) {
  const symbol = button.dataset.symbol;
  const name = button.dataset.name;
  const detail = button.dataset.detail;
  showCompanyLoading(name, symbol);
  try {
    const params = new URLSearchParams({ symbol, name });
    const response = await fetch(`/api/company?${params.toString()}`);
    const metrics = await response.json();
    renderCompany(metrics, detail);
  } catch (error) {
    document.querySelector("#companyBody").innerHTML = '<div class="empty">公司数据暂不可用，请稍后重试。</div>';
  }
}

function renderHistory(history) {
  const container = document.querySelector("#history");
  if (!history.length) {
    container.innerHTML = '<div class="empty">暂无历史记录</div>';
    return;
  }
  container.innerHTML = history
    .map((item) => {
      const first = item.horizons?.day?.[0]?.name || "暂无方向";
      return `<div class="ticker-row"><strong>${item.market_name}</strong><span>${formatTime(item.generated_at)}</span><span>${first}</span></div>`;
    })
    .join("");
}

async function loadCoreData() {
  const [
    reportsResponse,
    portfolioResponse,
    candidatesResponse,
    workflowResponse,
    pipelineResponse,
    intradayResponse,
    pipelineRunsResponse,
  ] = await Promise.all([
    fetch("/api/reports"),
    fetch("/api/portfolio"),
    fetch("/api/candidates"),
    fetch("/api/research-workflow"),
    fetch("/api/skill-pipeline"),
    fetch("/api/intraday-brief"),
    fetch("/api/pipeline-runs"),
  ]);
  const reports = await reportsResponse.json();
  const portfolio = await portfolioResponse.json();
  const candidates = await candidatesResponse.json();
  const workflow = await workflowResponse.json();
  const pipeline = await pipelineResponse.json();
  const intraday = await intradayResponse.json();
  const pipelineRuns = await pipelineRunsResponse.json();
  renderReports(reports);
  renderDecisionSummary(portfolio, reports, candidates);
  renderMarketStatus(reports, pipelineRuns);
  renderPipelineSlots(pipeline);
  renderSkillRunStatus(pipelineRuns);
  renderResearchWorkflow(workflow);
  renderIntradayBrief(intraday);
  renderCandidates(candidates);
  warmCompanyCache();
}

async function warmCompanyCache() {
  try {
    await fetch("/api/preload-companies");
  } catch {
    // Company details still load on demand if background preload is unavailable.
  }
}

async function loadSecondaryData() {
  try {
    const historyResponse = await fetch("/api/history");
    renderHistory(await historyResponse.json());
  } catch {
    document.querySelector("#history").innerHTML = '<div class="warning">历史记录加载失败</div>';
  }
}

async function loadData() {
  await loadCoreData();
  loadSecondaryData();
}

async function loadSnapshot() {
  const button = document.querySelector("#loadSnapshotBtn");
  button.disabled = true;
  renderSnapshotLoading();
  try {
    const snapshotResponse = await fetch("/api/data-snapshot");
    renderDataSnapshot(await snapshotResponse.json());
  } catch {
    document.querySelector("#dataSnapshot").innerHTML = '<div class="warning">行情快照加载失败</div>';
  } finally {
    button.disabled = false;
  }
}

async function pollRefresh() {
  const status = document.querySelector("#status");
  const button = document.querySelector("#refreshBtn");
  for (let i = 0; i < 120; i += 1) {
    const response = await fetch("/api/refresh-status");
    const payload = await response.json();
    if (payload.status === "complete") {
      status.textContent = `已更新 ${payload.saved_count || 0} 个市场`;
      await loadCoreData();
      loadSecondaryData();
      button.disabled = false;
      return;
    }
    if (payload.status === "error") {
      status.textContent = payload.error || "更新失败";
      button.disabled = false;
      return;
    }
    status.textContent = "后台刷新中...";
    await new Promise((resolve) => setTimeout(resolve, 2000));
  }
  status.textContent = "刷新仍在后台运行";
  button.disabled = false;
}

async function refreshData() {
  const status = document.querySelector("#status");
  const button = document.querySelector("#refreshBtn");
  button.disabled = true;
  status.textContent = "启动后台刷新...";
  try {
    await fetch("/api/refresh");
    pollRefresh();
  } catch (error) {
    status.textContent = "更新失败，请看终端日志";
    button.disabled = false;
  }
}

document.querySelectorAll(".market-tab").forEach((button) => {
  button.addEventListener("click", async () => {
    selectedMarket = button.dataset.market;
    document.querySelectorAll(".market-tab").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    renderReports(currentReports);
    renderResearchWorkflow(currentWorkflow);
    renderCandidates(currentCandidatePool);
  });
});

document.querySelector("#refreshBtn").addEventListener("click", refreshData);
document.querySelector("#loadSnapshotBtn")?.addEventListener("click", loadSnapshot);
document.querySelector("#candidateToggle").addEventListener("click", () => {
  candidateCollapsed = !candidateCollapsed;
  renderCandidates(currentCandidatePool);
});
document.querySelector("#closeCompanyPanel").addEventListener("click", () => {
  document.querySelector("#companyOverlay").hidden = true;
});
document.querySelector("#companyOverlay").addEventListener("click", (event) => {
  if (event.target.id === "companyOverlay") {
    document.querySelector("#companyOverlay").hidden = true;
  }
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    document.querySelector("#companyOverlay").hidden = true;
  }
});
document.addEventListener("click", (event) => {
  const leaderButton = event.target.closest(".leader");
  if (leaderButton) {
    openCompanyPanel(leaderButton);
  }
});

loadData();
setInterval(loadCoreData, 5 * 60 * 1000);
