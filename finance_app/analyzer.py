from typing import Iterable

from .config import HORIZON_WEIGHTS
from .models import EvidenceSource, HotDirection, Leader, MarketReport, utc_now_iso
from .theme_discovery import PROACTIVE_THEMES, discover_themes

THEME_COMPANY_GROUPS = {
    "ch": [
        {
            "patterns": ["CPO", "光模块", "光通信"],
            "leaders": [
                ("中际旭创", "300308.SZ", "AI 光模块龙头。"),
                ("新易盛", "300502.SZ", "高速光模块代表。"),
                ("天孚通信", "300394.SZ", "光器件平台型公司。"),
                ("光迅科技", "002281.SZ", "光通信器件老牌龙头。"),
                ("亨通光电", "600487.SH", "光通信和海缆平台公司。"),
            ],
            "challengers": [
                ("太辰光", "300570.SZ", "高速光器件弹性标的。"),
                ("德科立", "688205.SH", "光收发模块和光器件新锐。"),
                ("源杰科技", "688498.SH", "高速激光器芯片代表。"),
                ("仕佳光子", "688313.SH", "光芯片和无源器件代表。"),
                ("联特科技", "301205.SZ", "光模块弹性标的。"),
            ],
        },
        {
            "patterns": ["PCB", "服务器", "玻璃基板", "覆铜板"],
            "leaders": [
                ("沪电股份", "002463.SZ", "AI 服务器 PCB 核心标的。"),
                ("深南电路", "002916.SZ", "高端 PCB 龙头。"),
                ("生益科技", "600183.SH", "覆铜板材料代表。"),
                ("鹏鼎控股", "002938.SZ", "消费电子和服务器 PCB 龙头。"),
                ("景旺电子", "603228.SH", "PCB 综合厂商。"),
            ],
            "challengers": [
                ("胜宏科技", "300476.SZ", "高端 PCB 和算力链弹性标的。"),
                ("世运电路", "603920.SH", "PCB 弹性标的。"),
                ("崇达技术", "002815.SZ", "小批量 PCB 代表。"),
                ("方正科技", "600601.SH", "PCB 修复弹性标的。"),
                ("金安国纪", "002636.SZ", "覆铜板弹性标的。"),
                ("奥士康", "002913.SZ", "服务器和汽车 PCB 弹性标的。"),
                ("依顿电子", "603328.SH", "PCB 制造修复弹性标的。"),
            ],
        },
        {
            "patterns": ["存储", "HBM", "DRAM", "NAND"],
            "leaders": [
                ("兆易创新", "603986.SH", "存储芯片设计代表。"),
                ("澜起科技", "688008.SH", "内存接口芯片龙头。"),
                ("北京君正", "300223.SZ", "车规和存储芯片代表。"),
                ("深科技", "000021.SZ", "存储封测和模组代表。"),
                ("佰维存储", "688525.SH", "存储模组和封测代表。"),
            ],
            "challengers": [
                ("江波龙", "301308.SZ", "存储模组代表。"),
                ("普冉股份", "688766.SH", "非易失性存储芯片代表。"),
                ("东芯股份", "688110.SH", "NAND/DRAM 设计代表。"),
                ("德明利", "001309.SZ", "存储控制和模组弹性标的。"),
                ("香农芯创", "300475.SZ", "存储分销和产业链弹性标的。"),
                ("聚辰股份", "688123.SH", "EEPROM 和存储芯片代表。"),
                ("恒烁股份", "688416.SH", "Nor Flash 和 MCU 弹性标的。"),
            ],
        },
        {
            "patterns": ["模拟", "功率", "MLCC", "被动元件", "涨价"],
            "leaders": [
                ("圣邦股份", "300661.SZ", "模拟芯片代表。"),
                ("思瑞浦", "688536.SH", "模拟芯片平台公司。"),
                ("纳芯微", "688052.SH", "车规和工业模拟芯片代表。"),
                ("扬杰科技", "300373.SZ", "功率器件代表。"),
                ("斯达半导", "603290.SH", "IGBT 功率半导体代表。"),
            ],
            "challengers": [
                ("三环集团", "300408.SZ", "MLCC 和电子陶瓷代表。"),
                ("风华高科", "000636.SZ", "被动元件代表。"),
                ("宏微科技", "688711.SH", "功率模块弹性标的。"),
                ("东微半导", "688261.SH", "功率器件新锐。"),
                ("洁美科技", "002859.SZ", "电子元件材料代表。"),
                ("艾为电子", "688798.SH", "模拟和信号链芯片弹性标的。"),
                ("芯朋微", "688508.SH", "电源管理芯片代表。"),
            ],
        },
        {
            "patterns": ["机器人", "灵巧手", "减速器", "伺服"],
            "leaders": [
                ("汇川技术", "300124.SZ", "工控和伺服龙头。"),
                ("绿的谐波", "688017.SH", "谐波减速器代表。"),
                ("埃斯顿", "002747.SZ", "工业机器人整机代表。"),
                ("拓普集团", "601689.SH", "机器人执行器和汽车零部件代表。"),
                ("鸣志电器", "603728.SH", "控制电机和执行器代表。"),
            ],
            "challengers": [
                ("中大力德", "002896.SZ", "减速器和传动部件弹性标的。"),
                ("五洲新春", "603667.SH", "轴承和机器人零部件代表。"),
                ("柯力传感", "603662.SH", "力传感器代表。"),
                ("江苏雷利", "300660.SZ", "微电机和执行器代表。"),
                ("步科股份", "688160.SH", "运动控制代表。"),
            ],
        },
        {
            "patterns": ["固态电池", "电池材料", "硫化物"],
            "leaders": [
                ("宁德时代", "300750.SZ", "动力电池龙头。"),
                ("比亚迪", "002594.SZ", "电池和整车平台龙头。"),
                ("赣锋锂业", "002460.SZ", "锂资源和固态电池布局代表。"),
                ("天齐锂业", "002466.SZ", "锂资源龙头。"),
                ("恩捷股份", "002812.SZ", "隔膜材料代表。"),
            ],
            "challengers": [
                ("上海洗霸", "603200.SH", "固态电池材料弹性标的。"),
                ("翔丰华", "300890.SZ", "负极材料代表。"),
                ("金龙羽", "002882.SZ", "固态电池题材弹性标的。"),
                ("当升科技", "300073.SZ", "正极材料代表。"),
                ("容百科技", "688005.SH", "高镍正极材料代表。"),
            ],
        },
        {
            "patterns": ["商业航天", "低空经济", "eVTOL", "无人机", "卫星"],
            "leaders": [
                ("中航沈飞", "600760.SH", "航空装备龙头。"),
                ("航发动力", "600893.SH", "航空发动机龙头。"),
                ("中无人机", "688297.SH", "无人机整机代表。"),
                ("航天电子", "600879.SH", "航天电子配套代表。"),
                ("航天彩虹", "002389.SZ", "无人机和航天材料代表。"),
            ],
            "challengers": [
                ("万丰奥威", "002085.SZ", "低空经济弹性标的。"),
                ("宗申动力", "001696.SZ", "低空动力系统代表。"),
                ("卧龙电驱", "600580.SH", "eVTOL 电驱代表。"),
                ("莱斯信息", "688631.SH", "低空空管信息化代表。"),
                ("纵横股份", "688070.SH", "工业无人机代表。"),
            ],
        },
        {
            "patterns": ["创新药", "CXO", "BD", "license-out", "临床"],
            "leaders": [
                ("恒瑞医药", "600276.SH", "创新药平台型龙头。"),
                ("百济神州-U", "688235.SH", "全球化创新药代表。"),
                ("药明康德", "603259.SH", "CXO 和出海服务代表。"),
                ("复星医药", "600196.SH", "综合医药平台代表。"),
                ("迈瑞医疗", "300760.SZ", "医疗器械龙头。"),
            ],
            "challengers": [
                ("信立泰", "002294.SZ", "创新药转型代表。"),
                ("泽璟制药-U", "688266.SH", "创新药小市值弹性标的。"),
                ("迪哲医药-U", "688192.SH", "肿瘤创新药代表。"),
                ("康弘药业", "002773.SZ", "眼科和创新药代表。"),
                ("科伦药业", "002422.SZ", "创新药和 ADC 合作代表。"),
            ],
        },
        {
            "patterns": ["半导体设备", "设备", "材料", "电子特气", "刻蚀", "CMP"],
            "leaders": [
                ("北方华创", "002371.SZ", "半导体设备平台型龙头。"),
                ("中微公司", "688012.SH", "刻蚀设备代表。"),
                ("华海清科", "688120.SH", "CMP 设备代表。"),
                ("沪硅产业", "688126.SH", "半导体硅片代表。"),
                ("雅克科技", "002409.SZ", "电子材料和前驱体代表。"),
            ],
            "challengers": [
                ("拓荆科技", "688072.SH", "薄膜沉积设备新贵。"),
                ("芯源微", "688037.SH", "涂胶显影设备代表。"),
                ("盛美上海", "688082.SH", "清洗设备代表。"),
                ("安集科技", "688019.SH", "CMP 材料代表。"),
                ("金宏气体", "688106.SH", "电子特气代表。"),
            ],
        },
        {
            "patterns": ["红利", "股息", "公用事业", "水电", "煤炭"],
            "leaders": [
                ("长江电力", "600900.SH", "水电红利核心资产。"),
                ("中国神华", "601088.SH", "煤炭高股息代表。"),
                ("中国石油", "601857.SH", "能源高股息代表。"),
                ("工商银行", "601398.SH", "银行高股息代表。"),
                ("中国移动", "600941.SH", "电信高股息代表。"),
            ],
            "challengers": [
                ("华能水电", "600025.SH", "清洁电力红利代表。"),
                ("陕西煤业", "601225.SH", "煤炭高分红代表。"),
                ("中国海油", "600938.SH", "油气高股息代表。"),
                ("中国广核", "003816.SZ", "核电红利代表。"),
                ("中国核电", "601985.SH", "核电运营代表。"),
                ("交通银行", "601328.SH", "银行高股息代表。"),
                ("大秦铁路", "601006.SH", "铁路红利代表。"),
            ],
        },
    ],
    "hk": [
        {
            "patterns": ["互联网", "平台", "回购", "业绩"],
            "leaders": [
                ("腾讯控股", "0700.HK", "互联网平台和 AI 应用龙头。"),
                ("阿里巴巴-W", "9988.HK", "电商、云和 AI 平台龙头。"),
                ("美团-W", "3690.HK", "本地生活平台龙头。"),
                ("京东集团-SW", "9618.HK", "电商和供应链平台代表。"),
                ("网易-S", "9999.HK", "游戏和内容平台代表。"),
            ],
            "challengers": [
                ("快手-W", "1024.HK", "短视频和直播电商平台代表。"),
                ("哔哩哔哩-W", "9626.HK", "年轻用户内容社区代表。"),
                ("携程集团-S", "9961.HK", "在线旅游平台龙头。"),
                ("小米集团-W", "1810.HK", "AI 终端和硬件生态代表。"),
                ("金山云", "3896.HK", "云计算弹性标的。"),
            ],
        },
        {
            "patterns": ["AI融资", "AI新股", "新股", "融资", "IPO"],
            "leaders": [
                ("香港交易所", "0388.HK", "港股融资和交易活跃度核心标的。"),
                ("阿里巴巴-W", "9988.HK", "港股 AI 和云计算代表。"),
                ("腾讯控股", "0700.HK", "AI 应用和平台生态龙头。"),
                ("商汤-W", "0020.HK", "AI 软件和模型应用弹性标的。"),
                ("小米集团-W", "1810.HK", "AI 终端和硬件生态代表。"),
            ],
            "challengers": [
                ("第四范式", "6682.HK", "企业 AI 软件代表。"),
                ("地平线机器人-W", "9660.HK", "智能驾驶芯片和机器人新贵。"),
                ("速腾聚创", "2498.HK", "激光雷达和机器人感知代表。"),
                ("美图公司", "1357.HK", "AI 应用弹性标的。"),
                ("金山云", "3896.HK", "AI 云基础设施代表。"),
            ],
        },
        {
            "patterns": ["半导体", "芯片", "硬件", "存储"],
            "leaders": [
                ("中芯国际", "0981.HK", "晶圆制造核心公司。"),
                ("华虹半导体", "1347.HK", "特色工艺晶圆代工代表。"),
                ("ASMPT", "0522.HK", "封装设备代表。"),
                ("上海复旦", "1385.HK", "芯片设计代表。"),
                ("晶门半导体", "2878.HK", "显示芯片代表。"),
            ],
            "challengers": [
                ("贝克微", "2149.HK", "模拟 IC 设计新股。"),
                ("宏光半导体", "6908.HK", "第三代半导体弹性标的。"),
                ("中电华大科技", "0085.HK", "安全芯片代表。"),
                ("小米集团-W", "1810.HK", "AI 终端和硬件生态代表。"),
                ("联想集团", "0992.HK", "AI PC 和服务器硬件代表。"),
            ],
        },
        {
            "patterns": ["高股息", "股息", "南向", "央国企", "电信", "能源"],
            "leaders": [
                ("中国移动", "0941.HK", "港股高股息核心标的。"),
                ("中国海洋石油", "0883.HK", "能源高股息代表。"),
                ("汇丰控股", "0005.HK", "金融高股息代表。"),
                ("中国神华", "1088.HK", "煤炭高股息代表。"),
                ("中国电信", "0728.HK", "电信高股息代表。"),
            ],
            "challengers": [
                ("中信股份", "0267.HK", "央企综合平台代表。"),
                ("中国石油股份", "0857.HK", "油气高股息代表。"),
                ("中国财险", "2328.HK", "保险高股息代表。"),
                ("华润电力", "0836.HK", "电力运营代表。"),
                ("中广核电力", "1816.HK", "核电运营代表。"),
            ],
        },
        {
            "patterns": ["创新药", "BD", "临床", "license-out", "biotech", "pharma"],
            "leaders": [
                ("百济神州", "6160.HK", "全球化创新药龙头。"),
                ("信达生物", "1801.HK", "创新药商业化代表。"),
                ("康方生物", "9926.HK", "双抗和 BD 催化代表。"),
                ("药明生物", "2269.HK", "生物药 CDMO 龙头。"),
                ("石药集团", "1093.HK", "创新药和仿制药平台代表。"),
            ],
            "challengers": [
                ("科伦博泰生物-B", "6990.HK", "ADC 和创新药新贵。"),
                ("和黄医药", "0013.HK", "肿瘤创新药代表。"),
                ("再鼎医药", "9688.HK", "License-in 创新药代表。"),
                ("荣昌生物", "9995.HK", "ADC 和自身免疫药物代表。"),
                ("君实生物", "1877.HK", "肿瘤免疫治疗代表。"),
            ],
        },
        {
            "patterns": ["消费", "出行", "旅游", "retail", "travel"],
            "leaders": [
                ("携程集团-S", "9961.HK", "在线旅游平台龙头。"),
                ("安踏体育", "2020.HK", "运动消费龙头。"),
                ("华润啤酒", "0291.HK", "啤酒消费代表。"),
                ("海底捞", "6862.HK", "餐饮消费龙头。"),
                ("李宁", "2331.HK", "运动服饰代表。"),
            ],
            "challengers": [
                ("同程旅行", "0780.HK", "在线旅游弹性标的。"),
                ("九毛九", "9922.HK", "餐饮消费弹性标的。"),
                ("奈雪的茶", "2150.HK", "新茶饮代表。"),
                ("泡泡玛特", "9992.HK", "潮玩消费代表。"),
                ("特步国际", "1368.HK", "运动消费弹性标的。"),
            ],
        },
        {
            "patterns": ["券商", "港交所", "equity capital markets", "成交"],
            "leaders": [
                ("香港交易所", "0388.HK", "港股融资和交易活跃度核心标的。"),
                ("中信证券", "6030.HK", "中资券商龙头。"),
                ("华泰证券", "6886.HK", "财富管理和投行业务代表。"),
                ("中国银河", "6881.HK", "中资券商代表。"),
                ("国泰君安", "2611.HK", "大型券商代表。"),
            ],
            "challengers": [
                ("东方证券", "3958.HK", "券商弹性标的。"),
                ("广发证券", "1776.HK", "财富管理和投行代表。"),
                ("中金公司", "3908.HK", "投行业务代表。"),
                ("申万宏源香港", "0218.HK", "港股券商弹性标的。"),
                ("招商证券", "6099.HK", "综合券商代表。"),
            ],
        },
    ],
    "us": [
        {
            "patterns": ["量子", "quantum", "IonQ", "Rigetti", "D-Wave", "QUBT"],
            "leaders": [
                ("IBM", "IBM", "量子计算平台和企业服务代表。"),
                ("Honeywell", "HON", "Quantinuum 股东方和工业科技代表。"),
                ("Alphabet", "GOOGL", "量子研究和 AI 平台代表。"),
                ("Microsoft", "MSFT", "Azure Quantum 平台代表。"),
                ("Amazon", "AMZN", "Braket 量子云平台代表。"),
            ],
            "challengers": [
                ("IonQ", "IONQ", "离子阱量子计算高弹性标的。"),
                ("Rigetti Computing", "RGTI", "超导量子计算高弹性标的。"),
                ("D-Wave Quantum", "QBTS", "量子退火商业化新贵。"),
                ("Quantum Computing", "QUBT", "量子光子芯片弹性标的。"),
                ("Arqit Quantum", "ARQQ", "量子安全加密弹性标的。"),
                ("FormFactor", "FORM", "量子芯片测试和低温探针台生态代表。"),
            ],
        },
        {
            "patterns": ["CPO", "optical", "silicon photonics", "光通信"],
            "leaders": [
                ("Coherent", "COHR", "AI 数据中心光器件代表。"),
                ("Lumentum", "LITE", "光器件和激光器弹性标的。"),
                ("Marvell Technology", "MRVL", "AI 互联芯片代表。"),
                ("Broadcom", "AVGO", "交换芯片和光互联平台代表。"),
                ("Ciena", "CIEN", "光网络设备代表。"),
            ],
            "challengers": [
                ("Applied Optoelectronics", "AAOI", "光模块弹性标的。"),
                ("Fabrinet", "FN", "光通信代工代表。"),
                ("Credo Technology", "CRDO", "高速互联芯片新贵。"),
                ("MACOM Technology", "MTSI", "射频和光通信芯片代表。"),
                ("Astera Labs", "ALAB", "AI 数据中心互联新贵。"),
            ],
        },
        {
            "patterns": ["HBM", "memory", "DRAM", "NAND", "存储"],
            "leaders": [
                ("Micron Technology", "MU", "HBM 和 DRAM/NAND 周期核心。"),
                ("Western Digital", "WDC", "数据中心存储代表。"),
                ("SanDisk", "SNDK", "NAND/SSD 弹性标的。"),
                ("Seagate", "STX", "企业级硬盘代表。"),
                ("Lam Research", "LRCX", "存储设备龙头。"),
            ],
            "challengers": [
                ("Applied Materials", "AMAT", "半导体设备平台公司。"),
                ("KLA", "KLAC", "量测检测设备龙头。"),
                ("Teradyne", "TER", "半导体测试设备代表。"),
                ("Onto Innovation", "ONTO", "先进封装量测代表。"),
                ("Entegris", "ENTG", "半导体材料代表。"),
            ],
        },
        {
            "patterns": ["nuclear", "grid", "AI power", "电力", "核能"],
            "leaders": [
                ("Constellation Energy", "CEG", "核电和 AI 电力代表。"),
                ("Vistra", "VST", "电力容量市场代表。"),
                ("GE Vernova", "GEV", "电网和电力设备代表。"),
                ("Eaton", "ETN", "电气设备和数据中心电力代表。"),
                ("NRG Energy", "NRG", "独立电力运营商代表。"),
            ],
            "challengers": [
                ("Oklo", "OKLO", "先进核能新贵。"),
                ("NuScale Power", "SMR", "小型模块化核反应堆代表。"),
                ("Bloom Energy", "BE", "数据中心电力和燃料电池代表。"),
                ("Talen Energy", "TLN", "电力和数据中心负荷代表。"),
                ("Cameco", "CCJ", "铀资源代表。"),
            ],
        },
        {
            "patterns": ["defense", "SpaceX", "satellite", "aerospace", "国防", "航天"],
            "leaders": [
                ("Lockheed Martin", "LMT", "传统国防龙头。"),
                ("Northrop Grumman", "NOC", "航空航天和防务龙头。"),
                ("RTX", "RTX", "导弹、防空和航空系统代表。"),
                ("Palantir", "PLTR", "国防和商业 AI 软件代表。"),
                ("General Dynamics", "GD", "军工平台公司。"),
            ],
            "challengers": [
                ("Rocket Lab", "RKLB", "商业航天弹性标的。"),
                ("AST SpaceMobile", "ASTS", "卫星通信新贵。"),
                ("Intuitive Machines", "LUNR", "月球商业航天代表。"),
                ("Kratos Defense", "KTOS", "无人系统和国防科技代表。"),
                ("AeroVironment", "AVAV", "无人机和巡飞弹代表。"),
            ],
        },
        {
            "patterns": ["stablecoin", "tokenization", "crypto", "digital assets", "稳定币"],
            "leaders": [
                ("Coinbase", "COIN", "加密资产交易平台代表。"),
                ("Robinhood", "HOOD", "零售交易和加密业务代表。"),
                ("Circle", "CRCL", "稳定币相关代表。"),
                ("Block", "XYZ", "支付和数字资产生态代表。"),
                ("PayPal", "PYPL", "支付和稳定币应用代表。"),
            ],
            "challengers": [
                ("MicroStrategy", "MSTR", "比特币资产负债表代表。"),
                ("MARA Holdings", "MARA", "加密挖矿代表。"),
                ("Riot Platforms", "RIOT", "比特币挖矿代表。"),
                ("Galaxy Digital", "GLXY", "数字资产金融服务代表。"),
                ("CME Group", "CME", "加密衍生品交易所代表。"),
            ],
        },
        {
            "patterns": ["Fed", "rate", "yield", "bank", "inflation", "金融", "利率"],
            "leaders": [
                ("JPMorgan Chase", "JPM", "美国大型银行龙头。"),
                ("Berkshire Hathaway", "BRK.B", "保险和多元资产控股代表。"),
                ("Goldman Sachs", "GS", "投行和资本市场代表。"),
                ("Bank of America", "BAC", "大型银行代表。"),
                ("Morgan Stanley", "MS", "财富管理和投行业务代表。"),
            ],
            "challengers": [
                ("Citigroup", "C", "全球银行修复弹性标的。"),
                ("Wells Fargo", "WFC", "零售银行代表。"),
                ("BlackRock", "BLK", "资产管理龙头。"),
                ("Charles Schwab", "SCHW", "经纪和财富管理代表。"),
                ("CME Group", "CME", "利率和衍生品交易所代表。"),
            ],
        },
        {
            "patterns": ["大型科技", "platform", "software", "cloud"],
            "leaders": [
                ("Apple", "AAPL", "消费电子和生态平台龙头。"),
                ("Microsoft", "MSFT", "企业软件和云平台龙头。"),
                ("Alphabet", "GOOGL", "搜索、广告和 AI 平台。"),
                ("Amazon", "AMZN", "云和电商平台代表。"),
                ("Meta Platforms", "META", "社交广告和 AI 应用代表。"),
            ],
            "challengers": [
                ("Oracle", "ORCL", "云基础设施和数据库代表。"),
                ("ServiceNow", "NOW", "企业软件 AI 应用代表。"),
                ("Snowflake", "SNOW", "数据云平台代表。"),
                ("Datadog", "DDOG", "云监控和可观测性代表。"),
                ("Cloudflare", "NET", "边缘网络和安全平台代表。"),
            ],
        },
        {
            "patterns": ["Physical AI", "robotics", "industrial automation", "工业自动化"],
            "leaders": [
                ("Tesla", "TSLA", "机器人和自动驾驶生态代表。"),
                ("Intuitive Surgical", "ISRG", "手术机器人龙头。"),
                ("Rockwell Automation", "ROK", "工业自动化龙头。"),
                ("Honeywell", "HON", "工业自动化平台公司。"),
                ("Eaton", "ETN", "电气自动化和电力设备代表。"),
            ],
            "challengers": [
                ("Symbotic", "SYM", "仓储机器人新贵。"),
                ("Teradyne", "TER", "协作机器人和测试设备代表。"),
                ("UiPath", "PATH", "流程自动化软件代表。"),
                ("Emerson Electric", "EMR", "工业自动化代表。"),
                ("Deere", "DE", "农业自动化代表。"),
            ],
        },
    ],
}

