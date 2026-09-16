from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path
OUT=Path(__file__).parent

def setup(doc,title):
 sec=doc.sections[0];sec.top_margin=Inches(.75);sec.bottom_margin=Inches(.75);sec.left_margin=Inches(.8);sec.right_margin=Inches(.8)
 styles=doc.styles
 styles['Normal'].font.name='Microsoft YaHei';styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'),'微软雅黑');styles['Normal'].font.size=Pt(10.5)
 for n,size,color in [('Title',24,'26365D'),('Heading 1',16,'26365D'),('Heading 2',13,'5360D8'),('Heading 3',11,'278966')]:
  st=styles[n];st.font.name='Microsoft YaHei';st._element.rPr.rFonts.set(qn('w:eastAsia'),'微软雅黑');st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string(color)
 p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=p.add_run(title);r.bold=True;r.font.size=Pt(24);r.font.color.rgb=RGBColor(38,54,93)

def bullet(doc,text):doc.add_paragraph(text,style='List Bullet')
def table(doc,rows,widths=None):
 t=doc.add_table(rows=1,cols=len(rows[0]));t.style='Light Shading Accent 1'
 for i,x in enumerate(rows[0]):t.rows[0].cells[i].text=str(x)
 for row in rows[1:]:
  c=t.add_row().cells
  for i,x in enumerate(row):c[i].text=str(x)
 return t

def placeholder(doc,text):
 # 正式提交版不保留未完成的截图占位符；界面操作由软件演示视频呈现。
 return None

