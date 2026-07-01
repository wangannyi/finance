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
            "https://www.cls.cn/detail/2411836",
            "https://www.sfccn.com/2026/6-12/xMMDE1MjBfMjE1OTAxMQ.html",
            "https://finance.sina.com.cn/wm/2026-06-11/doc-iniazpqr3992135.shtml",
            "https://www.stcn.com/article/detail/3957156.html",
            "https://www.cls.cn/detail/2370529",
            "https://www.cls.cn/detail/2397515",
            "https://finance.eastmoney.com/a/202606083763780253.html",
            "https://www.stcn.com/article/detail/3802973.html",
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

MARKET_CONFIGS["ch"]["horizon_directions"] = {
    "month": MARKET_CONFIGS["ch"]["directions"],
    "week": [
        {
            "name": "CPO/光模块",
            "keywords": ["CPO", "光模块", "硅光", "光通信", "800G", "1.6T"],
            "risk": "产业链景气较高，需防范订单兑现不及预期和估值透支。",
            "leaders": [
                ("中际旭创", "300308.SZ", "海外 AI 光模块龙头。"),
                ("新易盛", "300502.SZ", "高速光模块代表。"),
                ("天孚通信", "300394.SZ", "光器件平台型公司。"),
            ],
        },
        {
            "name": "PCB/AI服务器链",
            "keywords": ["PCB", "AI服务器", "服务器", "高速板", "HDI", "玻璃基板"],
            "risk": "订单、产能和价格需要持续跟踪，短期涨幅大后波动会放大。",
            "leaders": [
                ("沪电股份", "002463.SZ", "AI 服务器 PCB 代表。"),
                ("胜宏科技", "300476.SZ", "高端 PCB 和算力链弹性标的。"),
                ("生益科技", "600183.SH", "覆铜板和材料代表。"),
            ],
        },
        {
            "name": "存储芯片",
            "keywords": ["存储芯片", "HBM", "DRAM", "NAND", "存储"],
            "risk": "存储价格周期反转会快速影响盈利预期。",
            "leaders": [
                ("兆易创新", "603986.SH", "存储芯片设计代表。"),
                ("澜起科技", "688008.SH", "内存接口芯片龙头。"),
                ("江波龙", "301308.SZ", "存储模组和品牌存储代表。"),
            ],
        },
        {
            "name": "电子特气/六氟化钨",
            "keywords": ["电子特气", "特种气体", "六氟化钨", "WF6", "三氟化氮", "刻蚀气"],
            "risk": "价格和国产替代预期已被快速交易，需核验订单和高位波动风险。",
            "leaders": [],
        },
        {
            "name": "光刻胶/湿电子化学品",
            "keywords": ["光刻胶", "KrF", "ArF", "湿电子化学品", "显影液", "清洗剂", "剥离液"],
            "risk": "客户验证和量产节奏不确定，短线题材波动可能很大。",
            "leaders": [],
        },
        {
            "name": "刻蚀材料/设备",
            "keywords": ["刻蚀", "刻蚀设备", "刻蚀材料", "蚀刻液", "介质刻蚀", "等离子刻蚀"],
            "risk": "设备和材料验证周期长，需防范涨幅提前透支。",
            "leaders": [],
        },
        {
            "name": "氟化工/含氟电子材料",
            "keywords": ["氟化工", "含氟材料", "含氟电子材料", "含氟电子特气", "电子化学品", "氟碳", "氟聚合物", "PTFE", "六氟丁二烯", "高端氟材料"],
            "risk": "受商品周期、环保供给和下游半导体需求共同影响。",
            "leaders": [],
        },
        {
            "name": "半导体设备/材料",
            "keywords": ["半导体设备", "设备", "材料", "电子特气", "刻蚀", "CMP"],
            "risk": "设备验证周期长，订单和国产替代节奏可能低于预期。",
            "leaders": [
                ("北方华创", "002371.SZ", "半导体设备平台型龙头。"),
                ("中微公司", "688012.SH", "刻蚀设备代表。"),
                ("华海清科", "688120.SH", "CMP 设备代表。"),
            ],
        },
        {
            "name": "创新药BD/出海",
            "keywords": ["创新药", "BD", "license-out", "出海", "授权", "临床"],
            "risk": "临床和授权进展不确定，消息驱动下波动较大。",
            "leaders": [
                ("恒瑞医药", "600276.SH", "创新药平台型龙头。"),
                ("百济神州-U", "688235.SH", "全球化创新药代表。"),
                ("药明康德", "603259.SH", "CXO 和出海服务代表。"),
            ],
        },
    ],
    "day": [
        {
            "name": "CPO商业化/光模块资金",
            "keywords": ["CPO", "商业化", "光模块", "资金流入", "主力资金"],
            "risk": "日内交易受资金情绪影响大，追高回撤风险高。",
            "leaders": [
                ("中际旭创", "300308.SZ", "关注光模块资金强度。"),
                ("新易盛", "300502.SZ", "关注高速光模块成交和换手。"),
                ("天孚通信", "300394.SZ", "关注光器件链弹性。"),
            ],
        },
        {
            "name": "模拟/功率半导体涨价",
            "keywords": ["模拟芯片", "功率半导体", "涨价", "MLCC", "被动元件"],
            "risk": "涨价题材持续性弱于供需验证时容易快速降温。",
            "leaders": [
                ("圣邦股份", "300661.SZ", "模拟芯片代表。"),
                ("扬杰科技", "300373.SZ", "功率器件代表。"),
                ("三环集团", "300408.SZ", "MLCC 和电子陶瓷代表。"),
            ],
        },
        {
            "name": "存储芯片资金流入",
            "keywords": ["存储芯片", "存储", "资金流入", "DRAM", "NAND"],
            "risk": "资金驱动题材可能快速轮动，需结合成交和公告验证。",
            "leaders": [
                ("兆易创新", "603986.SH", "存储芯片设计代表。"),
                ("澜起科技", "688008.SH", "内存接口芯片龙头。"),
                ("江波龙", "301308.SZ", "存储模组代表。"),
            ],
        },
        {
            "name": "电子特气/六氟化钨",
            "keywords": ["电子特气", "特种气体", "六氟化钨", "WF6", "三氟化氮", "刻蚀气", "涨价"],
            "risk": "涨价和订单传闻容易造成日内高波动，需核验公告和产能。",
            "leaders": [],
        },
        {
            "name": "光刻胶/湿电子化学品",
            "keywords": ["光刻胶", "KrF", "ArF", "湿电子化学品", "显影液", "清洗剂", "剥离液", "涨停"],
            "risk": "验证周期长，短线催化和真实业绩之间可能存在落差。",
            "leaders": [],
        },
        {
            "name": "刻蚀材料/设备",
            "keywords": ["刻蚀", "刻蚀设备", "刻蚀材料", "蚀刻液", "介质刻蚀", "等离子刻蚀", "涨停"],
            "risk": "题材弹性大，设备订单和材料认证需要持续验证。",
            "leaders": [],
        },
        {
            "name": "氟化工/含氟电子材料",
            "keywords": ["氟化工", "含氟材料", "含氟电子材料", "含氟电子特气", "电子化学品", "氟碳", "氟聚合物", "PTFE", "六氟丁二烯", "高端氟材料"],
            "risk": "化工周期和半导体材料逻辑交织，需区分价格弹性与长期壁垒。",
            "leaders": [],
        },
        {
            "name": "PCB涨价/玻璃基板",
            "keywords": ["PCB", "涨价", "玻璃基板", "覆铜板", "AI服务器"],
            "risk": "短线催化依赖涨价扩散和订单确认，波动较大。",
            "leaders": [
                ("沪电股份", "002463.SZ", "AI 服务器 PCB 核心标的。"),
                ("胜宏科技", "300476.SZ", "高端 PCB 弹性标的。"),
                ("生益科技", "600183.SH", "覆铜板材料代表。"),
            ],
        },
        {
            "name": "机器人降价/新品催化",
            "keywords": ["机器人", "人形机器人", "降价", "新品", "灵巧手"],
            "risk": "产品发布和降价容易形成短期交易，业绩兑现仍早。",
            "leaders": [
                ("汇川技术", "300124.SZ", "工控和伺服龙头。"),
                ("绿的谐波", "688017.SH", "谐波减速器代表。"),
                ("埃斯顿", "002747.SZ", "工业机器人整机代表。"),
            ],
        },
    ],
}