EXTRA_DIRECTIONS = {
    "ch": [
        {
            "name": "业绩预告/中报超预期",
            "keywords": ["中报", "业绩预告", "预增", "超预期", "利润"],
            "risk": "业绩披露期容易出现兑现和预期差波动。",
        },
        {
            "name": "资金流/成交放大",
            "keywords": ["资金流入", "主力资金", "成交额", "放量", "换手"],
            "risk": "资金驱动持续性弱，需防范快速轮动。",
        },
    ],
    "hk": [
        {
            "name": "南向资金加仓",
            "keywords": ["南向资金", "港股通", "加仓", "成交", "净买入"],
            "risk": "南向资金风格切换会影响短期表现。",
        },
        {
            "name": "回购与估值修复",
            "keywords": ["回购", "buyback", "估值修复", "低估值", "净买入"],
            "risk": "回购不等于基本面反转，需验证盈利趋势。",
        },
    ],
    "us": [
        {
            "name": "财报超预期交易",
            "keywords": ["earnings", "guidance", "beat", "revenue", "margin"],
            "risk": "财报后波动大，指引变化会快速改变估值。",
        },
        {
            "name": "ETF资金流入",
            "keywords": ["ETF", "inflows", "fund flows", "sector ETF", "volume"],
            "risk": "ETF 流入可能放大趋势，也可能快速反转。",
        },
    ],
}