doc=Document();setup(doc,'大学生生活记账与会计AI伴学软件\n设计说明书')
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run('\n高等教育组·自制教学工具软件\n作者：薛辉、马丽荣、马珍珍\n单位：石家庄邮电职业技术学院\n2026年7月').font.size=Pt(12)
doc.add_page_break()
doc.add_heading('摘要',1);doc.add_paragraph('本软件面向高职《基础会计》初学者，源于教师使用企业微信收集学生一周经济活动时发现的集中补填、重复应付、概念混淆和评价耗时等真实问题。软件将学生日常收支、校园卡充值、花呗、垫付和退款等生活事项转化为个性化会计学习任务，采用规则引擎、DeepSeek和教师复核协同机制，形成“记录—判断—反馈—订正—迁移—评价—备课”闭环。')
doc.add_paragraph('关键词：基础会计；AI伴学；形成性评价；生活记账；人机协同')
doc.add_heading('1 项目背景',1)
doc.add_heading('1.1 真实教学问题',2)
for x in ['学生在截止日期前集中补填，无法证明持续观察。','大量重复“吃饭、外卖”，记录数量不等于学习质量。','将“支出、资金、生活需求”等非规范概念当作会计要素。','把现金流入等同收入、现金流出等同费用。','忽略花呗、垫付、退款中的债权债务和时间节点。','教师逐条阅读开放文本耗时，难以及时反馈。']:bullet(doc,x)
placeholder(doc,'原企业微信任务匿名记录')
doc.add_heading('1.2 教材依据',2);doc.add_paragraph('教材：《会计学基础（含实训）》第4版，任伟峰、张勇、降艳琴主编，北京理工大学出版社，ISBN 9787576342566。重点对接项目一任务2“认识企业经济业务”和项目二任务1“理解会计基本理论”。')
doc.add_heading('2 设计目标与理念',1)
table(doc,[['设计主线','功能体现'],['知识模型化','生活事项动态认知模型、主体—关系—时间—要素四层结构'],['练习游戏化','60秒分类挑战、AI生活账找茬、情境和变式挑战'],['评价数据化','首次判断、订正、迁移、复核、认知地图和个人轨迹'],['教学智能化','DeepSeek伴学、教师复核、AI备课和资源推荐']])
doc.add_heading('3 用户与应用场景',1)
table(doc,[['角色','主要功能'],['学生','记录事项、完成判断、理由、订正、变式、小游戏和成长档案'],['教师','班级、账号、周期、认知地图、学生轨迹、复核、AI备课、导出'],['演示/试用人员','一键角色演示、聚光灯引导、30秒复核亮点和本机离线体验']])
doc.add_heading('4 总体架构',1);doc.add_paragraph('前端采用Next.js、React和TypeScript；服务端API负责认证、规则、AI和数据访问；Prisma连接SQLite本机数据库；DeepSeek提供语义理解和开放式生成；Mock模式保障断网运行。')
placeholder(doc,'系统技术架构图')
doc.add_heading('5 核心教学流程',1)
steps=['学生选择真实、模糊或模拟记录。','系统检查主体、类型、日期、金额、资金状态、多事项和重复。','AI或离线规则完成结构化，学生核对。','学生先完成结构化判断，再使用理由支架表达。','规则引擎检查确定性内容，DeepSeek提出个性化追问。','学生完成实质性订正并查看前后对照。','系统生成变式迁移并进入成长档案。','教师查看班级认知地图和个人轨迹。']
for i,x in enumerate(steps,1):doc.add_paragraph(f'{i}. {x}')
doc.add_heading('6 学生端功能',1)
for h,txt in [('6.1 引导式记录','支持真实、模糊和模拟三种模式；一次只记录一个事项。'),('6.2 输入质量检查','检查无关内容、多事项、日期、金额冲突和同类重复。'),('6.3 动态认知模型','从生活语言逐步展示主体、资金资源、权利义务和企业迁移。'),('6.4 结构化判断与理由支架','客观选项由规则评分，开放理由由AI辅助评价。'),('6.5 订正与变式','必须实际修改后才能完成订正，并保留首次与订正证据。'),('6.6 3D会计等式实验','将教材九类经济业务转化为账户增减选择和3D天平反馈，结果写入SQLite。'),('6.7 双主体关系剧场','通过借款、押金、预付和垫付案例比较双方权利义务，支持简单本地手势判断和按钮备选。'),('6.8 生活会计小游戏','学生端从左侧“情境挑战”进入，可完成60秒会计分类挑战和AI生活账找茬；成绩、正确数、用时和明细写入SQLite。教师端从左侧“游戏数据”查看班级完成情况。'),('6.9 成长档案','展示记录、订正率、错误变化和阶段表现。')]:doc.add_heading(h,2);doc.add_paragraph(txt);placeholder(doc,h)
doc.add_heading('7 教师端功能',1)
for h in ['班级与邀请码','学生试用账号','学习周期','班级认知地图','个人学习轨迹','AI复核闭环','AI运行状态','小游戏数据','AI备课与资源推荐','成绩和匿名数据导出']:bullet(doc,h)
placeholder(doc,'教师决策中心全景')
doc.add_heading('8 AI与规则协同',1)
table(doc,[['环节','负责机制'],['日期、金额、选项矛盾','规则引擎'],['自然语言结构化','DeepSeek/Mock'],['个性化追问','DeepSeek/预设规则'],['开放理由初评','DeepSeek'],['低置信度和冲突','教师复核'],['最终成绩','教师']])
doc.add_paragraph('原则：AI不在学生首次判断前泄露答案，不独立决定最终成绩，不虚构教材、政策和参考依据。')
doc.add_heading('9 数据库与权限',1);doc.add_paragraph('SQLite保存用户、课程、教学班、周期、生活记录、首次答案、订正、游戏、AI日志、教师复核和备课方案。HttpOnly Cookie保存会话；学生只能读取自己的数据；教师只能读取所管理班级数据。')
doc.add_heading('10 隐私与安全',1)
for x in ['不接入银行卡、微信或支付宝账户。','教师默认查看脱敏摘要。','真实、模糊、模拟记录学习效力相同。','API Key仅保存在本机环境变量。','摄像头视频仅本地处理，不上传、不保存。','支持SQLite备份、健康检查和发布检查。']:bullet(doc,x)
doc.add_heading('11 创新点',1)
for x in ['隐私可控的生活事项生成个性化会计学习任务。','生活辨析与企业会计迁移双层结构。','规则、DeepSeek、教师复核三方协同。','首次判断—AI反馈—订正—变式全过程留痕。','班级认知地图驱动教学决策。','基于当前班级过程数据的AI备课和内部资源推荐。']:bullet(doc,x)
doc.add_heading('12 当前验证状态与后续教学应用',1);doc.add_paragraph('作品源于既有真实课程作业和匿名问题分析，当前已完成软件功能测试、典型案例回放、按钮审计、权限检查、跨电脑免安装运行测试和生产构建。因作品定型阶段处于暑假，尚未组织新一轮正式学生课堂试用；教师端部分百分比已明确标注为演示班样例指标，仅用于说明分析功能，不作为教学效果结论。作品计划于2026年秋季学期开展学生前测、软件任务、后测、迁移测试和问卷，并据实统计有效记录率、首次正确率、订正率、迁移正确率及教师评价时间。当前不提供虚构的前后测统计图。')
placeholder(doc,'前后测与问卷统计图')
doc.add_heading('13 测试与运行',1)
table(doc,[['测试','要求'],['生产构建','应用A生产构建通过'],['UI按钮审计','无明显空按钮'],['健康检查','数据库connected'],['离线模式','核心流程可完成'],['权限','学生/教师隔离'],['多设备','电脑与手机浏览器；摄像头使用localhost或HTTPS'],['AI故障','自动降级Mock']])
doc.add_heading('14 推广与迭代',1);doc.add_paragraph('可推广到基础会计、财经素养、智能财税、管理会计实训和财务机器人应用等课程。后续可迁移PostgreSQL并部署公网，扩展学校统一身份认证和更多课程模型。')
doc.add_heading('15 结论',1);doc.add_paragraph('作品以真实教学问题为起点，通过模型化、游戏化、数据化和智能化构建基础会计学习闭环，旨在支持学生形成更清晰的主体、权利义务和会计要素认知，并为教师提供可解释、可复核、可推广的数字化教学工具。实际教学效果将在2026年秋季学期课堂应用后据实验证。')
doc.add_heading('附录：当前正式版本功能补充',1);doc.add_paragraph('当前正式版本进一步加入错误标签驱动的诊断分流：学生提交首次判断后，系统自动定位第一处错误，并按问题类型推荐3D会计等式或生活经济关系剧场；专项训练完成后返回原事项继续订正。生活事项四层认知模型、3D等式模型、双主体权利义务模型和校园经济生活图谱构成四类知识模型体系。教师端增加总括说明、精确导航、单条误记录删除、AI复核闭环和学情驱动AI备课。Windows交付采用Next.js Standalone免安装包，默认Mock模式且不包含API Key。');doc.save(OUT/'软件设计说明书.docx')

