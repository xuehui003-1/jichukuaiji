# -*- coding: utf-8 -*-
"""12_项目二_课件教师答案对照手册 生成器 v1.3
从两份课件 SLIDES 数组自动提取逐页内容（页码零手抄，课件改一页手册跟着变）。
用法: python3 _refs/gen_manual_12.py   (在仓库根运行)
"""
import io, re, os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RPA = os.path.join(ROOT, "RPA")
F08 = "08_项目二_第1-3讲_变量命令流程_纸上篇_课件_v1.2_20260906.html"
F10 = "10_项目二_第4讲_机器人上岗_课件_v1.2_20260906.html"
OUT = "12_项目二_课件教师答案对照手册_v1.3_20260908.docx"

def strip(t):
    t = re.sub(r"<br\s*/?>", " ", t)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip()

def parse(fn):
    s = io.open(os.path.join(RPA, fn), encoding="utf-8").read()
    a = s.find("const SLIDES"); b = s.find("\n];", a)
    chunks = s[a:b].split("{cls:")[1:]
    pages = []
    for i, c in enumerate(chunks, 1):
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", c, re.S)
        eyebrow = re.search(r'class="eyebrow"[^>]*>(.*?)</div>', c, re.S)
        pill = re.search(r'border-radius:999px[^>]*>(.*?)</div>', c, re.S)
        badges = [x.strip() for x in re.findall(r'type:"(?:note|question)", text:"([^"]+)"', c)]
        stu = [strip(x) for x in re.findall(r'class="stu"[^>]*>(.*?)</span>', c)]
        now = [strip(x) for x in re.findall(r"现在你：([^<`\\n]+)", c)]
        where = re.search(r'class="where"[^>]*>(.*?)</div>', c, re.S)
        rvs = [strip(x) for x in re.findall(r'<div class="rv"><div class="anscard">(.*?)</div></div>', c)]
        notes = re.search(r'notes:"((?:[^"\\]|\\.)*)"', c)
        pages.append(dict(no=i,
            pill=strip(pill.group(1)) if pill else "",
            eyebrow=strip(eyebrow.group(1)) if eyebrow else "",
            h1=strip(h1.group(1)) if h1 else "",
            badges=badges, stu=stu, now=now,
            where=strip(where.group(1)) if where else "", rvs=rvs,
            notes=strip(notes.group(1)) if notes else ""))
    return pages

p8 = parse(F08); p10 = parse(F10)
assert len(p8) == 57 and len(p10) == 21, (len(p8), len(p10))

# 暂停点总表：(编号, 课件, 页, 学生写什么/验收要点) —— 页码必须与课件一致，课件改动后核对
PAUSE = [
 ("①","08",6,"记录册第1页最后一行：好命令三行——①想法 ②思考过程 ③听老师讲"),
 ("②","08",12,"先写猜想再对照揭晓（余额 50 → 250）"),
 ("③","08",14,"给 3 个真实数据各起一个见名知义的英文名"),
 ("④","08",17,"十二个货各归五类（常量/文本/整数/小数/布尔），答案下一页揭晓"),
 ("⑤","08",21,"写判断（能算/报错）＋理由——结论进机房上机揭晓"),
 ("⑥","08",30,"拆「37号同学，你的麻辣烫好了」：动作/参数/输出"),
 ("⑦","08",32,"弹出提示三要素：弹什么/什么时候弹/弹给谁"),
 ("⑧","08",35,"补两条命令＋揪出卧底（丙）"),
 ("⑨","08",38,"三种串法（顺序/条件/循环）各配一个生活例子"),
 ("⑩","08",41,"给行程单挑刺——补上缺掉的集合时间"),
 ("⑪","08",43,"三句话各配一个自己的例子"),
 ("⑫","08",51,"图纸三行：变量清单/命令清单/串法（参考答案见该页点击揭晓）"),
 ("⑬","08",53,"全班找错：抢答三张带病图纸的病＋改法；最狠的一个＋改法一行写进记录册"),
 ("⑭","08",54,"同桌互验验收单：换三个刁钻输入互考（恰好25→21；10→原价10；0→弹应付0）"),
 ("⑮","10",6,"打招呼三件事：你好 → 我是小邮 → 今天上岗"),
 ("⑯","10",9,"先猜屏幕输出再对照揭晓（先打 50 再打 200，只留最新）"),
 ("⑰","10",16,"读报错三处：第几行/什么类型/它想要什么"),
 ("⑱","10",18,"排错三行：我在干什么/机器人说了啥/我改了什么结果怎样"),
 ("⑲","10",20,"三句话各配今天的真机例子"),
]