def _document_text(document) -> str:
    if isinstance(document, dict):
        return f"{document.get('title', '')}\n{document.get('text', '')}"
    return str(document)


def _all_text(documents: Iterable) -> str:
    return "\n".join(_document_text(document) for document in documents).lower()


def _score_direction(direction: dict, documents: Iterable[str], horizon: str, index: int) -> int:
    text = _all_text(documents)
    keyword_hits = sum(text.count(keyword.lower()) for keyword in direction["keywords"])
    weights = HORIZON_WEIGHTS[horizon]
    base = max(0, 100 - index * 9)
    return base + keyword_hits * 12 + weights["freshness"] * 3 + weights["position"]


def _evidence(direction: dict, score: int, market_name: str) -> str:
    keywords = "、".join(direction["keywords"][:4])
    if score >= 125:
        return f"{market_name}公开信息中多次出现 {keywords} 等关键词，热度和产业关注度较高。"
    if score >= 110:
        return f"{market_name}公开信息中出现 {keywords} 等相关线索，可作为近期观察方向。"
    return f"该方向具备中期跟踪价值，但本轮抓取到的直接热度有限，需要继续验证。"


def _evidence_sources(direction: dict, documents: Iterable, limit: int = 3) -> list[EvidenceSource]:
    sources = []
    for document in documents:
        if not isinstance(document, dict):
            continue
        text = _document_text(document).lower()
        matched = [
            keyword
            for keyword in direction["keywords"]
            if keyword.lower() in text
        ]
        if matched:
            sources.append(
                EvidenceSource(
                    url=document.get("url", ""),
                    title=document.get("title", document.get("url", "")),
                    matched_keywords=matched[:6],
                    error=document.get("error"),
                )
            )
        if len(sources) >= limit:
            break
    return sources


