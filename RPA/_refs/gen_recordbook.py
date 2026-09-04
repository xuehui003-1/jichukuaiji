# -*- coding: utf-8 -*-
"""
生成《05_项目一_第1讲_开学第一课_学生记录册》Word 文档。
v1.2 精简改版（配套 04_课件 v1.5）：只记暂停点与老师检查点，全册 6 页——
  封面（姓名/搭档＋五条规矩＋评分标准＋标签暗号）
  第 2 页 记录① ⏸暂停点①（意外头脑风暴）
  第 3 页 记录②③④ 意外三卡（正常→万一→应该，各 1 行填写＋老师答案）
  第 4 页 记录⑤ 换个机器（领到机器＋流程＋意外，各 1–2 行）
  第 5 页 记录⑥ 学生当指挥·任务单（任务A乱数据填空／任务B通知填空，只填空不自由发挥）
  第 6 页 记录⑦ ⏸暂停点②（哪句命令更好）
所有填写区 1–2 行，每个填写项下方紧跟「🧑🏫 老师的答案」区，写错了当场补记。
版本号机制同规划文档：改 VERSION / DATE / REVISION_HISTORY 后重跑，旧版自动删除（只保留最新版）。
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ============ 每次修订只需要改这里 ============
VERSION = "v1.2"
DATE = "2026-09-04"
REVISION_HISTORY = [
    ("v1.2", "2026-09-04",
     "精简改版：①全册 6 页，只记暂停点与老师检查点（暂停点①/②、意外三卡、换机器、当指挥任务单），"
     "其余环节不记录，避免每讲都攒厚册子；②所有填写区压缩为 1–2 行，删除多余空行；"
     "③当指挥页改为具体任务单：任务A整理乱数据（照填空：重复只留几个/按什么排序/要几列）、"
     "任务B写班级通知（照填空：时间/地点/事情/要带什么），学生只填空不自由发挥；"
     "④页面顺序＝课堂顺序（①暂停点1=第2页 ②③④意外=第3页 ⑤换机器=第4页 ⑥任务单=第5页 ⑦暂停点2=第6页），"
     "页眉标「记录①–⑦」与课件标签一一对应。"),
    ("v1.1", "2026-09-04",
     "一一对应改版：①页面按课堂顺序重排（暂停点①＝第 1 页、意外三卡＝2–4 页、换机器＝5、未来功能＝6、"
     "AI 实验＝7、当指挥＝8、暂停点②＝第 9 页、收尾＝第 10 页）；②页眉标「记录①–⑩」与课件标签对应；"
     "③所有填写项改为「✍️我的答案」＋「🧑🏫老师的答案」双区。"),
    ("v1.0", "2026-09-04",
     "新建，配套 04_课件 v1.3（学生视角版）：封面＋8 页正文；暂停点①＝第 1 页、暂停点②＝第 2 页；"
     "意外三卡按「正常→万一→应该」模板＋同桌互查三连。"),
]

# ============ 颜色 ============
ORANGE = (233, 120, 53)
ORANGE_DARK = (194, 90, 31)
BLUE = (59, 110, 165)
GREEN = (107, 158, 107)
GRAY = (89, 89, 89)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ============ 输出 ============
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
OUT = os.path.join(ROOT, "05_项目一_第1讲_开学第一课_学生记录册_{}_{}.docx".format(VERSION, DATE.replace("-", "")))

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(2)
sec.top_margin = sec.bottom_margin = Cm(1.6)


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
         color=None, space_after=4, space_before=0, line=1.3):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = line
    if align is not None:
        p.alignment = align
    r = p.add_run(text)
    set_font(r, name=name, size=size, bold=bold, color=color)
    return p


def blank(n=46, lines=1, space_after=4, line=1.55):
    """手写横线：全角下划线（打印后为连续横线）。"""
    for _ in range(lines):
        para("＿" * n, size=10.5, color=GRAY, space_after=space_after, line=line)


def banner(text):
    """橙色条幅（暂停点页用）。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(8)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), 'E97835')
    pPr.append(shd)
    r = p.add_run("　" + text + "　")
    set_font(r, size=15, bold=True, name="黑体", color=WHITE)


def h_title(text):
    para(text, size=13, bold=True, name="黑体", color=ORANGE_DARK, space_after=6, space_before=2)


def card_title(text):
    """意外卡小标题。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("▍" + text)
    set_font(r, size=11.5, bold=True, name="黑体", color=BLACK)


def tpl_fixed(label, color, text):
    """「正常→万一→应该」模板行：彩色标签＋内容（固定内容，不用写）。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.2
    r1 = p.add_run("■ " + label + "　")
    set_font(r1, size=10.5, bold=True, name="黑体", color=color)
    r2 = p.add_run(text)
    set_font(r2, size=10.5, name="宋体")


