# 基础会计AI教学软件

本项目包含两个可独立运行的响应式Web应用：

1. **大学生生活记账与会计AI伴学软件**（应用A，常规项目主申报候选）
2. **校园数字支付与会计AI推演软件**（应用B，专项/创新展示候选）

## 技术环境

- Node.js 20 LTS或22 LTS
- npm 10+
- Next.js 16.2.11
- React 19
- Prisma 6.19.3
- SQLite
- Three.js
- MediaPipe本地手势识别
- DeepSeek OpenAI兼容接口/Mock规则模式

## Windows首次安装

双击：

```text
setup-first-time.cmd
```

脚本会安装依赖、初始化演示数据库并构建两个生产版本。若Prisma官方下载因TLS或校园网限制失败，脚本会自动改用国内镜像重试；也可单独运行`repair-prisma-network.cmd`。

> `npm run db:setup`会重置SQLite演示数据。真实试用后不要直接执行，先运行`backup-data.cmd`。

## 启动

```text
start-app-a.cmd  应用A：http://localhost:3000
start-app-b.cmd  应用B：http://localhost:3001
start-both-apps.cmd  同时启动
```

摄像头手势应使用`localhost`、`127.0.0.1`或HTTPS。普通HTTP局域网地址可能被浏览器拒绝摄像头权限。

## 演示账号

```text
学生：student_demo / demo1234
教师：teacher_demo / demo1234
演示班邀请码：DEMO2026
```

登录页同时提供一键学生/教师演示入口。

## AI模式

在线模式配置：

```text
configure-deepseek.cmd
```

离线/Mock模式：

```text
use-mock-ai.cmd
```

真实API Key只写入本机`.env.local`，不得放入源码包、截图或聊天内容。

## 应用A核心闭环

```text
生活事项
→输入质量检查
→AI结构化（不抢答）
→学生首次判断
→规则/AI追问
→学生订正
→变式迁移
→成长记录
→班级认知地图
→教师复核与AI备课
```

特色模块：

- 真实、模糊、模拟三种隐私模式
- 动态结构化判断与理由支架
- 3D会计等式九类业务实验
- 双主体生活经济关系剧场
- 简单手势判断：☝左、✌右、👍是、✊否
- 生活会计小游戏
- 教师认知地图、学生轨迹和人机协同复核

## 应用B核心闭环

```text
数字支付场景
→首次预测
→建立资金/商品/权利义务关系
→切换时间节点
→规则/AI反馈
→实际修改并订正
→会计要素迁移
→教师关系与时间节点诊断
```

特色模块：

- 10个数字支付场景
- 关系箭头和节点拖动
- 3D空间推演实验室
- 本地手势主体闯关：☝商家、✌学生、👍信用支付方
- 摄像头本地处理与按钮备选
- 教师场景、关系、时间节点和手势统计

> 当前功能是“3D＋本地手势识别”，不是严格意义上的AR。

## 数据与备份

数据库：

```text
prisma/dev.db
```

备份：

```text
backup-data.cmd
```

查看备份：

```text
list-backups.cmd
```

教师默认查看脱敏摘要；摄像头视频不上传、不保存、不发送给DeepSeek。

## 发布检查

```bash
npm run check:release
```

该命令检查：

- UI按钮
- TypeScript
- 应用A生产构建
- 应用B生产构建

健康检查：

```text
http://localhost:3000/api/health
http://localhost:3001/api/health
```

预期：

```json
{"ok":true,"database":"connected"}
```

## 参赛数据口径

教师端部分百分比明确标记为“演示班样例指标”。在取得5—10名学生真实试用数据前，不得将其表述为真实教学成效。正式视频应区分：

- SQLite实时记录
- 演示数据
- 真实试用数据

参赛材料位于：

```text
参赛材料/
试用材料/
```
