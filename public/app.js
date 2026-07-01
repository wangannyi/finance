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
      const horizons = ["day", "week", "month"]
        .map((horizon) => {
          const rows = (report.horizons[horizon] || [])
            .map(
              (item) => `
                <article class="direction">
                  <div class="direction-title">
                    <strong>${item.name}</strong>
                    <span class="score">${item.score}</span>
                  </div>
                  <div class="evidence">${item.evidence}</div>
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
                </article>`,
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
          <div class="horizon-grid">${horizons}</div>
          <div class="sources">${sources}</div>
        </article>`;
    })
    .join("");
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
  const [reportsResponse, historyResponse] = await Promise.all([fetch("/api/reports"), fetch("/api/history")]);
  const reports = await reportsResponse.json();
  const history = await historyResponse.json();
  renderReports(reports);
  renderHistory(history);
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
