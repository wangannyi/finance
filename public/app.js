const labels = {
  day: "接下来一天",
  week: "接下来一周",
  month: "接下来一个月",
};

let selectedMarket = "all";

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

function hostLabel(url) {
  try {
    return new URL(url).host.replace("www.", "");
  } catch {
    return url;
  }
}

function renderReports(reports) {
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
                    <div class="evidence">${item.evidence}</div>
                    <div class="evidence-sources">
                      ${sourceRows || '<span class="no-source">本轮未命中可展示来源</span>'}
                    </div>
                    <div class="risk">风险：${item.risk}</div>
                    <div class="leaders">
                      ${(item.leaders || [])
                        .map(
                          (leader) =>
                            `<button class="leader" type="button" data-name="${leader.name}" data-symbol="${leader.ticker}" data-detail="${leader.detail}">
                              <strong>${leader.name}</strong> <span>${leader.ticker}</span>：${leader.detail}
                            </button>`,
                        )
                        .join("")}
                    </div>
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
            <div class="generated">更新时间<br>${formatTime(report.generated_at)}</div>
          </div>
          ${discoveries}
          <div class="horizon-grid">${horizons}</div>
          <div class="sources">${sources}</div>
        </article>`;
    })
    .join("");
}

function renderDiscoveries(discoveredThemes) {
  if (!discoveredThemes.length) {
    return '<div class="discovery-empty">主动发现：本轮未捕捉到额外高频新主题</div>';
  }
  return `
    <section class="discovery-panel">
      <div class="discovery-title">
        <strong>主动发现</strong>
        <span>来源扫描，不等于买入建议</span>
      </div>
      <div class="discovery-grid">
        ${discoveredThemes
          .map(
            (theme) => `
              <article class="discovery-card">
                <div class="discovery-card-head">
                  <strong>${theme.name}</strong>
                  <span>${theme.score}</span>
                </div>
                <p>${theme.risk}</p>
                <div class="keyword-line">${(theme.matched_keywords || []).slice(0, 6).join(" / ")}</div>
                <div class="evidence-sources">
                  ${(theme.evidence_sources || [])
                    .slice(0, 2)
                    .map(
                      (source) => `
                        <a class="evidence-source" href="${source.url}" target="_blank" rel="noreferrer">
                          <strong>${source.title || hostLabel(source.url)}</strong>
                          <span>${(source.matched_keywords || []).slice(0, 4).join(" / ")}</span>
                        </a>`,
                    )
                    .join("")}
                </div>
              </article>`,
          )
          .join("")}
      </div>
    </section>`;
}

function renderPortfolio(plan) {
  const container = document.querySelector("#portfolioPlan");
  const marketRows = Object.entries(plan.markets || {})
    .map(
      ([market, item]) => `
        <div class="portfolio-market">
          <span>${item.name}</span>
          <strong>${formatMarketCap(item.target_amount, "CNY")}</strong>
          <small>${(item.target_ratio * 100).toFixed(0)}% · ${item.role}</small>
        </div>`,
    )
    .join("");

  const checks = (plan.risk_checks || []).map((item) => `<li>${item}</li>`).join("");
  const questions = (plan.questions || []).map((item) => `<li>${item}</li>`).join("");

  container.innerHTML = `
    <div class="portfolio-markets">${marketRows}</div>
    <div class="guardrail-row">
      <div><span>单标的上限</span><strong>${formatMarketCap(plan.guardrails.max_single_position_amount, "CNY")}</strong></div>
      <div><span>单主题上限</span><strong>${formatMarketCap(plan.guardrails.max_theme_amount, "CNY")}</strong></div>
      <div><span>建议分批</span><strong>${plan.guardrails.suggested_batches} 次</strong></div>
    </div>
    <div class="check-list">
      <strong>买入前检查</strong>
      <ul>${checks}</ul>
    </div>
    <div class="check-list muted-list">
      <strong>仍需你确认</strong>
      <ul>${questions}</ul>
    </div>`;
}

function renderDataSnapshot(snapshot) {
  const container = document.querySelector("#dataSnapshot");
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

function renderCandidates(pool) {
  const container = document.querySelector("#candidatePool");
  const limit = document.querySelector("#candidateLimit");
  const candidates = pool.candidates || [];
  limit.textContent = `单标的上限 ${formatMarketCap(pool.limits?.max_single_position_amount, "CNY")}`;

  if (!candidates.length) {
    container.innerHTML = '<div class="empty">暂无候选标的。先点击“立即更新”生成三市场报告。</div>';
    return;
  }

  container.innerHTML = `
    <div class="candidate-header">
      <span>公司</span>
      <span>市场</span>
      <span>主题</span>
      <span>动作</span>
      <span>上限</span>
      <span>风险</span>
    </div>
    ${candidates
      .slice(0, 18)
      .map(
        (item) => `
          <div class="candidate-row">
            <button class="leader candidate-company" type="button" data-name="${item.name}" data-symbol="${item.symbol}" data-detail="${item.leader_detail}">
              <strong>${item.name}</strong><span>${item.symbol}</span>
            </button>
            <span>${item.market_name}</span>
            <span>${item.themes.slice(0, 2).join(" / ")}</span>
            <strong>${item.action}</strong>
            <span>${formatMarketCap(item.max_observation_amount, "CNY")}</span>
            <span>${item.risk_tags.join("、")}</span>
          </div>`,
      )
      .join("")}
    <div class="candidate-note">候选池只用于观察和买入前检查，不代表买入建议。真正交易前需要核验财报、公告、估值和仓位。</div>`;
}

function showCompanyLoading(name, symbol) {
  document.querySelector("#companyTitle").textContent = `${name} ${symbol}`;
  document.querySelector("#companyBody").innerHTML = '<div class="empty">正在从本机服务查询公司行情...</div>';
  document.querySelector("#companyOverlay").hidden = false;
}

function renderCompany(metrics, detail) {
  const returns = metrics.returns || {};
  document.querySelector("#companyTitle").textContent = `${metrics.name || ""} ${metrics.symbol || ""}`;
  document.querySelector("#companyBody").innerHTML = `
    ${metrics.error ? `<div class="warning">${metrics.error}</div>` : ""}
    <div class="metric-grid">
      <div><span>当前价格</span><strong>${formatNumber(metrics.price)} ${metrics.currency || ""}</strong></div>
      <div><span>市值</span><strong>${formatMarketCap(metrics.market_cap, metrics.currency)}</strong></div>
      <div><span>PE</span><strong>${formatNumber(metrics.trailing_pe)}</strong></div>
      <div><span>Forward PE</span><strong>${formatNumber(metrics.forward_pe)}</strong></div>
      <div><span>近 3 天</span><strong class="${percentClass(returns.three_day)}">${formatPercent(returns.three_day)}</strong></div>
      <div><span>近 1 周</span><strong class="${percentClass(returns.one_week)}">${formatPercent(returns.one_week)}</strong></div>
      <div><span>近 1 个月</span><strong class="${percentClass(returns.one_month)}">${formatPercent(returns.one_month)}</strong></div>
      <div><span>股息率</span><strong>${metrics.dividend_yield ? formatPercent(metrics.dividend_yield * 100) : "暂无数据"}</strong></div>
      <div><span>52 周高点</span><strong>${formatNumber(metrics.fifty_two_week_high)}</strong></div>
      <div><span>52 周低点</span><strong>${formatNumber(metrics.fifty_two_week_low)}</strong></div>
    </div>
    <div class="company-note">
      <p><strong>龙头说明：</strong>${detail || "暂无补充说明"}</p>
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
    document.querySelector("#companyBody").innerHTML = '<div class="warning">公司详情查询失败，请稍后再试。</div>';
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

async function loadData() {
  const [reportsResponse, historyResponse, portfolioResponse, snapshotResponse, candidatesResponse] = await Promise.all([
    fetch("/api/reports"),
    fetch("/api/history"),
    fetch("/api/portfolio"),
    fetch("/api/data-snapshot"),
    fetch("/api/candidates"),
  ]);
  const reports = await reportsResponse.json();
  const history = await historyResponse.json();
  const portfolio = await portfolioResponse.json();
  const snapshot = await snapshotResponse.json();
  const candidates = await candidatesResponse.json();
  renderReports(reports);
  renderHistory(history);
  renderPortfolio(portfolio);
  renderDataSnapshot(snapshot);
  renderCandidates(candidates);
}

async function refreshData() {
  const status = document.querySelector("#status");
  const button = document.querySelector("#refreshBtn");
  button.disabled = true;
  status.textContent = "本地爬虫运行中...";
  try {
    await fetch("/api/refresh");
    await loadData();
    status.textContent = "已更新到本地数据库";
  } catch (error) {
    status.textContent = "更新失败，请看终端日志";
  } finally {
    button.disabled = false;
  }
}

document.querySelectorAll(".market-tab").forEach((button) => {
  button.addEventListener("click", async () => {
    selectedMarket = button.dataset.market;
    document.querySelectorAll(".market-tab").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    await loadData();
  });
});

document.querySelector("#refreshBtn").addEventListener("click", refreshData);
document.querySelector("#closeCompanyPanel").addEventListener("click", () => {
  document.querySelector("#companyOverlay").hidden = true;
});
document.querySelector("#companyOverlay").addEventListener("click", (event) => {
  if (event.target.id === "companyOverlay") {
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
setInterval(loadData, 5 * 60 * 1000);
