const crypto = require('crypto');
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();
async function main(){
  await prisma.diagnosticAssessment.deleteMany();
  await prisma.managementProjectAttempt.deleteMany();
  await prisma.aILiteracyAttempt.deleteMany();
  await prisma.relationshipAttempt.deleteMany();
  await prisma.equationAttempt.deleteMany();
  await prisma.lifeGameAttempt.deleteMany();
  await prisma.gestureAttempt.deleteMany();
  await prisma.teacherReview.deleteMany();
  await prisma.session.deleteMany();
  await prisma.simulationRecord.deleteMany();
  await prisma.lifeEvent.deleteMany();
  await prisma.classMember.deleteMany();
  await prisma.learningCycle.deleteMany();
  await prisma.classroom.deleteMany();
  await prisma.course.deleteMany();
  await prisma.user.deleteMany();
  const passwordHash=crypto.createHash('sha256').update('demo1234').digest('hex');
  const teacher=await prisma.user.create({data:{username:'teacher_demo',displayName:'演示教师',role:'TEACHER',passwordHash}});
  const student=await prisma.user.create({data:{username:'student_demo',displayName:'演示学生',role:'STUDENT',passwordHash}});
  const course=await prisma.course.create({data:{name:'基础会计',textbook:'会计学基础（含实训）第4版'}});
  const room=await prisma.classroom.create({data:{name:'基础会计演示班',term:'2026学年',inviteCode:'DEMO2026',courseId:course.id}});
  await prisma.classMember.createMany({data:[{classroomId:room.id,userId:teacher.id,memberRole:'OWNER'},{classroomId:room.id,userId:student.id,memberRole:'STUDENT'}]});
  const now=new Date(),end=new Date(now.getTime()+7*86400000);
  const cycle=await prisma.learningCycle.create({data:{classroomId:room.id,name:'周期02：会计要素与等式',stage:2,startsAt:now,endsAt:end}});
  await prisma.lifeEvent.create({data:{studentId:student.id,classroomId:room.id,cycleId:cycle.id,mode:'模拟记录',participation:'使用系统模拟事项',category:'充值/账户转换',eventDate:now,amount:'100',amountMode:'精确金额',payment:'银行卡',fundFlow:'已经流出',rawDescription:'我从银行卡给校园卡充值100元',redactedSummary:'银行卡向校园卡充值100元',analysisType:'账户转换',analysisFlow:'一个可支配账户减少，另一个增加',diagnosisTag:'ACCOUNT_TRANSFER_AS_EXPENSE',choicesJson:'{}',firstReason:'银行卡减少，校园卡增加，尚未发生实际消费。',revisedReason:'明确两个账户一增一减，资产总额暂不变化。',variationText:'充值赠送20元且赠送金额不能提现。',status:'REVISED',score:88}});
  const templates=[
    ['即时消费','日常消费','食堂消费15元','CASH_EQUALS_EXPENSE'],
    ['资金转入','家庭资金转入','收到家庭生活费','CASH_EQUALS_INCOME'],
    ['垫付/收回','垫付与收回','替同学垫付聚餐费','IGNORE_RECEIVABLE'],
    ['延期支付','延期支付','使用花呗购买用品','IGNORE_LIABILITY'],
    ['退货/退款','退货与退款','网购退货等待退款','CASH_EQUALS_INCOME'],
    ['充值/账户转换','账户转换','银行卡充值校园卡','ACCOUNT_TRANSFER_AS_EXPENSE']
  ];
  for(let i=2;i<=12;i++){
    const u=await prisma.user.create({data:{username:`student_demo_${i}`,displayName:`学生${String.fromCharCode(64+i)}`,role:'STUDENT',passwordHash}});
    await prisma.classMember.create({data:{classroomId:room.id,userId:u.id,memberRole:'STUDENT'}});
    for(let j=0;j<2;j++){
      const t=templates[(i+j)%templates.length],revised=(i+j)%3!==0;
      await prisma.lifeEvent.create({data:{studentId:u.id,classroomId:room.id,cycleId:cycle.id,mode:'模拟记录',participation:'使用系统模拟事项',category:t[0],eventDate:now,amount:String(20+i*5),amountMode:'精确金额',payment:'微信/支付宝',fundFlow:t[0]==='资金转入'?'已经流入':'已经流出',rawDescription:t[2],redactedSummary:t[2],analysisType:t[1],analysisFlow:'演示数据：资金、资源与权利义务变化',diagnosisTag:t[3],choicesJson:'{}',firstReason:'首次判断演示文本',revisedReason:revised?'根据反馈补充主体、时点与权利义务。':null,variationText:'改变支付时间或承担方后重新判断。',status:revised?'REVISED':'SUBMITTED',score:revised?82:60}});
    }
  }
  // 录屏与教师端使用的匿名演示记录；标题明确标注“演示”，不作为真实教学成效。
  await prisma.managementProjectAttempt.createMany({data:[
    {studentId:student.id,projectCode:'BUDGET_DEMO',projectTitle:'预算编制（匿名演示）',firstPrediction:'超过15万元',firstAnswer:96000,revisedAnswer:176000,diagnosisTag:'OMITTED_PERIOD',status:'DEMO_REVISED',score:86},
    {studentId:student.id,projectCode:'COST_DEMO',projectTitle:'成本管理（匿名演示）',firstPrediction:'不利差异',firstAnswer:1450,revisedAnswer:1550,diagnosisTag:'CALCULATION_ERROR',status:'DEMO_REVISED',score:84},
    {studentId:student.id,projectCode:'CVP_DEMO',projectTitle:'本量利分析（匿名演示）',firstPrediction:'不低于3000件',firstAnswer:2500,revisedAnswer:3000,diagnosisTag:'FORMULA_ERROR',status:'DEMO_REVISED',score:88},
    {studentId:student.id,projectCode:'INVEST_DEMO',projectTitle:'投资决策（匿名演示）',firstPrediction:'项目不可行',firstAnswer:-5000,revisedAnswer:-5230,diagnosisTag:'DISCOUNT_ERROR',status:'DEMO_REVISED',score:82}
  ]});
  const demoAssessmentResults=[
    {id:'D1',tag:'延期支付',type:'单选',correct:false},{id:'D2',tag:'时间节点',type:'判断',correct:false},{id:'D3',tag:'会计主体',type:'单选',correct:true},{id:'D4',tag:'数据保护',type:'多选',correct:true},{id:'D5',tag:'管理会计',type:'案例',correct:true}
  ];
  await prisma.diagnosticAssessment.createMany({data:[
    {studentId:student.id,title:'匿名演示诊断测评A',answersJson:'{}',resultJson:JSON.stringify(demoAssessmentResults),score:72,correctCount:22,totalCount:30,status:'DEMO'},
    {studentId:student.id,title:'匿名演示诊断测评B',answersJson:'{}',resultJson:JSON.stringify(demoAssessmentResults.map((x,i)=>({...x,correct:i!==1}))),score:83,correctCount:25,totalCount:30,status:'DEMO'},
    {studentId:student.id,title:'匿名演示诊断测评C',answersJson:'{}',resultJson:JSON.stringify(demoAssessmentResults.map((x,i)=>({...x,correct:i>0}))),score:87,correctCount:26,totalCount:30,status:'DEMO'}
  ]});
  const simTemplates=[['card','校园卡充值与消费'],['credit','花呗购买与还款'],['advance','替同学垫付与收回'],['refund','网购退货与退款'],['prepaid','会员预付与分期受益'],['platform','外卖平台三方结算']];
  for(let i=0;i<30;i++){
    const t=simTemplates[i%simTemplates.length],rev=i%4!==0;
    await prisma.simulationRecord.create({data:{studentId:student.id,classroomId:room.id,cycleId:cycle.id,scenarioId:t[0],scenarioTitle:t[1],stepIndex:i%3,relationsJson:JSON.stringify([{from:0,to:1,type:'资金',amount:String(20+i)}]),elementsJson:JSON.stringify({资产:i%2?'减少':'不变',负债:'不涉及'}),firstChoice:'需要结合主体、时点和权利义务判断',firstReason:'匿名演示推演理由',revisedJson:rev?JSON.stringify({note:'根据反馈修正关系方向和性质'}):null,status:rev?'REVISED':'SUBMITTED',score:rev?78+i%12:55+i%10}});
  }
  for(let i=0;i<12;i++){const completed=[true,true,i%3!==0,i%4!==0],errors={0:i%2,1:i%3,2:i%4,3:i%5};await prisma.relationshipAttempt.create({data:{studentId:student.id,classroomId:room.id,scenario:'借款与还款',score:completed.filter(Boolean).length*25,completedJson:JSON.stringify(completed),errorsJson:JSON.stringify(errors),durationMs:65000+i*2200}})}
  for(let i=0;i<12;i++){const completed=Array.from({length:9},(_,j)=>j<6+i%4),errors=Object.fromEntries(Array.from({length:9},(_,j)=>[j,(i+j)%3]));await prisma.equationAttempt.create({data:{studentId:student.id,classroomId:room.id,score:completed.filter(Boolean).length*10,completedJson:JSON.stringify(completed),errorsJson:JSON.stringify(errors),durationMs:90000+i*3000}})}
  for(let i=0;i<16;i++){const type=i%2?'CLASSIFY':'DETECT',total=8,correct=5+i%4;await prisma.lifeGameAttempt.create({data:{studentId:student.id,classroomId:room.id,gameType:type,score:correct*10,total,correct,durationMs:45000+i*500,detailsJson:'[]'}})}
  for(let i=0;i<12;i++){const expected=['Pointing_Up','Victory','Thumb_Up','Open_Palm','Closed_Fist'];const attempts=expected.map((x,j)=>({question:j+1,expected:x,actual:(i+j)%5===0?'None':x,correct:(i+j)%5!==0}));await prisma.gestureAttempt.create({data:{studentId:student.id,classroomId:room.id,score:attempts.filter(x=>x.correct).length*20,attemptsJson:JSON.stringify(attempts),durationMs:42000+i*1500}})}
  await prisma.teacherReview.createMany({data:[
    {app:'LIFE_LEDGER',reviewType:'LOW_CONFIDENCE',title:'父母转生活费：主体判断',detail:'AI无法确定学生采用个人资金视角还是企业会计视角',studentLabel:'演示学生',confidence:0.68},
    {app:'LIFE_LEDGER',reviewType:'RULE_CONFLICT',title:'结构化选择与理由冲突',detail:'选择“不属于收入”，理由中却写“收入增加”',studentLabel:'学生D'},
    {app:'PAYMENT_SIMULATOR',reviewType:'LOW_CONFIDENCE',title:'平台补贴由谁承担',detail:'外卖平台场景缺少优惠承担方证据',studentLabel:'演示学生',confidence:0.64},
    {app:'PAYMENT_SIMULATOR',reviewType:'RULE_CONFLICT',title:'关系图与理由不一致',detail:'图中为资金流，理由描述为偿还义务',studentLabel:'学生D'},
    {app:'PAYMENT_SIMULATOR',reviewType:'OPEN_SCENARIO',title:'二手交易主体判断',detail:'需要教师确认当前分析的是买方、卖方还是平台',studentLabel:'学生E'}
  ]});
  console.log({teacher:teacher.username,student:student.username,classroom:room.name,students:12,simulations:30,reviews:5});
}
main().finally(()=>prisma.$disconnect());