doc = Document()
sec = doc.sections[0]
sec.orientation = WD_ORIENT.LANDSCAPE
sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
sec.left_margin = sec.right_margin = Cm(1.2); sec.top_margin = sec.bottom_margin = Cm(1.2)
st = doc.styles["Normal"]; st.font.name = "微软雅黑"; st.font.size = Pt(9)
st._element.rPr.rFonts.set(qn("w:eastAsia"), "微软雅黑")

def H(txt, size=14, color="C0390B", before=6):
    p = doc.add_paragraph(); r = p.add_run(txt)
    r.bold = True; r.font.size = Pt(size); r.font.color.rgb = RGBColor.from_string(color)
    p.paragraph_format.space_before = Pt(before)
def T(txt, size=9, bold=False):
    p = doc.add_paragraph(); r = p.add_run(txt); r.bold = bold; r.font.size = Pt(size)
    return p

H("项目二 · 课件教师答案对照手册", 16)
T("v1.3 ｜ 2026-09-08 ｜ 会计学院 · 大数据与会计 2501 班", 10, True)
T("对应课件：08《项目二·纸上篇（变量·命令·流程）》v1.2（57 页）＋ 10《机器人上岗》v1.2（21 页）。", 9)
T("本手册由课件源文件自动提取生成（_refs/gen_manual_12.py）：页码与课件逐一对应，课件改一页、重跑脚本手册跟着变。课件里带底色的答案块默认隐藏，放映时点击才揭晓——手册「点击揭晓答案」列即其完整文本，供课前备课与课后验收。", 9)

H("一、暂停点总表（全册统一编号 ①–⑲）", 13)
T("课件每个动笔处都标「⏸ 暂停点X · 标题」，右上角徽章同步提示记录册落点；开场抽查一律写明抽哪个暂停点。下表页码即课件页码。", 9)
tb = doc.add_table(rows=1, cols=4); tb.style = "Table Grid"
for j, w in enumerate((1.4, 1.6, 5.2, 18.5)):
    tb.columns[j].width = Cm(w)
hdr = tb.rows[0].cells
for j, h in enumerate(("编号", "课件", "页", "暂停点 · 学生写什么（验收要点）")):
    hdr[j].text = ""; r = hdr[j].paragraphs[0].add_run(h); r.bold = True
for code, src, pg, pt_ in PAUSE:
    info = (p8 if src == "08" else p10)[pg-1]
    title = info["eyebrow"].replace("⏸ 暂停点", "").split("·", 1)[-1].strip() if "暂停点" in info["eyebrow"] else info["h1"]
    c = tb.add_row().cells
    c[0].text = code; c[1].text = src; c[2].text = str(pg)
    c[3].text = "%s ｜ %s" % (title, pt_)

def page_table(sec_title, pages, note=""):
    H(sec_title, 12)
    if note: T(note, 8)
    t = doc.add_table(rows=1, cols=5); t.style = "Table Grid"
    for j, w in enumerate((0.9, 4.6, 6.6, 8.0, 6.6)):
        t.columns[j].width = Cm(w)
    hdr = t.rows[0].cells
    for j, h in enumerate(("页", "页眉/徽章", "页面标题", "学生干什么", "点击揭晓答案 ｜ 教师提示")):
        hdr[j].text = ""; r = hdr[j].paragraphs[0].add_run(h); r.bold = True
    for pg in pages:
        c = t.add_row().cells
        c[0].text = str(pg["no"])
        c[1].text = " / ".join([x for x in (pg["pill"], pg["eyebrow"]) if x] + pg["badges"])
        c[2].text = pg["h1"]
        stu = "；".join(pg["stu"])
        now = "；".join("现在你：" + x for x in pg["now"])
        c[3].text = " ｜ ".join([x for x in (stu, now, pg["where"]) if x])
        rv = " ◆ ".join(pg["rvs"])
        c[4].text = ("答案：" + rv + "\n") if rv else ""
        if pg["notes"]: c[4].text += "提示：" + pg["notes"]

page_table("二、08《纸上篇》第 1 章 变量——储物格（第 1–22 页）", p8[:22])
page_table("三、08《纸上篇》第 2 章 命令（第 23–39 页）", p8[22:39])
page_table("四、08《纸上篇》第 3 章 流程与调试（第 40–57 页）", p8[39:])
page_table("五、10《机器人上岗》（全 21 页）", p10, "暂停点接续编号 ⑮–⑲。")
T("—— 全册完 ——", 9).alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.save(os.path.join(RPA, OUT))
print("生成", OUT, "| 08×%d 10×%d" % (len(p8), len(p10)))
