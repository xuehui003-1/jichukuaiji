#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《03_项目一_第1讲_开学第一课_规划文档》Word 文档。
第一课专属规划：90 分钟分钟级流程；分组两套方案对比（固定小组 / 同桌互审）；
开学点单表设计；AI 点睛「财务部来了新同事」落位。
版本号机制同规划文档：改 VERSION / DATE / REVISION_HISTORY 后重跑，旧版保留。
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ============ 每次修订只需要改这里 ============
VERSION = "v1.0"
DATE = "2026-08-31"
REVISION_HISTORY = [
    ("v1.0", "2026-08-31",
     "新建：第一节课（项目一第1讲·开学第一课）规划文档。90 分钟分钟级课堂流程；"
     "分组两套方案对比（固定小组 / 同桌互审）与推荐；开学点单表 6 题设计；"
     "AI 点睛「财务部来了新同事」落位；趣味任务卡 A1/A2。"),
]
# =============================================

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
OUT = os.path.join(ROOT, "03_项目一_第1讲_开学第一课_规划文档_{}_{}.docx".format(VERSION, DATE.replace("-", "")))

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2)
sec.top_margin = sec.bottom_margin = Cm(2)

GRAY = (89, 89, 89)
BLUE = (31, 78, 121)


def set_font(run, name="宋体", size=10.5, bold=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run._element.get_or_add_rPr()
    rfonts = run._element.rPr.get_or_add_rFonts()
    rfonts.set(qn("w:eastAsia"), name)
    if color:
        run.font.color.rgb = RGBColor(*color)


def para(text="", size=10.5, bold=False, align=None, name="宋体",
         color=None, space_after=4, space_before=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = 1.3
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    set_font(r, name=name, size=size, bold=bold, color=color)
    return p


def h1(text):
    para(text, size=15, bold=True, name="黑体", color=BLUE, space_before=12, space_after=6)


def h2(text):
    para(text, size=12, bold=True, name="黑体", color=(0, 0, 0), space_before=8, space_after=4)


def shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def make_table(headers, rows, widths_cm, font_size=9.5, header_bg="D9E2F3"):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    tblPr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    hdr = t.rows[0].cells
    for i, htxt in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(htxt)
        set_font(r, size=font_size, bold=True)
        shade_cell(hdr[i], header_bg)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(str(v))
            set_font(r, size=font_size)
    for i, w in enumerate(widths_cm):
        for row in t.rows:
            row.cells[i].width = Cm(w)
    return t


def add_footer():
    footer = sec.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p.add_run("第 ")
    set_font(r1, size=9, color=GRAY)
    run = p.add_run()
    f1 = OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"), "begin")
    it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = "PAGE"
    f2 = OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"), "end")
    run._r.append(f1); run._r.append(it); run._r.append(f2)
    set_font(run, size=9, color=GRAY)
    r2 = p.add_run(" 页 · 共 ")
    set_font(r2, size=9, color=GRAY)
    run2 = p.add_run()
    g1 = OxmlElement("w:fldChar"); g1.set(qn("w:fldCharType"), "begin")
    it2 = OxmlElement("w:instrText"); it2.set(qn("xml:space"), "preserve"); it2.text = "NUMPAGES"
    g2 = OxmlElement("w:fldChar"); g2.set(qn("w:fldCharType"), "end")
    run2._r.append(g1); run2._r.append(it2); run2._r.append(g2)
    set_font(run2, size=9, color=GRAY)
    r3 = p.add_run(" 页")
    set_font(r3, size=9, color=GRAY)


add_footer()

# ================= 标题区 =================
para("项目一　第 1 讲　开学第一课（讲课规划文档）", size=20, bold=True, name="黑体",
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4, space_before=6)
para("财务机器人应用与开发 · 第 1 周 · 90 分钟（2 课时连上）", size=12, name="黑体",
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
para("文档编号 03 ｜ 版本 {} ｜ 生成日期 {} ｜ 配套《00_财务机器人课程教学规划_v3.2》｜ 性质：讲课规划（第一课专属版）".format(VERSION, DATE),
     size=10.5, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

# ================= 0 使用说明 =================
h1("0　使用说明（这份怎么用）")
for s in [
    "① 这是开学第一课的完整规划，90 分钟课堂流程精确到分钟，照着走就行。",
    "② 第一课不碰软件：智多星下周（项目二）才安装；本课只需要投影＋一台能联网的电脑（大模型演示用）。",
    "③ 本课定位一句话：不是教多少知识，而是让学生「下周还想来」——期待感第一，知识量第二。",
    "④ 分组方案两套并排写在第二部分，点单表第 3 题收集学生偏好，课后拍板；课堂流程第 70–75 分钟两种写法都备好。",
    "⑤ 配套参考：点单表玩法沿用基础会计课 90-C2；积分规则沿用 90-C5（2 分/5 分机制）。",
]:
    para(s, size=10.5, space_after=3)

# ================= 一、定位与目标 =================
h1("一、本讲定位与目标")
make_table(
    ["维度", "目标"],
    [
        ("知识", "知道这门课学什么、RPA 和 AI 大致是什么、财务机器人在财务场景里长什么样"),
        ("技能", "会初步辨别「人写的还是 AI 写的」财务文本（本课唯一“硬”知识）"),
        ("情感（核心）", "期待感拉满——“这学期我能指挥机器人干活”；建立“AI 是同事不是威胁”的认知"),
    ],
    [2.6, 14.4], font_size=10)
para("第一课的「三不」：不讲深、不动软件、不考试。", size=10.5, bold=True, space_before=4)

# ================= 二、分组两套方案 =================
h1("二、分组方案：两套对比（课后拍板）")
para("您提到「固定分组还是同桌互审」还没定，两套方案都写好，点单表第 3 题收集学生偏好后拍板。",
     size=10.5, space_after=6)
make_table(
    ["对比维度", "方案 A：第一节课就固定分组（4 人小组）", "方案 B：同桌互审起步，大任务时临时组队"],
    [
        ("建组成本", "需要调座位、起组名、选角色，约 10 分钟", "零成本：机房同桌即搭档，1 分钟搞定"),
        ("角色感", "强：组长 / 操作 / 复核 / 记录播报固定", "中：一个做、一个审，角色随时互换"),
        ("财务专业对口", "一般", "强：制单与审核分离就是财务岗位的天然机制"),
        ("与基础会计课衔接", "要改习惯（基础会计课默认不分组）", "一脉相承（沿用 90-C12「同桌互审」）"),
        ("大任务适配", "发布会等大任务直接可用", "第 7 周起大任务前按需临时组队"),
        ("管理成本", "组长制省心，但第一节课分组易「硬凑」", "几乎为零"),
        ("一句话结论", "适合「团队战」课程", "适合「先单兵、后组队」课程"),
    ],
    [2.8, 6.6, 7.6], font_size=9.5)
para("推荐：方案 B 起步。理由：①机房同桌是天然搭档，第一节课座位都没定死，硬分组容易流于形式；"
     "②「制单—审核」分离本身就是财务岗位机制，互审比小组更专业对口；③与您基础会计课一脉相承，学生零适应成本。"
     "需要团队大任务时（如第 16 周新品发布会），提前一周按任务组队即可。",
     size=10.5, bold=True, space_before=6)
para("两套方案在课堂流程第 70–75 分钟都有对应写法，选哪套照哪套走。", size=10, color=GRAY)

# ================= 三、课前准备 =================
h1("三、课前准备")
for s in [
    "教师：大模型账号登录投影备用；预录屏兜底（「AI 员工生成过程」30 秒，防无网）；点单表打印 60 份；"
    "积分规则一页 PPT；开场视频（财务机器人干活快放）。",
    "学生：无特殊准备（第一课空手来）。",
    "机房：只检查投影与音响；智多星本周不装。",
]:
    para(s, size=10.5, space_after=3)

# ================= 四、课堂流程 =================
h1("四、课堂流程（90 分钟 · 分钟级）")
make_table(
    ["时间", "环节", "教师做什么", "学生做什么", "设计意图"],
    [
        ("0–8", "悬念开场", "放「财务机器人干活」快放视频；三问：①这学期谁陪你上课？②机器人会取代会计吗？③你最想让机器人帮你干什么？",
         "看视频；举手 / 便利贴回答", "用悬念立期待，让问题先悬着"),
        ("8–20", "课程全景", "一张图讲「RPA 是手、AI 是脑」；学什么（六项目＋项目七）、怎么玩（2 分/5 分、彩蛋库、作品化）、怎么考核（过程 60%＋期末 40%）",
         "听讲＋提问", "消除未知感，规则透明"),
        ("20–30", "开学点单表", "发表，讲清「你写什么，这学期课上就出现什么」；当堂填、当堂交",
         "填表", "收集兴趣＋分组偏好＋AI 员工名字形象"),
        ("30–42", "生活中的 AI 与 AI 发展", "学生版讲解：手机里的 AI（刷脸/语音/推荐）→ 生成式 AI → 智能体；插 1–2 个短视频",
         "互动：说出一个你今天用过的 AI", "从熟悉出发建立好奇"),
        ("42–45", "暂停点 1", "问：AI 会不会比会计先学会做账？先写猜测再公布思路",
         "记录单写猜测", "预测效应：先猜后讲记得牢"),
        ("45–60", "AI 点睛「财务部来了新同事」", "当堂输入提示词，演示生成 AI 员工自我介绍；不满意现场改；全班起名投票建档（一学期沿用）",
         "起名＋投票", "亲手「招」第一位数字同事"),
        ("60–70", "RPA 初印象", "财务共享中心智能场景机器人视频；RPA 在商科的应用（报销/开票/对账）",
         "找共同点：它们都在「替人干活」", "RPA 与 AI 两条线在此会师"),
        ("70–75", "建立学习搭档 / 分组", "方案 A：4 人固定小组起组名选角色；方案 B：确定同桌搭档＋互审规则",
         "执行对应方案", "为后续协作定队形"),
        ("75–85", "辨别赛「人写的还是 AI 写的」", "4 段财务文本（邮件/报表说明/公告），搭档或小组抢答＋说理由，答对 2 分",
         "抢答", "本课唯一「硬」知识：AI 文本可辨别"),
        ("85–90", "收尾", "三句话总结；下节课预告（装智多星、带 U 盘）；课后任务",
         "记任务", "制造下周期待"),
    ],
    [1.4, 2.7, 5.3, 4.2, 3.4], font_size=9)
para("时间合计：8+12+10+12+3+15+10+5+10+5 = 90 分钟。", size=10, bold=True, space_before=4)

# ================= 五、知识点详解 =================
h1("五、知识点详解（学生版）")
for t in [
    ("知识点 1　AI 发展的三个阶段（通俗版）",
     "认字的 AI（识别）：刷脸、语音、OCR 识别发票——只能「看」，不能「想」。",
     "写字的 AI（生成）：写报告、做图、写文案——能「创作」，但不会自己干活。",
     "干活的 AI（智能体）：自己规划步骤、调用工具去执行——本课程项目七的主角。",
     "每一阶段都配一个财务例子，让学生明白「AI 离会计很近」。" ),
    ("知识点 2　RPA 是什么：「RPA 是手，AI 是脑」",
     "RPA＝只会照流程干活的「手」：不思考、不犯错、不知疲倦，流程怎么写就怎么干。",
     "AI＝会理解、会判断的「脑」：看得懂发票、判得了异常。",
     "手＋脑＝数字员工；学生在课程里的角色＝指挥者。"),
    ("知识点 3　财务共享中心智能场景机器人",
     "报销机器人：收单 → 审核 → 付款；开票机器人：订单 → 开票 → 发送；对账机器人：银行流水 → 逐笔核对。",
     "每个场景一句话讲完，配合视频画面。"),
    ("认知误区（常见坑）",
     "误区 1「机器人会取代会计」→ 取代的是重复劳动，会计升级为指挥者和复核者。",
     "误区 2「AI 说的都对」→ 第一课就立复核观：AI 可能一本正经地胡说，复核是财务人的底线。"),
]:
    para(t[0], size=11, bold=True, space_before=6, space_after=2)
    for line in t[1:]:
        para(line, size=10.5, space_after=2)

# ================= 六、趣味任务卡 =================
h1("六、趣味任务卡（第一课用）")
make_table(
    ["任务卡", "规则", "提示 / 彩蛋"],
    [
        ("A1 给 AI 员工起名建档\n难度★",
         "全班提名 → 投票定名＋形象；名字要求「见名知意」（和变量命名一脉相承：一眼知道它干什么）；提议被采纳者得 5 分",
         "提示：先立命名标准再提名，防止跑偏。\n彩蛋：名字和形象上「数字员工墙」，一学期沿用"),
        ("A2 人写的还是 AI 写的\n难度★★",
         "4 段财务文本（邮件 / 报表说明 / 公告）抢答辨别＋说理由；答对 2 分",
         "提示：看数字细节、看客套话密度。\n彩蛋：全对者获「火眼金睛」称号"),
    ],
    [3.2, 8.0, 5.8], font_size=9.5)

# ================= 七、点单表设计 =================
h1("七、开学点单表设计（6 题 · 当堂填当堂交）")
make_table(
    ["题号", "题目", "用途"],
    [
        ("1", "给我们的 AI 员工起个名字（要求见名知意）", "定 AI 员工档案（名字）"),
        ("2", "它的形象风格：可爱 / 酷 / 科技感", "定 AI 员工档案（生成头像用）"),
        ("3", "你希望怎么合作：同桌搭档 / 固定小组 / 无所谓", "决定分组方案 A 还是 B"),
        ("4", "你最想让机器人帮你干的财务活（打钩：报销 / 开票 / 对账 / 查账 / 其他）", "课程案例选题"),
        ("5", "你用过哪些 AI（刷脸 / 语音助手 / 写文案…）", "摸底，调整讲法深浅"),
        ("6", "愿不愿意被画进教学漫画 / 彩蛋（署名 / 匿名 / 不出现）", "彩蛋授权（沿用基础会计课做法）"),
    ],
    [1.0, 8.0, 8.0], font_size=9.5)
para("当场收齐，课后统计（统计方法参照基础会计课 90_通用工具的点单表做法），第二节课前定案并贴出「数字员工墙」。",
     size=10.5, space_before=4)

# ================= 八、课后任务 =================
h1("八、课后任务")
para("必做：用 30 秒给爸妈讲「这学期我要学什么」（口头即可；下节课抽 3 人复述，＋2 分）。", size=10.5, space_after=2)
para("选做：找一条 AI 新闻下周分享（1 条＋2 分）。", size=10.5, space_after=2)

# ================= 九、教学备忘 =================
h1("九、教学备忘（易错点与应急）")
for s in [
    "大模型无网 / 卡顿：用预录屏兜底；若两样都失效 → 跳过演示，宣布「下周我们亲手把这位同事请进来」，流程向后顺延。",
    "时间超支：辨别赛可压到 2 题；「课程全景」的考核说明可移至下节课。",
    "纪律：第一节课就公开并试用 2 分/5 分机制，当堂给分，立好规矩。",
    "视频素材：优先用官方 / 自制素材，避免版权问题。",
]:
    para(s, size=10.5, space_after=3)

# ================= 十、修订记录 =================
h1("十、修订记录")
make_table(
    ["版本", "日期", "修订内容"],
    REVISION_HISTORY,
    [1.8, 2.6, 12.6], font_size=9.5)

doc.save(OUT)
print("已生成:", OUT)
