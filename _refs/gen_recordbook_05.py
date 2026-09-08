# -*- coding: utf-8 -*-
"""05 学生实验记录册（全程）生成器 v2.4
页码/编号/标题全部自动从课件 SLIDES 提取（04/08/10），课件改页重跑即同步。
结构＝暂停点格＋填写表＋老师布置的任务＋一行自查，其余不写。
用法: python3 _refs/gen_recordbook_05.py   (在仓库根运行)
"""
import io, re, os, json, subprocess
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RPA = os.path.join(ROOT, "RPA")
REFS = os.path.join(ROOT, "_refs")
F04 = "04_项目一_第1讲_开学第一课_课件_v2.1_20260906.html"
F08 = "08_项目二_第1-3讲_变量命令流程_纸上篇_课件_v1.2_20260906.html"
F10 = "10_项目二_第4讲_机器人上岗_课件_v1.2_20260906.html"
OUT = "05_机器人实验记录册_全程_v2.4_20260908.docx"
NUM = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲"

def strip(t):
    t = re.sub(r"<br\s*/?>", " ", t)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()

def pauses(fn):
    """node 权威解析 SLIDES -> JSON，返回 {编号: (页码, 标题)}"""
    tmp = os.path.join("/tmp", "slides_%s.json" % fn[:2])
    subprocess.run(["node", os.path.join(REFS, "extract_slides.js"),
                    os.path.join(RPA, fn), tmp], check=True, capture_output=True)
    slides = json.load(io.open(tmp, encoding="utf-8"))
    out = {}
    for pg in slides:
        m = re.search(r"⏸\s*暂停点([①-⑳])(?:\s*·\s*([^<\n`]{2,16}))?", pg["html"])
        if m and m.group(1) not in out:
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", pg["html"], re.S)
            title = (m.group(2) or "").strip() or (strip(h1.group(1))[:12] if h1 else "")
            out[m.group(1)] = (pg["no"], title)
    return out

p4, p8, p10 = pauses(F04), pauses(F08), pauses(F10)
assert sorted(p4) == list("①②③④"), p4
assert sorted(p8, key=NUM.index) == list(NUM[:14]), p8
assert sorted(p10, key=NUM.index) == list(NUM[14:]), p10

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(1.6); sec.top_margin = sec.bottom_margin = Cm(1.4)
st = doc.styles["Normal"]; st.font.name = "微软雅黑"; st.font.size = Pt(10.5)
st._element.rPr.rFonts.set(qn("w:eastAsia"), "微软雅黑")

def run(p, t, size=10.5, bold=False, color=None):
    r = p.add_run(t); r.bold = bold; r.font.size = Pt(size)
    if color: r.font.color.rgb = RGBColor.from_string(color)
    return r
def P(t, size=10.5, bold=False, color=None, before=2, after=2):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(after)
    run(p, t, size, bold, color); return p
def sec_head(t):
    doc.add_page_break()
    p = P(t, 13, True, "C0390B", 0, 6)
    return p
def pause(code, src, desc):
    pg, title = {"04": p4, "08": p8, "10": p10}[src][code]
    p = P("⏸ 暂停点%s · %s　——课件 %s · p%d" % (code, title, src, pg), 11.5, True, "1A5276", 10, 2)
    if desc: P(desc, 9.5, False, "555555", 0, 3)
    return p
def grid(rows, blank_lines=1):
    """2 列表：左标签右填写区"""
    t = doc.add_table(rows=len(rows), cols=2); t.style = "Table Grid"
    t.columns[0].width = Cm(4.6); t.columns[1].width = Cm(12.6)
    for i, label in enumerate(rows):
        c0, c1 = t.rows[i].cells
        c0.width = Cm(4.6); c1.width = Cm(12.6)
        run(c0.paragraphs[0], label, 10, True)
        for _ in range(blank_lines):
            c1.add_paragraph()
def selfcheck(t):
    P("✅ 下课前自查：" + t, 9.5, False, "555555", 10, 2)

# ───────── 封面头 ─────────
P("我 的 机 器 人 实 验 记 录", 20, True, "C0390B", 0, 4)
P("《财务机器人应用与开发》　　班级：＿＿＿＿＿＿　学号：＿＿＿＿＿＿＿＿　姓名：＿＿＿＿＿＿　互审搭档：＿＿＿＿＿＿", 10.5)
P("这不是作业本，是实验记录。看到课件「⏸ 暂停点N」才动笔：先写你的想法，再听老师讲；猜错不扣分——猜错的地方，正是你今天要学的地方。", 9.5, False, "555555")