MARKET_CONFIGS["hk"]["horizon_directions"] = {
    "month": MARKET_CONFIGS["hk"]["directions"],
    "week": [
        {
            "name": "AI融资/新股链",
            "keywords": ["AI boom", "artificial intelligence", "fundraising", "IPO", "share sales", "融资"],
            "risk": "新股热度受市场情绪影响大，上市后波动可能较高。",
            "leaders": [
                ("阿里巴巴-W", "9988.HK", "港股 AI 和云计算代表。"),
                ("腾讯控股", "0700.HK", "AI 应用和平台生态龙头。"),
                ("商汤-W", "0020.HK", "AI 软件和模型应用代表。"),
            ],
        },
        {
            "name": "中资券商/港交所",
            "keywords": ["share sales", "equity capital markets", "IPO", "成交", "融资"],
            "risk": "成交和 IPO 周期波动明显，受风险偏好影响大。",
            "leaders": [
                ("香港交易所", "0388.HK", "港股融资和交易活跃度核心标的。"),
                ("中信证券", "6030.HK", "中资券商龙头。"),
                ("华泰证券", "6886.HK", "财富管理和投行业务代表。"),
            ],
        },
        {
            "name": "高股息电信能源",
            "keywords": ["dividend", "yield", "buyback", "股息", "分红", "能源"],
            "risk": "防守资产也会受商品价格、利率和盈利变化影响。",
            "leaders": [
                ("中国移动", "0941.HK", "电信高股息核心标的。"),
                ("中国海洋石油", "0883.HK", "能源高股息代表。"),
                ("中国神华", "1088.HK", "煤炭高股息代表。"),
            ],
        },
        {
            "name": "创新药授权出海",
            "keywords": ["biotech", "pharma", "license-out", "BD", "临床", "创新药"],
            "risk": "临床和授权节点不确定，单日波动可能较大。",
            "leaders": [
                ("百济神州", "6160.HK", "全球化创新药龙头。"),
                ("信达生物", "1801.HK", "生物药和创新药代表。"),
                ("康方生物", "9926.HK", "双抗创新药代表。"),
            ],
        },
        {
            "name": "AI硬件/半导体映射",
            "keywords": ["AI", "semiconductor", "chip", "半导体", "芯片", "硬件"],
            "risk": "港股映射标的弹性和流动性差异大。",
            "leaders": [
                ("中芯国际", "0981.HK", "晶圆制造核心公司。"),
                ("华虹半导体", "1347.HK", "特色工艺晶圆代工代表。"),
                ("ASMPT", "0522.HK", "封装设备代表。"),
            ],
        },
    ],
    "day": [
        {
            "name": "AI新股/融资情绪",
            "keywords": ["AI boom", "fundraising", "share sales", "IPO", "人工智能"],
            "risk": "短线受新闻和资金情绪驱动，不宜替代基本面判断。",
            "leaders": [
                ("香港交易所", "0388.HK", "融资活跃度直接受益标的。"),
                ("阿里巴巴-W", "9988.HK", "AI 云和平台代表。"),
                ("商汤-W", "0020.HK", "AI 主题弹性标的。"),
            ],
        },
        {
            "name": "南向高股息买盘",
            "keywords": ["南向资金", "股息", "回购", "dividend", "yield"],
            "risk": "短线买盘变化和除息安排会影响价格表现。",
            "leaders": [
                ("中国移动", "0941.HK", "南向高股息核心。"),
                ("中国海洋石油", "0883.HK", "能源高股息代表。"),
                ("汇丰控股", "0005.HK", "金融高股息代表。"),
            ],
        },
        {
            "name": "创新药临床/BD催化",
            "keywords": ["临床", "BD", "license-out", "创新药", "biotech"],
            "risk": "事件驱动波动大，需核验公告质量。",
            "leaders": [
                ("康方生物", "9926.HK", "双抗和 BD 催化代表。"),
                ("信达生物", "1801.HK", "创新药商业化代表。"),
                ("百济神州", "6160.HK", "全球化创新药龙头。"),
            ],
        },
        {
            "name": "互联网回购/业绩催化",
            "keywords": ["buyback", "earnings", "platform", "回购", "业绩"],
            "risk": "回购和业绩催化若低于预期，估值修复会受阻。",
            "leaders": [
                ("腾讯控股", "0700.HK", "回购和平台盈利韧性代表。"),
                ("阿里巴巴-W", "9988.HK", "电商和云平台龙头。"),
                ("美团-W", "3690.HK", "本地生活平台龙头。"),
            ],
        },
        {
            "name": "港股半导体弹性",
            "keywords": ["semiconductor", "chip", "半导体", "芯片", "AI"],
            "risk": "消息驱动和流动性会放大日内波动。",
            "leaders": [
                ("中芯国际", "0981.HK", "晶圆制造核心公司。"),
                ("华虹半导体", "1347.HK", "特色工艺晶圆代工代表。"),
                ("ASMPT", "0522.HK", "封装设备代表。"),
            ],
        },
    ],
}

