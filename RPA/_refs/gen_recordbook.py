# -*- coding: utf-8 -*-
"""
生成《05_项目一_第1讲_开学第一课_学生记录册》Word 文档。
v1.3 暂停点制改版（配套 04_课件 v1.6）：全册 1 页，无分页符、无页眉；
只收录暂停点——凡是学生需要填写的地方都是暂停点，每处三行：
  ① 我的想法（先写自己的）→ ② 思考过程 → ③ 老师的讲解（写错了就在这里补记）；
  暂停点① 意外头脑风暴；暂停点②③④ 洗衣机出事了（停电/忘洗衣液/没人拿）；
  暂停点⑤ 哪句 AI 命令更好；
换机器、当指挥等环节用草稿纸＋举纸，不进记录册（少而精，每人打印 1 页）。
版本号机制同规划文档：改 VERSION / DATE / REVISION_HISTORY 后重跑，旧版自动删除（只保留最新版）。
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

# ============ 每次修订只需要改这里 ============
VERSION = "v1.3"
DATE = "2026-09-04"
REVISION_HISTORY = [
    ("v1.3", "2026-09-04",
     "暂停点制改版：①全册 1 页、无分页符、无页眉，删除「记录X·第N页」等文字；"
     "②只收录暂停点（凡学生填写处即暂停点）：①意外头脑风暴 ②③④洗衣机出事了（停电/忘洗衣液/没人拿）"
     "⑤哪句AI命令更好；每处三行——①我的想法→②思考过程→③老师的讲解；"
     "③换机器、当指挥等环节改用草稿纸＋举纸，不进记录册，每人只打印 1 页。"),
    ("v1.2", "2026-09-04",
     "精简至 6 页，只记暂停点与老师检查点；填写区 1–2 行＋老师的答案区；当指挥页改任务单填空。"),
    ("v1.1", "2026-09-04",
     "标签一一对应版：页面按课堂顺序重排，页眉标「记录①–⑩」，填写项双区。"),
    ("v1.0", "2026-09-04",
     "新建，配套 04_课件 v1.3（学生视角版）。"),
]

# ============ 颜色 ============
ORANGE_DARK = (194, 90, 31)
BLUE = (59, 110, 165)
GREEN = (107, 158, 107)
GRAY = (89, 89, 89)
BLACK = (0, 0, 0)

# ============ 输出 ============
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
OUT = os.path.join(ROOT, "05_项目一_第1讲_开学第一课_学生记录册_{}_{}.docx".format(VERSION, DATE.replace("-", "")))

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(1.8)
sec.top_margin = sec.bottom_margin = Cm(1.5)


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
         color=None, space_after=2, space_before=0, line=1.25):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = line
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    set_font(r, name=name, size=size, bold=bold, color=color)
    return p


def blank(n=48, lines=1, space_after=2, line=1.45):
    """手写横线：全角下划线（打印后为连续横线）。"""
    for _ in range(lines):
        para("＿" * n, size=10.5, color=GRAY, space_after=space_after, line=line)


def pause_head(text):
    """暂停点标题行（橙色加粗）。"""
    para("⏸ " + text, size=11.5, bold=True, name="黑体", color=ORANGE_DARK,
         space_before=6, space_after=1)


def three_lines(labels, lines):
    """三行制：①想法 ②思考过程 ③老师的讲解。labels 为三个标签文本，lines 为各横线行数。"""
    for lab, n in zip(labels, lines):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.2
        r = p.add_run(lab)
        set_font(r, size=10.5, bold=True, name="黑体", color=BLACK)
        blank(48, lines=n, space_after=1, line=1.4)


def card_line(title, normal, wan):
    """意外卡一行式：正常/万一固定内容压成一行。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.2
    r = p.add_run(title)
    set_font(r, size=10.5, bold=True, name="黑体", color=BLACK)
    r2 = p.add_run("（正常：" + normal + "；万一：" + wan + "）")
    set_font(r2, size=10, name="宋体", color=GRAY)


def add_footer():
    footer = sec.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("05_ 学生记录册 {} · {} ｜ 只有暂停点才动笔：①想法→②思考过程→③老师的讲解".format(VERSION, DATE))
    set_font(r, size=8.5, color=GRAY)


add_footer()

# ================= 页首（封面信息三行） =================
para("《财务机器人应用与开发》我的机器人实验记录 · 第 1 讲", size=14, bold=True, name="黑体",
     align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
para("班级：＿＿＿＿＿＿　　学号：＿＿＿＿＿＿＿＿　　姓名：＿＿＿＿＿＿　　互审搭档：＿＿＿＿＿＿",
     size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para("用法：看到课件「📒暂停点N」才动笔，每处三行——①先写你的想法 → ②写思考过程 → ③听老师讲，写错了就在③补记",
     size=9, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)

# ================= 暂停点① =================
pause_head("暂停点①　什么时候会「出事」？")
para("正常流程：放衣服→放洗衣液→关舱门→选模式→按启动→进水→洗涤→漂洗→脱水→蜂鸣结束。哪一步会出问题？",
     size=9.5, color=GRAY, space_after=1)
three_lines(["① 我的想法——意外清单（越多越好）", "② 思考过程——它卡住了正常流程的哪一步", "③ 老师的讲解——归类＋全班圈出的「最要命的三个」"],
            [3, 1, 2])

# ================= 暂停点②③④ 洗衣机出事了 =================
pause_head("暂停点②③④　洗衣机出事了 · 写规矩（写完举册子）")
card_line("② 停电", "进水→洗涤→漂洗→脱水", "洗到一半突然停电")
three_lines(["① 我的想法——来电后从哪一步继续？", "② 思考过程——为什么从这里继续？", "③ 老师的讲解"],
            [1, 1, 1])
card_line("③ 忘洗衣液", "放洗衣液→进水洗涤", "忘了放洗衣液")
three_lines(["① 我的想法——机器怎么发现？怎么办？", "② 思考过程——追问：想清水洗？洗到一半才想起？", "③ 老师的讲解"],
            [1, 1, 1])
card_line("④ 没人拿", "洗完→蜂鸣提醒→取衣", "一直没人来拿")
three_lines(["① 我的想法——怎么办？", "② 思考过程——追问：提醒几次？衣服皱了？超时？", "③ 老师的讲解"],
            [1, 1, 1])

# ================= 暂停点⑤ =================
pause_head("暂停点⑤　哪句 AI 命令更好？差在哪？")
three_lines(["① 我的想法——哪句更好", "② 思考过程——差在哪（理由）", "③ 老师的讲解——把话说清楚的要点"],
            [1, 2, 2])


def prune(prefix):
    """只保留最新版：删除同前缀、同扩展名的旧文件。"""
    for f in os.listdir(ROOT):
        if f.startswith(prefix) and f.endswith(".docx") and f != os.path.basename(OUT):
            os.remove(os.path.join(ROOT, f))


prune("05_项目一_第1讲_开学第一课_学生记录册_")
doc.save(OUT)
print("已生成:", OUT)
