MARKET_CONFIGS = {
    "ch": {
        "code": "ch",
        "name": "A 股",
        "summary": "结构性行情为主，科技硬制造和业绩验证是当前主线，防守端关注红利资产。",
        "sources": [
            "https://stock.eastmoney.com/",
            "https://finance.sina.com.cn/stock/",
            "https://www.cls.cn/",
            "https://www.stcn.com/",
            "https://www.cls.cn/detail/2411748",
            "https://wap.eastmoney.com/a/202606253783247759.html",
            "https://www.stcn.com/article/detail/3980016.html",
            "https://www.stcn.com/article/detail/3978374.html",
        ],
        "directions": [
            {
                "name": "AI 算力硬件",
                "keywords": ["AI", "算力", "CPO", "PCB", "GPU", "光模块", "服务器"],
                "risk": "估值偏高，业绩兑现或海外订单低于预期时回撤会很大。",
                "leaders": [
                    ("中际旭创", "300308.SZ", "光模块龙头，关注海外 AI 资本开支和毛利率。"),
                    ("新易盛", "300502.SZ", "高速光模块代表，关注订单持续性。"),
                    ("沪电股份", "002463.SZ", "AI 服务器 PCB 代表，关注产能和客户结构。"),
                ],
            },
            {
                "name": "半导体国产替代",
                "keywords": ["半导体", "芯片", "设备", "材料", "国产替代", "先进封装"],
                "risk": "周期波动和技术验证周期长，部分公司估值已反映较高预期。",
                "leaders": [
                    ("北方华创", "002371.SZ", "半导体设备平台型龙头。"),
                    ("中微公司", "688012.SH", "刻蚀和薄膜设备代表。"),
                    ("华海清科", "688120.SH", "CMP 设备核心公司。"),
                ],
            },
            {
                "name": "创新药/CXO",
                "keywords": ["创新药", "医药", "CXO", "出海", "授权", "临床"],
                "risk": "研发失败、医保控费、海外监管和融资环境都会影响估值。",
                "leaders": [
                    ("恒瑞医药", "600276.SH", "国内创新药龙头，关注管线和海外授权。"),
                    ("百济神州-U", "688235.SH", "全球化创新药代表，关注商业化效率。"),
                    ("药明康德", "603259.SH", "CXO 龙头，关注海外政策风险。"),
                ],
            },
            {
                "name": "机器人/智能制造",
                "keywords": ["机器人", "智能制造", "减速器", "伺服", "工控"],
                "risk": "产业落地节奏不稳定，订单和价格竞争需要持续验证。",
                "leaders": [
                    ("汇川技术", "300124.SZ", "工控和伺服龙头。"),
                    ("埃斯顿", "002747.SZ", "工业机器人整机代表。"),
                    ("绿的谐波", "688017.SH", "谐波减速器核心零部件公司。"),
                ],
            },
            {
                "name": "红利/公用事业",
                "keywords": ["红利", "股息", "电力", "公用事业", "煤炭", "水电"],
                "risk": "利率上行或分红不及预期会压制估值。",
                "leaders": [
                    ("长江电力", "600900.SH", "水电红利核心资产。"),
                    ("中国神华", "601088.SH", "煤炭高股息代表。"),
                    ("华能水电", "600025.SH", "清洁电力代表。"),
                ],
            },
        ],
    },
    "hk": {
        "code": "hk",
        "name": "港股",
        "summary": "港股重点看低估值修复、南向资金、高股息和互联网平台盈利韧性。",
        "sources": [
            "https://www.hkexnews.hk/",
            "https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities?sc_lang=en",
            "https://www.aastocks.com/",
            "https://www.sfc.hk/en/",
            "https://finance.yahoo.com/markets/stocks/articles/hong-kong-share-sales-hit-020257101.html",
        ],
        "directions": [
            {
                "name": "互联网平台",
                "keywords": ["internet", "AI", "platform", "e-commerce", "互联网", "平台"],
                "risk": "监管、竞争和广告消费修复弱于预期。",
                "leaders": [
                    ("腾讯控股", "0700.HK", "社交、游戏和金融科技平台龙头。"),
                    ("阿里巴巴-W", "9988.HK", "电商和云计算平台龙头。"),
                    ("美团-W", "3690.HK", "本地生活平台龙头。"),
                ],
            },
            {
                "name": "高股息央国企",
                "keywords": ["dividend", "yield", "buyback", "股息", "分红", "回购"],
                "risk": "盈利周期下行或分红政策变化会削弱防守属性。",
                "leaders": [
                    ("中国移动", "0941.HK", "电信高股息核心标的。"),
                    ("中国海洋石油", "0883.HK", "能源高股息代表。"),
                    ("汇丰控股", "0005.HK", "金融高股息代表，受利率周期影响大。"),
                ],
            },
            {
                "name": "创新药",
                "keywords": ["biotech", "pharma", "drug", "创新药", "医药"],
                "risk": "临床失败、融资压力和商业化不及预期。",
                "leaders": [
                    ("百济神州", "6160.HK", "全球化创新药龙头。"),
                    ("信达生物", "1801.HK", "生物药和创新药代表。"),
                    ("康方生物", "9926.HK", "双抗创新药代表。"),
                ],
            },
            {
                "name": "AI 与半导体",
                "keywords": ["AI", "semiconductor", "chip", "半导体", "芯片"],
                "risk": "估值弹性大，业绩兑现和外部限制会影响波动。",
                "leaders": [
                    ("中芯国际", "0981.HK", "晶圆制造核心公司。"),
                    ("华虹半导体", "1347.HK", "特色工艺晶圆代工代表。"),
                    ("ASMPT", "0522.HK", "半导体封装设备代表。"),
                ],
            },
            {
                "name": "消费与出行修复",
                "keywords": ["consumer", "travel", "retail", "消费", "出行", "旅游"],
                "risk": "消费复苏慢、价格竞争和利润率承压。",
                "leaders": [
                    ("携程集团-S", "9961.HK", "在线旅游平台龙头。"),
                    ("安踏体育", "2020.HK", "运动消费龙头。"),
                    ("华润啤酒", "0291.HK", "啤酒消费代表。"),
                ],
            },
        ],
    },
    "us": {
        "code": "us",
        "name": "美股",
        "summary": "美股重点看 AI 资本开支、利率路径、盈利质量和指数集中度风险。",
        "sources": [
            "https://www.sec.gov/news/pressreleases",
            "https://www.nasdaq.com/market-activity/stocks",
            "https://fred.stlouisfed.org/",
            "https://finance.yahoo.com/",
            "https://finance.yahoo.com/technology/",
            "https://finance.yahoo.com/topic/semiconductors/",
            "https://finance.yahoo.com/technology/ai/articles/optical-transceiver-market-set-double-104800250.html",
            "https://www.idtechex.com/en/research-report/co-packaged-optics-cpo/1138",
            "https://futurumgroup.com/insights/coherent-q3-fy-2026-ai-data-center-demand-accelerates-optical-growth/",
            "https://www.micron.com/about/newsroom",
            "https://www.businessinsider.com/ai-stocks-investing-ideas-bubble-valuations-ben-snider-goldman-sachs-2026-7",
            "https://finance.yahoo.com/energy/articles/best-nuclear-ai-energy-stocks-120000687.html",
            "https://www.ishares.com/us/insights/portfolio-insights/thematic-investing-2026-outlook",
            "https://themesetfs.com/insights/6-blockbuster-investment-themes-to-watch-in-2026",
        ],
        "directions": [
            {
                "name": "AI 存储/HBM",
                "keywords": ["memory", "storage", "HBM", "DRAM", "NAND", "SSD", "Micron", "SanDisk", "Western Digital", "Seagate"],
                "risk": "存储是强周期行业，价格和供需反转会造成业绩与估值双杀。",
                "leaders": [
                    ("Micron Technology", "MU", "美国存储龙头，关注 HBM、DRAM/NAND 价格和 AI 服务器需求。"),
                    ("SanDisk", "SNDK", "NAND/SSD 代表，关注企业级存储需求和价格周期。"),
                    ("Western Digital", "WDC", "数据中心硬盘与存储代表，关注云厂商资本开支。"),
                ],
            },
            {
                "name": "CPO/光通信",
                "keywords": ["CPO", "co-packaged optics", "optical", "transceiver", "silicon photonics", "photonics", "Coherent", "Lumentum", "Marvell"],
                "risk": "CPO 产业化节奏仍有不确定性，短期交易可能提前透支远期预期。",
                "leaders": [
                    ("Coherent", "COHR", "光通信与光器件代表，关注 AI 数据中心光互联需求。"),
                    ("Lumentum", "LITE", "光器件和激光器代表，关注 CPO/NPO 产业化节奏。"),
                    ("Marvell Technology", "MRVL", "AI 数据中心互联芯片代表，关注定制芯片和光互联产品。"),
                ],
            },
            {
                "name": "AI 基础设施",
                "keywords": ["AI", "semiconductor", "GPU", "accelerator", "data center", "cloud", "networking"],
                "risk": "资本开支放缓或估值过高会导致明显回撤。",
                "leaders": [
                    ("NVIDIA", "NVDA", "GPU 和 AI 加速计算龙头。"),
                    ("Broadcom", "AVGO", "AI 网络和定制芯片代表。"),
                    ("Microsoft", "MSFT", "云计算和 AI 应用平台龙头。"),
                ],
            },
            {
                "name": "大型科技平台",
                "keywords": ["earnings", "cloud", "platform", "software", "AI"],
                "risk": "指数集中度高，监管和估值压缩风险突出。",
                "leaders": [
                    ("Apple", "AAPL", "消费电子和生态平台龙头。"),
                    ("Microsoft", "MSFT", "企业软件和云平台龙头。"),
                    ("Alphabet", "GOOGL", "搜索、广告和 AI 模型平台。"),
                ],
            },
            {
                "name": "医疗健康",
                "keywords": ["healthcare", "biotech", "pharma", "drug", "FDA"],
                "risk": "政策控费、临床失败和专利悬崖。",
                "leaders": [
                    ("Eli Lilly", "LLY", "减重药和糖尿病药物龙头。"),
                    ("UnitedHealth", "UNH", "管理式医疗龙头。"),
                    ("Johnson & Johnson", "JNJ", "综合医疗健康代表。"),
                ],
            },
            {
                "name": "金融与利率交易",
                "keywords": ["Fed", "rate", "yield", "bank", "inflation"],
                "risk": "利率路径判断错误和信用风险上升。",
                "leaders": [
                    ("JPMorgan Chase", "JPM", "美国大型银行龙头。"),
                    ("Berkshire Hathaway", "BRK.B", "保险和多元资产控股代表。"),
                    ("Goldman Sachs", "GS", "投行和资本市场代表。"),
                ],
            },
            {
                "name": "宽基 ETF",
                "keywords": ["ETF", "S&P 500", "Nasdaq", "index", "fund"],
                "risk": "指数高集中度导致回撤时分散效果变弱。",
                "leaders": [
                    ("Vanguard S&P 500 ETF", "VOO", "低费率标普 500 ETF。"),
                    ("iShares Core S&P 500 ETF", "IVV", "标普 500 核心配置 ETF。"),
                    ("Invesco QQQ Trust", "QQQ", "纳斯达克 100 科技成长 ETF。"),
                ],
            },
        ],
    },
}

HORIZON_WEIGHTS = {
    "day": {"freshness": 3, "position": 2},
    "week": {"freshness": 2, "position": 2},
    "month": {"freshness": 1, "position": 3},
}