def my_zone(label_text, lines=1):
    """「✍️ 我的答案」填写区（1–2 行）。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("✍️ " + label_text)
    set_font(r, size=10.5, bold=True, name="黑体", color=BLACK)
    blank(46, lines=lines, space_after=2)


def teacher_zone(label_text="老师的答案（写错了，就把老师讲的补记在这里）：", lines=1):
    """「🧑🏫 老师的答案」补记区——紧跟在学生填写区下一行。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("🧑🏫 " + label_text)
    set_font(r, size=10, bold=True, name="黑体", color=BLUE)
    blank(46, lines=lines, space_after=2)


def peer_check(no):
    """🤝 互审标签＋同桌互查三连（对应评分标准）。"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("🤝 互审" + no + "　同桌互查三连：")
    set_font(r, size=10.5, bold=True, name="黑体", color=GREEN)
    r2 = p.add_run("□ 机器能懂吗？　□ 想得全吗？　□ 会不会闹笑话？")
    set_font(r2, size=10.5, name="宋体")


def page_head(rec_no, page_label):
    """每页页眉条：左＝册名，右＝记录序号 · 第 N 页。"""
    t = doc.add_table(rows=1, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0 = t.cell(0, 0)
    c0.width = Cm(11)
    p0 = c0.paragraphs[0]
    r0 = p0.add_run("🤖 我的机器人实验记录 · 第 1 讲")
    set_font(r0, size=9, bold=True, color=GRAY)
    c1 = t.cell(0, 1)
    c1.width = Cm(6)
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r1 = p1.add_run("记录" + rec_no + " · " + page_label)
    set_font(r1, size=9, bold=True, color=ORANGE_DARK)
    para("", size=2, space_after=2)


def new_page():
    from docx.enum.text import WD_BREAK
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run()
    r.add_break(WD_BREAK.PAGE)


def add_footer():
    footer = sec.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("05_ 学生记录册 · {} · {} ｜ ✍️ 先写你的 · 🧑🏫 写错了补记老师的 · 写完举册子".format(VERSION, DATE))
    set_font(r, size=9, color=GRAY)


add_footer()

# ================= 封面 =================
para("《财务机器人应用与开发》", size=12, bold=True, name="黑体", color=GRAY,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=2)
para("我的机器人实验记录", size=30, bold=True, name="黑体", color=ORANGE_DARK,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para("第 1 讲 · 开学第一课", size=16, bold=True, name="黑体",
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
para("班级：＿＿＿＿＿＿＿＿　学号：＿＿＿＿＿＿＿＿　姓名：＿＿＿＿＿＿＿＿　互审搭档（同桌）：＿＿＿＿＿＿＿＿",
     size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

para("▍五条规矩", size=11, bold=True, name="黑体", color=ORANGE_DARK, space_after=3)
for s in [
    "① 记录册：只记暂停点和检查点，先写你的，再听讲",
    "② 随机抽人：答不出，同桌帮",
    "③ 同桌互审：一个做、一个查，做完交换",
    "④ 积分：有字 2 分，写好 5 分",
    "⑤ 彩蛋库：好作品，全班看",
]:
    para(s, size=10.5, space_after=2)

para("▍评分标准：机器能懂 +2 分｜想得全（别人没想到的）+3 分｜不闹笑话（机器不懵）+5 分；"
     "好规矩进「规矩宝典」，最好的组获「首席总工程师」🏅", size=10.5, space_before=8, space_after=6)

para("▍标签暗号", size=11, bold=True, name="黑体", color=ORANGE_DARK, space_after=3)
for s in [
    "📒 记录＝翻到标签写的页码，动笔写　　🤝 互审＝同桌互查三连（能懂吗/想得全吗/闹笑话吗）",
    "🙋 提问＝举手抢答　　🎲 提问＝随机抽人",
    "✍️ 先写你的答案；🧑🏫 写错了，就在下一行补记老师怎么讲的",
]:
    para(s, size=10.5, space_after=2)

para("修订记录：v1.2 2026-09-04 精简至 6 页，只记暂停点与检查点，填写区 1–2 行；"
     "v1.1 2026-09-04 标签一一对应版；v1.0 2026-09-04 新建。",
     size=8.5, color=GRAY, space_before=14)

# ================= 第 2 页 · 记录① 暂停点① =================
new_page()
page_head("①", "第 2 页")
banner("⏸ 暂停点① · 什么时候会「出事」？")
para("洗衣机洗一件衣服，正常流程走得好好的——什么时候会「出事」？写下你能想到的意外情况，越多越好。"
     "写完合上，先别讨论。", size=11.5, bold=True, space_after=4)
para("提示：从正常流程的每一步想——放衣服 → 放洗衣液 → 关舱门 → 选模式 → 按启动 → 进水 → 洗涤 → 漂洗 → 脱水 → 蜂鸣结束，"
     "哪一步会出问题？", size=10, color=GRAY, space_after=6)
my_zone("我的意外清单：", lines=2)
teacher_zone("黑板归类＋全班圈出的「最要命的三个」：", lines=2)

# ================= 第 3 页 · 记录②③④ 意外三卡 =================
new_page()
page_head("②③④", "第 3 页")
h_title("洗衣机出事了 · 按「正常 → 万一 → 应该」写规矩")

card_title("意外① 突然停电")
tpl_fixed("正常", GREEN, "进水 → 洗涤 → 漂洗 → 脱水")
tpl_fixed("万一", BLUE, "洗到一半，突然停电")
tpl_fixed("应该", ORANGE, "来电之后，从哪一步继续？（写完举册子）")
my_zone("我的规矩：")
teacher_zone()

card_title("意外② 忘了放洗衣液")
tpl_fixed("正常", GREEN, "放洗衣液 → 进水洗涤")
tpl_fixed("万一", BLUE, "忘了放洗衣液")
tpl_fixed("应该", ORANGE, "机器怎么发现？怎么办？（写完举册子）")
my_zone("我的规矩：")
teacher_zone()

card_title("意外③ 洗好了，一直没人拿")
tpl_fixed("正常", GREEN, "洗完 → 蜂鸣提醒 → 取衣")
tpl_fixed("万一", BLUE, "一直没人来拿")
tpl_fixed("应该", ORANGE, "怎么办？（写完举册子）")
my_zone("我的规矩：")
teacher_zone()

peer_check("①②③")

# ================= 第 4 页 · 记录⑤ 换个机器 =================
new_page()
page_head("⑤", "第 4 页")
h_title("换个机器试试（老师分配 · 限时 3 分钟）")
para("我领到的机器：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿", size=11, bold=True, space_after=6)
my_zone("正常流程（先…再…最后…）：")
teacher_zone()
my_zone("意外规矩（如果…就…，写 3 条）：", lines=2)
teacher_zone()
peer_check("④")

# ================= 第 5 页 · 记录⑥ 当指挥任务单 =================
new_page()
page_head("⑥", "第 5 页")
h_title("学生当指挥 · 任务单（只填空，不自由发挥）")
para("任务 A · 整理乱数据（老师会把原样发给你）：", size=11, bold=True, space_after=2)
para("王芳 13812340001 王芳 wangfang@stu.edu 财会2301 13812340001", size=10.5, color=GRAY, space_after=4)
para("把命令填完整：「请把这行信息整理成表格：①重复的只留＿＿个；②按＿＿＿＿排序；③要＿＿列。」",
     size=11, space_after=2)
teacher_zone("老师的答案：")
para("任务 B · 写班级通知（把要素填全）：", size=11, bold=True, space_before=8, space_after=2)
para("「＿＿＿＿（时间）在＿＿＿＿（地点）＿＿＿＿（事情），请带＿＿＿＿。」", size=11, space_after=2)
teacher_zone("老师的答案：")
peer_check("⑤")
para("小抄：把话说清楚 = 干什么＋怎么算干好", size=10, color=GRAY, space_before=8)

# ================= 第 6 页 · 记录⑦ 暂停点② =================
new_page()
page_head("⑦", "第 6 页")
banner("⏸ 暂停点② · 哪句命令更好？差在哪？")
para("刚才两组上台，给 AI 下命令让它干活。哪句命令更好？差在哪？先写判断，再听分享。",
     size=11.5, bold=True, space_after=4)
my_zone("哪句更好：")
my_zone("差在哪：")
teacher_zone()
para("小抄：把话说清楚 = 干什么＋怎么算干好", size=10, color=GRAY, space_before=8)


def prune(prefix):
    """只保留最新版：删除同前缀、同扩展名的旧文件。"""
    for f in os.listdir(ROOT):
        if f.startswith(prefix) and f.endswith(".docx") and f != os.path.basename(OUT):
            os.remove(os.path.join(ROOT, f))


prune("05_项目一_第1讲_开学第一课_学生记录册_")
doc.save(OUT)
print("已生成:", OUT)