MARKET_CONFIGS["us"]["horizon_directions"] = {
    "month": [
        MARKET_CONFIGS["us"]["directions"][2],
        MARKET_CONFIGS["us"]["directions"][0],
        MARKET_CONFIGS["us"]["directions"][1],
        MARKET_CONFIGS["us"]["directions"][3],
        MARKET_CONFIGS["us"]["directions"][5],
    ],
    "week": [
        {
            "name": "AI存储/HBM价格链",
            "keywords": ["HBM", "DRAM", "NAND", "memory", "Micron", "SanDisk", "Western Digital"],
            "risk": "存储价格和订单变化会带来较强周期波动。",
            "leaders": [
                ("Micron Technology", "MU", "HBM 和 DRAM/NAND 周期核心。"),
                ("SanDisk", "SNDK", "NAND/SSD 弹性标的。"),
                ("Western Digital", "WDC", "数据中心存储代表。"),
            ],
        },
        {
            "name": "CPO/硅光光互联",
            "keywords": ["CPO", "co-packaged optics", "silicon photonics", "optical transceiver", "Coherent", "Lumentum"],
            "risk": "产业化进度和订单兑现仍需持续验证。",
            "leaders": [
                ("Coherent", "COHR", "AI 数据中心光器件代表。"),
                ("Lumentum", "LITE", "光器件和激光器代表。"),
                ("Marvell Technology", "MRVL", "AI 互联芯片代表。"),
            ],
        },
        {
            "name": "AI电力/核能链",
            "keywords": ["AI power", "nuclear", "grid", "utilities", "energy infrastructure", "data center power"],
            "risk": "项目周期、政策和利率会影响估值。",
            "leaders": [
                ("GE Vernova", "GEV", "电网和电力设备代表。"),
                ("Constellation Energy", "CEG", "核电和数据中心电力代表。"),
                ("Vistra", "VST", "电力和容量市场代表。"),
            ],
        },
        {
            "name": "国防航天/SpaceX映射",
            "keywords": ["defense", "aerospace", "space", "SpaceX", "satellite", "military"],
            "risk": "预算和项目节点不确定，估值容易受消息扰动。",
            "leaders": [
                ("Palantir", "PLTR", "国防和商业 AI 软件代表。"),
                ("Rocket Lab", "RKLB", "商业航天弹性标的。"),
                ("Lockheed Martin", "LMT", "传统国防龙头。"),
            ],
        },
        {
            "name": "稳定币/代币化金融",
            "keywords": ["stablecoin", "tokenization", "digital assets", "blockchain", "crypto"],
            "risk": "监管和加密资产波动会显著影响交易热度。",
            "leaders": [
                ("Coinbase", "COIN", "加密交易和基础设施代表。"),
                ("Robinhood", "HOOD", "零售交易和加密业务代表。"),
                ("Circle", "CRCL", "稳定币相关代表。"),
            ],
        },
    ],
    "day": [
        {
            "name": "MU/HBM财报与涨价",
            "keywords": ["Micron", "MU", "HBM", "DRAM", "price", "memory"],
            "risk": "财报和价格预期交易波动极高。",
            "leaders": [
                ("Micron Technology", "MU", "HBM 和 DRAM/NAND 核心标的。"),
                ("SanDisk", "SNDK", "NAND 弹性标的。"),
                ("Western Digital", "WDC", "存储周期弹性代表。"),
            ],
        },
        {
            "name": "COHR/LITE光通信订单",
            "keywords": ["Coherent", "Lumentum", "CPO", "optical transceiver", "silicon photonics"],
            "risk": "订单传闻和估值变化会造成短线大幅波动。",
            "leaders": [
                ("Coherent", "COHR", "光通信订单弹性标的。"),
                ("Lumentum", "LITE", "光器件弹性标的。"),
                ("Marvell Technology", "MRVL", "AI 互联芯片代表。"),
            ],
        },
        {
            "name": "核电/电网订单催化",
            "keywords": ["nuclear", "grid", "utilities", "energy infrastructure", "AI power"],
            "risk": "政策和项目新闻驱动，兑现周期长。",
            "leaders": [
                ("GE Vernova", "GEV", "电网设备代表。"),
                ("Constellation Energy", "CEG", "核电代表。"),
                ("Vistra", "VST", "电力容量市场代表。"),
            ],
        },
        {
            "name": "国防科技消息催化",
            "keywords": ["defense", "SpaceX", "satellite", "military", "aerospace"],
            "risk": "预算和合同消息可能快速反转。",
            "leaders": [
                ("Palantir", "PLTR", "国防 AI 软件代表。"),
                ("Rocket Lab", "RKLB", "商业航天弹性标的。"),
                ("Lockheed Martin", "LMT", "传统国防龙头。"),
            ],
        },
        {
            "name": "稳定币监管/交易量",
            "keywords": ["stablecoin", "tokenization", "crypto", "digital assets", "blockchain"],
            "risk": "监管措辞和币价波动会放大日内表现。",
            "leaders": [
                ("Coinbase", "COIN", "加密资产交易平台代表。"),
                ("Robinhood", "HOOD", "零售交易和加密业务代表。"),
                ("Circle", "CRCL", "稳定币相关代表。"),
            ],
        },
    ],
}