def _directions_for_horizon(market_config: dict, horizon: str) -> list[dict]:
    directions = list(market_config.get("horizon_directions", {}).get(horizon) or market_config["directions"])
    market = market_config["code"]
    seen = {item["name"] for item in directions}
    for theme in PROACTIVE_THEMES.get(market, []):
        if theme["name"] in seen:
            continue
        directions.append(
            {
                "name": theme["name"],
                "keywords": theme["keywords"],
                "risk": theme["risk"],
                "leaders": [],
                "challengers": [],
            }
        )
        seen.add(theme["name"])
        if len(directions) >= 10:
            break
    for extra in EXTRA_DIRECTIONS.get(market, []):
        if len(directions) >= 10:
            break
        if extra["name"] in seen:
            continue
        directions.append({**extra, "leaders": [], "challengers": []})
        seen.add(extra["name"])
    return directions


def _company_group(market: str, direction: dict, group: str, exclude: set[str] | None = None) -> list[Leader]:
    configured = direction.get(group, [])
    theme_pool = _matched_company_pool(market, direction, group)
    pool = [*configured, *theme_pool]
    companies = []
    seen = set(exclude or set())
    for item in pool:
        name, ticker, detail = item
        if ticker in seen:
            continue
        companies.append(Leader(name=name, ticker=ticker, detail=detail))
        seen.add(ticker)
        if len(companies) >= 5:
            break
    return companies