# ───────── 项目一（课件 04） ─────────
sec_head("项目一 · 开学第一课｜课件 04")
pause("①", "04", "正常流程走得好好的，什么时候会「出事」？把想到的意外都写下来（越多越好）。")
grid(["我的想法", "思考过程", "老师的讲解"])
pause("②", "04", "万一：洗到一半突然停电。来电后从哪一步继续？写下你的规矩。")
grid(["我的想法", "思考过程", "老师的讲解"])
pause("③", "04", "万一：忘了放洗衣液。机器怎么发现？怎么办？写下你的规矩。")
grid(["我的想法", "思考过程", "老师的讲解"])
pause("④", "04", "万一：洗好了一直没人拿。怎么办？写下你的规矩。")
grid(["我的想法", "思考过程", "老师的讲解"])
P("✏️ 课堂记录 · 哪句 AI 命令更好？差在哪？　——课件 04 · p22–23", 11.5, True, "1A5276", 10, 2)
P("两组命令上台对比后写：好在哪、差在哪（先写判断，再听分享）。", 9.5, False, "555555", 0, 3)
grid(["我的判断", "差在哪", "老师的讲解"])
selfcheck("□①我写出了意外　□②③④我写了规矩　□我判了哪句命令更好　　我猜错最惨的：＿＿＿＿＿＿＿＿＿＿＿＿")

# ───────── 项目二 · 纸上篇（课件 08） ─────────
sec_head("项目二 · 纸上篇（变量·命令·流程）｜课件 08")
pause("①", "08", "哪句命令更好？差在哪？先写判断再听讲（好命令三行：①想法 ②思考过程 ③听老师讲）。")
grid(["我的想法", "思考过程", "老师的讲解"])
pause("②", "08", "余额格：早上 50，妈妈转来 200，买奶茶花 30——现在格子里是多少？先写猜的数和理由，再对黑板验证。")
grid(["我的猜想（数字＋理由）", "验证之后", "老师的讲解"])
pause("③", "08", "给三个数起见名知义的英文名。行规：首字母小写、第二个词首字母大写。写完同桌互审，不合格打回重起。")
grid(["饭卡余额 → 我的命名", "每月话费 → 我的命名", "班费 → 我的命名"])
pause("④", "08", "把①–⑫号货填进五类，每类再写一个你自己的新例子。分对 8 个以上过关。")
P("十二个货：①饭卡余额35.5 ②今天气温26℃ ③隆兴寺预约号A08-15 ④地铁票价2元 ⑤骑手位置 ⑥借书到期日2026-10-01 ⑦取件码A8-2012 ⑧到站时间14:30 ⑨学生证照片studentID.jpg ⑩「运输中」 ⑪大锅菜6元 ⑫微信步数18326", 9, False, "555555", 0, 3)
grid(["数值（能加减乘除）", "字符（文字不能算）", "日期", "时间", "文件（存在哪）"])
pause("⑤", "08", "取件码 \"A8-2012\" 能当数算吗？写下判断＋理由。今天不揭晓——进机房让机器人跑给你看，把答案抄回来。")
grid(["我的判断（能算／报错）", "我的理由", "进机房后的答案"])
pause("⑥", "08", "「37 号同学，你的麻辣烫好了」——拆成三要素。")
grid(["动作（让屏幕干什么）", "参数（给了什么要求）", "输出（大家看到什么）"])
pause("⑦", "08", "「弹出提示」的三要素。")
grid(["弹什么", "什么时候弹", "弹给谁"])
pause("⑧", "08", "把「打印讲义」补成师傅一句都不用问的完整命令；再揪出 4 条说明里说反的卧底。")
grid(["我的完整命令", "卧底是＿条", "我的理由"])
pause("⑨", "08", "三种串法各配一个你自己生活里的例子。")
grid(["顺序 · 我的例子", "条件 · 我的例子", "循环 · 我的例子"])
pause("⑩", "08", "给班委的正定行程单挑刺：最要命的缺参数是哪处？补上它。")
grid(["缺的命令", "会出的乱子", "我的补法"])
pause("⑪", "08", "三句话抄下来，每句配一个你自己的例子，同桌判。")
grid(["三句话抄下来", "我的例子", "同桌判"])
pause("⑫", "08", "任务A「外卖满减计算器」图纸（全班必做）：照右边三行画全，讲给同桌听、他点头才开工。")
grid(["第 1 行 变量：建哪几个格＋类型", "第 2 行 命令：用哪几条", "第 3 行 串法：先算→再判→最后弹什么", "同桌点头：签名＿＿＿＿＿＿"])
P("✏️ 加时图纸 · 任务B「班费记账」（做完 A 再画）　——课件 08 · p50", 11.5, True, "1A5276", 10, 2)
grid(["第 1 行 变量", "第 2 行 命令", "第 3 行 串法（含「如果…就…」）"])
pause("⑬", "08", "全班找错·三张带病图纸：把最狠的一个病＋改法写下来。")
grid(["最狠的病（哪张图、哪行）", "改法"])
pause("⑭", "08", "同桌互验·三个数考他的图纸：你念数、他口头跑，记下各弹多少，然后互换。")
grid(["恰好 25 元 → 弹多少", "便宜到 10 元 → 弹多少", "0 份 → 弹多少", "翻车的数＋卡在哪行（帮他圈出来）"])
P("📋 老师布置的任务（课件 08）", 12, True, "C0390B", 12, 3)
P("必做①（p44）：找 3 件「按固定步骤做事」的事，每件写成「先…再…最后…」。", 10)
grid(["我的三件事（一件一行）"], blank_lines=3)
P("必做②（p57）：给图纸加一条新规矩——满 100 再减 5。", 10)
grid(["我加的规矩"])
P("选做（p44）：用「如果…就…否则…」给家里定一条家规。", 10)
grid(["我的家规"])
P("选做（p57）：把图纸讲给家人，让他找出顺序、条件、循环各在哪。", 10)
grid(["家人找出的一处"])
P("🗓 大任务（p57，一周内交，+5 分）：当一回家里的「小会计」——挑家里最近一笔大开销（买菜/话费/网购），照外卖计算器画一张「满减或比价」三行图纸，讲给家人听、让他挑一个刺写在图纸旁。", 10)
grid(["我挑的开销", "家人挑的刺", "完成日期"])
selfcheck("□①–⑤判断猜想都写了　□⑥–⑧三要素拆全　□⑨–⑪例子配了　□⑫图纸三行全　□⑬⑭找错互验各写一行　　今天最值钱的错：＿＿＿＿＿＿＿＿")

