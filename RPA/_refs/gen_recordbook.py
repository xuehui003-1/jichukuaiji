# -*- coding: utf-8 -*-
"""
生成《05_项目一_第1讲_开学第一课_学生记录册》Word 文档。
v1.4 表格化改版（学基础会计 90-A1 记录册设计，配套 04_课件 v1.7）：
  结构＝暂停点①–⑤，每个暂停点三段：①题目描述一行 → ②三行空表格（我的想法/思考过程/老师的讲解）→ 下一个暂停点；
  空行全部改为带边框的空表格（左列标签＋右列作答），不再用下划线空行，也不出现嵌套编号；
  全册 1 页（标题三行＋5 个暂停点＋下课前自查），每人打印 1 页；
  封面语沿用基础会计记录册哲学：先写你的想法再听老师讲，猜错不扣分，猜错的地方正是今天要学的。
版本号机制同规划文档：改 VERSION / DATE / REVISION_HISTORY 后重跑，旧版自动删除（只保留最新版）。
"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.table import WD_ROW_HEIGHT_RULE

# ============ 每次修订只需要改这里 ============
VERSION = "v1.4"
DATE = "2026-09-04"
REVISION_HISTORY = [
    ("v1.4", "2026-09-04",
     "表格化改版（学基础会计 90-A1 记录册设计）：①每个暂停点＝题目描述一行＋三行空表格"
     "（左列「我的想法/思考过程/老师的讲解」＋右列作答），空行全部改为带边框空表格，"
     "删除下划线空行与嵌套编号，暂停点①–⑤依次排开不再叠套；②全册 1 页＋底部「下课前自查」；"
     "③封面语沿用基础会计：先写你的想法再听老师讲，猜错不扣分，猜错的地方正是今天要学的。"),
    ("v1.3", "2026-09-04",
     "暂停点制改版：全册 1 页、无分页符、无页眉，只收录暂停点，每处三行（①想法→②思考过程→③老师的讲解）。"),
    ("v1.2", "2026-09-04",
     "精简至 6 页，只记暂停点与老师检查点；填写区 1–2 行＋老师的答案区。"),
    ("v1.1", "2026-09-04",
     "标签一一对应版：页面按课堂顺序重排，页眉标「记录①–⑩」，填写项双区。"),
    ("v1.0", "2026-09-04",
     "新建，配套 04_课件 v1.3（学生视角版）。"),
]

# ============ 颜色 ============
ORANGE = (233, 120, 53)
ORANGE_DARK = (194, 90, 31)
BLUE = (59, 110, 165)
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


def pause_point(no, title, desc, labels=("我的想法", "思考过程", "老师的讲解")):
    """一个暂停点：标题行 → 题目描述一行 → 三行空表格（左列标签＋右列作答）。"""
    # 标题行
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run("⏸ 暂停点" + no + "　" + title)
    set_font(r, size=11.5, bold=True, name="黑体", color=ORANGE_DARK)
    # 题目描述一行
    para(desc, size=9.5, color=GRAY, space_after=2)
    # 三行空表格
    t = doc.add_table(rows=3, cols=2)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, lab in enumerate(labels):
        row = t.rows[i]
        row.height = Cm(0.9)
        row.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
        c0 = row.cells[0]
        c0.width = Cm(2.6)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(lab)
        set_font(r0, size=9.5, bold=True, name="黑体", color=BLACK)
        c1 = row.cells[1]
        c1.width = Cm(14.8)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)


def add_footer():
    footer = sec.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("05_ 学生记录册 {} · {} ｜ 看到课件「📒暂停点N」才动笔".format(VERSION, DATE))
    set_font(r, size=8.5, color=GRAY)


add_footer()

# ================= 页首（标题三行） =================
para("我 的 机 器 人 实 验 记 录", size=18, bold=True, name="黑体",
     align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=1)
para("《财务机器人应用与开发》· 第 1 讲　　　　班级：＿＿＿＿　　学号：＿＿＿＿＿＿　　"
     "姓名：＿＿＿＿　　互审搭档：＿＿＿＿", size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
para("这不是作业本，是实验记录。课上看到「📒暂停点N」才动笔：先写你的想法，再听老师讲；"
     "猜错不扣分——猜错的地方，正是你今天要学的地方。",
     size=9, color=GRAY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)

# ================= 暂停点①–⑤ =================
pause_point("①", "什么时候会「出事」？",
            "正常流程：放衣服→放洗衣液→关舱门→选模式→按启动→进水→洗涤→漂洗→脱水→蜂鸣结束。"
            "哪一步会出问题？把你想到的意外情况都写下来（越多越好）。")

pause_point("②", "洗衣机出事了①：停电",
            "正常：进水→洗涤→漂洗→脱水；万一：洗到一半突然停电。来电后，从哪一步继续？写下你的规矩。")

pause_point("③", "洗衣机出事了②：忘了放洗衣液",
            "正常：放洗衣液→进水洗涤；万一：忘了放洗衣液。机器怎么发现？怎么办？写下你的规矩。")

pause_point("④", "洗衣机出事了③：一直没人拿",
            "正常：洗完→蜂鸣提醒→取衣；万一：一直没人来拿。怎么办？写下你的规矩。")

pause_point("⑤", "哪句 AI 命令更好？差在哪？",
            "刚才两组上台给 AI 下命令。哪句命令更好？差在哪？先写判断，再听分享。")

# ================= 下课前自查 =================
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(2)
r = p.add_run("下课前自查：")
set_font(r, size=10, bold=True, name="黑体", color=ORANGE_DARK)
r2 = p.add_run("□ 暂停点①我写出了意外　□ ②③④我写了规矩　□ ⑤我写了哪句更好　　"
               "我猜错最惨的：＿＿＿＿＿＿＿＿＿＿")
set_font(r2, size=10, name="宋体")


def prune(prefix):
    """只保留最新版：删除同前缀、同扩展名的旧文件。"""
    for f in os.listdir(ROOT):
        if f.startswith(prefix) and f.endswith(".docx") and f != os.path.basename(OUT):
            os.remove(os.path.join(ROOT, f))


prune("05_项目一_第1讲_开学第一课_学生记录册_")
doc.save(OUT)
print("已生成:", OUT)
