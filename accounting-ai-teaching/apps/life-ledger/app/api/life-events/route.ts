import { NextResponse } from 'next/server';
import { prisma } from '../../../lib/prisma';
import { currentUser } from '../../../lib/auth';
export async function GET(request:Request){
 try{
  const user=await currentUser();if(!user)return NextResponse.json({ok:false,error:'请先登录'},{status:401});
  const classId=new URL(request.url).searchParams.get('classroomId');
  if(user.role==='TEACHER'&&classId){const m=await prisma.classMember.findUnique({where:{classroomId_userId:{classroomId:classId,userId:user.id}}});if(!m)return NextResponse.json({ok:false,error:'无权查看该班级'},{status:403})}
  const eventWhere=user.role==='TEACHER'?(classId?{classroomId:classId}:{}):{studentId:user.id};
  const studentWhere=classId?{classroomId:classId,memberRole:'STUDENT'}:{memberRole:'STUDENT'};
  const [events,students]=await Promise.all([prisma.lifeEvent.findMany({where:eventWhere,orderBy:{createdAt:'desc'},take:100,select:{id:true,category:true,analysisType:true,redactedSummary:true,diagnosisTag:true,status:true,score:true,createdAt:true,firstReason:true,revisedReason:true,classroomId:true,cycleId:true}}),prisma.classMember.count({where:studentWhere})]);
  const revised=events.filter(x=>x.status==='REVISED').length;const tags:Record<string,number>={};events.forEach(x=>{if(x.diagnosisTag)tags[x.diagnosisTag]=(tags[x.diagnosisTag]||0)+1});
  return NextResponse.json({ok:true,events,stats:{students,total:events.length,revised,revisionRate:events.length?Math.round(revised/events.length*100):0,tags}})
 }catch{return NextResponse.json({ok:false,error:'数据库读取失败'},{status:500})}
}
export async function POST(request:Request){
 try{const b=await request.json();const student=await currentUser();if(!student||student.role!=='STUDENT')return NextResponse.json({ok:false,error:'仅学生可提交'},{status:403});const membership=await prisma.classMember.findFirst({where:{userId:student.id,memberRole:'STUDENT'},include:{classroom:{include:{cycles:{orderBy:{startsAt:'desc'},take:1}}}}});if(!membership)return NextResponse.json({ok:false,error:'请先加入班级'},{status:400});const cycle=membership.classroom.cycles[0];
  const event=await prisma.lifeEvent.create({data:{studentId:student.id,classroomId:membership.classroomId,cycleId:cycle?.id,mode:b.mode,participation:b.participation,category:b.category,eventDate:new Date(b.eventDate),amount:b.amount||null,amountMode:b.amountMode,payment:b.payment||null,fundFlow:b.fundFlow,rawDescription:b.rawDescription,redactedSummary:b.redactedSummary,analysisType:b.analysisType,analysisFlow:b.analysisFlow,diagnosisTag:b.diagnosisTag||null,choicesJson:JSON.stringify(b.choices||{}),firstReason:b.firstReason,variationText:b.variationText||null,status:'SUBMITTED',score:typeof b.score==='number'?b.score:60}});if(['ACCOUNTING_ENTITY_CONFUSION','MULTIPLE_EVENTS_MERGED'].includes(b.diagnosisTag)){await prisma.teacherReview.create({data:{app:'LIFE_LEDGER',reviewType:'LOW_CONFIDENCE',title:`${b.analysisType}需要教师复核`,detail:'AI识别到会计主体或多事项边界存在不确定性。',targetId:event.id,studentLabel:student.displayName,confidence:0.68}})}return NextResponse.json({ok:true,event,classroom:membership.classroom.name,cycle:cycle?.name})
 }catch{return NextResponse.json({ok:false,error:'保存失败，请检查数据库'},{status:500})}
}
export async function PATCH(request:Request){
 try{const b=await request.json();const user=await currentUser();if(!user)return NextResponse.json({ok:false,error:'请先登录'},{status:401});const existing=await prisma.lifeEvent.findUnique({where:{id:b.id}});if(!existing||(user.role!=='TEACHER'&&existing.studentId!==user.id))return NextResponse.json({ok:false,error:'无权修改'},{status:403});const event=await prisma.lifeEvent.update({where:{id:b.id},data:{revisedReason:b.revisedReason,status:'REVISED',score:typeof b.score==='number'?b.score:88}});return NextResponse.json({ok:true,event})}catch{return NextResponse.json({ok:false,error:'订正保存失败'},{status:500})}
}