# ───────── 项目二 · 机器人上岗（课件 10） ─────────
sec_head("项目二 · 机器人上岗｜课件 10")
pause("⑮", "10", "《打招呼》里机器人依次干了哪几件事？按顺序一件一行。")
grid(["①", "②", "③"])
pause("⑯", "10", "先猜后验：放 50→输出，再放 200→输出——屏幕先后打出什么？先写猜想再点运行。")
grid(["我的猜想", "验证之后", "老师的讲解"])
pause("⑰", "10", "读报错：把机器人说的原话一字不改抄下来，圈出读懂的词。")
grid(["机器人原话", "我读懂的词", "它想要的"])
pause("⑱", "10", "排错三行：把刚才翻车那次写下来（以后每次报错都写）。")
grid(["我在干什么", "机器人说了啥", "我改了什么·结果"])
pause("⑲", "10", "结业三句，各配一个今天真机上的例子。")
grid(["会记（变量）·例子", "会派（命令）·例子", "会修（调试）·例子"])
P("📋 老师布置的任务（课件 10）", 12, True, "C0390B", 12, 3)
P("必做（p21）：把「生活费」建出来——建变量、放 1500、算出剩 900。", 10)
grid(["我算出的剩余"])
P("选做（p21）：把今天的报错截图带过来，开「报错博物馆」。", 10)
grid(["我带来的报错词"])
P("🏁 项目二大任务（p21，一周内交，+5 分）：把你家一周生活费做成记账图纸——建变量放 1500，每花一笔「生活费＝生活费−这一笔」，低于 100 弹「该省省了」；下次进机房跑给机器人算。", 10)
grid(["我定的最低线", "跑出来的结果", "完成日期"])
selfcheck("□⑮按顺序写全　□⑯先猜后验　□⑰抄了报错原话　□⑱排错三行　□⑲三句配了例子　　我最怕的报错词：＿＿＿＿＿＿＿＿＿＿")

doc.save(os.path.join(RPA, OUT))
print("生成", OUT)
print("04:", {k: v[0] for k, v in sorted(p4.items(), key=lambda x: NUM.index(x[0]))})
print("08:", {k: v[0] for k, v in sorted(p8.items(), key=lambda x: NUM.index(x[0]))})
print("10:", {k: v[0] for k, v in sorted(p10.items(), key=lambda x: NUM.index(x[0]))})