def _matched_company_pool(market: str, direction: dict, group: str) -> list[tuple[str, str, str]]:
    direction_name = direction.get("name", "").lower()
    haystack = " ".join([direction.get("name", ""), *direction.get("keywords", [])]).lower()
    best = None
    best_score = 0
    for theme in THEME_COMPANY_GROUPS.get(market, []):
        score = 0
        for pattern in theme["patterns"]:
            lowered = pattern.lower()
            if lowered in direction_name:
                score += 3
            elif lowered in haystack:
                score += 1
        if score > best_score:
            best = theme
            best_score = score
    if best is None:
        return []
    return best.get(group, [])


def build_market_report(market_config: dict, documents: Iterable[str], market_code: str | None = None) -> MarketReport:
    documents = list(documents)
    market = market_code or market_config["code"]
    horizons = {}
    for horizon in ("day", "week", "month"):
        scored = []
        for index, direction in enumerate(_directions_for_horizon(market_config, horizon)):
            score = _score_direction(direction, documents, horizon, index)
            leaders = _company_group(market, direction, "leaders")
            scored.append(
                HotDirection(
                    name=direction["name"],
                    score=score,
                    evidence=_evidence(direction, score, market_config["name"]),
                    risk=direction["risk"],
                    leaders=leaders,
                    challengers=_company_group(market, direction, "challengers", {leader.ticker for leader in leaders}),
                    evidence_sources=_evidence_sources(direction, documents),
                )
            )
        horizons[horizon] = sorted(scored, key=lambda item: item.score, reverse=True)[:10]

    return MarketReport(
        market=market,
        market_name=market_config["name"],
        generated_at=utc_now_iso(),
        summary=market_config["summary"],
        sources=market_config["sources"],
        horizons=horizons,
        discovered_themes=discover_themes(market_code or market_config["code"], documents),
    )