# Installation guide
ins=Document();setup(ins,'安装运行与卸载说明')
ins.add_heading('1 运行环境',1);ins.add_paragraph('Windows 10/11，Node.js 20 LTS或22 LTS，Chrome或Edge最新版。在线AI需要网络和DeepSeek API Key；离线Mock模式不需要API。')
ins.add_heading('2 首次安装',1);ins.add_paragraph('解压软件包后双击setup-first-time.cmd。脚本依次安装依赖、初始化SQLite演示数据库并构建生产版本。等待出现SETUP COMPLETED SUCCESSFULLY。')
ins.add_heading('3 AI配置（可选）',1);ins.add_paragraph('首次安装后、启动应用前双击configure-deepseek.cmd并在本机输入API Key。配置后重启服务器。未配置时自动使用Mock。')
ins.add_heading('4 启动',1);ins.add_paragraph('双击start-app-a.cmd，浏览器访问http://localhost:3000。演示学生student_demo，演示教师teacher_demo，密码demo1234。')
ins.add_heading('5 局域网',1);ins.add_paragraph('双击show-network-address.cmd查看192.168开头地址。其他设备需位于同一专用网络。')
ins.add_heading('6 停止与卸载',1);ins.add_paragraph('关闭服务器窗口或按Ctrl+C停止。备份prisma/dev.db后，删除项目文件夹即可卸载。')
ins.add_heading('7 自检',1);ins.add_paragraph('双击verify-running.cmd检查运行状态；双击release-check.cmd执行按钮审计和生产构建。')
ins.add_heading('8 数据重置警告',1);ins.add_paragraph('reset-demo-data或db:setup会删除当前本机测试数据，仅用于演示重置。正式试用前后请运行backup-data.cmd。')
ins.save(OUT/'安装运行与卸载说明.docx')
print('created')
