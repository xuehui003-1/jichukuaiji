import { NextResponse } from 'next/server';
import { prisma } from '../../../lib/prisma';
import { currentUser } from '../../../lib/auth';
export async function GET(request:Request){
 const teacher=await currentUser();if(!teacher||teacher.role!=='TEACHER')return NextResponse.json({ok:false,error:'仅教师可查看'},{status:403});
 const q=new URL(request.url).searchParams,classroomId=q.get('classroomId'),studentId=q.get('studentId');if(!classroomId)return NextResponse.json({ok:false,error:'缺少班级'},{status:400});
 const own=await prisma.classMember.findUnique({where:{classroomId_userId:{classroomId,userId:teacher.id}}});if(!own)return NextResponse.json({ok:false,error:'无权查看该班级'},{status:403});
 if(studentId){const member=await prisma.classMember.findUnique({where:{classroomId_userId:{classroomId,userId:studentId}},include:{user:true}});if(!member||member.memberRole!=='STUDENT')return NextResponse.json({ok:false,error:'学生不存在'},{status:404});const [lifeEvents,simulations]=await Promise.all([prisma.lifeEvent.findMany({where:{classroomId,studentId},orderBy:{createdAt:'desc'},select:{id:true,analysisType:true,redactedSummary:true,diagnosisTag:true,status:true,score:true,firstReason:true,revisedReason:true,createdAt:true}}),prisma.simulationRecord.findMany({where:{classroomId,studentId},orderBy:{createdAt:'desc'},select:{id:true,scenarioTitle:true,stepIndex:true,status:true,score:true,firstChoice:true,firstReason:true,revisedJson:true,createdAt:true}})]);return NextResponse.json({ok:true,student:{id:member.user.id,displayName:member.user.displayName,username:member.user.username},lifeEvents,simulations})}
 const members=await prisma.classMember.findMany({where:{classroomId,memberRole:'STUDENT'},include:{user:true},orderBy:{user:{displayName:'asc'}}});const students=await Promise.all(members.map(async m=>{const [lifeTotal,lifeRevised,simTotal,simRevised,lifeAgg,simAgg]=await Promise.all([prisma.lifeEvent.count({where:{classroomId,studentId:m.userId}}),prisma.lifeEvent.count({where:{classroomId,studentId:m.userId,status:'REVISED'}}),prisma.simulationRecord.count({where:{classroomId,studentId:m.userId}}),prisma.simulationRecord.count({where:{classroomId,studentId:m.userId,status:'REVISED'}}),prisma.lifeEvent.aggregate({where:{classroomId,studentId:m.userId},_avg:{score:true}}),prisma.simulationRecord.aggregate({where:{classroomId,studentId:m.userId},_avg:{score:true}})]);const total=lifeTotal+simTotal,revised=lifeRevised+simRevised;return{id:m.user.id,displayName:m.user.displayName,username:m.user.username,lifeTotal,simTotal,revisedRate:total?Math.round(revised/total*100):0,averageScore:Math.round(((lifeAgg._avg.score||0)+(simAgg._avg.score||0))/((lifeTotal?1:0)+(simTotal?1:0)||1))}}));return NextResponse.json({ok:true,students})
}

export async function POST(request:Request){
 const teacher=await currentUser();if(!teacher||teacher.role!=='TEACHER')return NextResponse.json({ok:false,error:'仅教师可创建学生账号'},{status:403});const b=await request.json();const own=await prisma.classMember.findUnique({where:{classroomId_userId:{classroomId:b.classroomId,userId:teacher.id}}});if(!own||own.memberRole!=='OWNER')return NextResponse.json({ok:false,error:'无权管理该班级'},{status:403});const names:Array<string>=(b.names||[]).map((x:any)=>String(x).trim()).filter(Boolean).slice(0,100);if(!names.length)return NextResponse.json({ok:false,error:'请至少填写一名学生'},{status:400});const crypto=await import('node:crypto');const credentials=[];for(let i=0;i<names.length;i++){let username=String(b.usernames?.[i]||'').trim();if(!username){const base=`stu_${Date.now().toString().slice(-6)}_${i+1}`;username=base}while(await prisma.user.findUnique({where:{username}}))username=`${username}_${Math.floor(Math.random()*90+10)}`;const password=crypto.randomBytes(4).toString('hex').slice(0,8),passwordHash=crypto.createHash('sha256').update(password).digest('hex');const user=await prisma.user.create({data:{username,displayName:names[i],role:'STUDENT',passwordHash,forcePasswordChange:true,memberships:{create:{classroomId:b.classroomId,memberRole:'STUDENT'}}}});credentials.push({id:user.id,displayName:user.displayName,username,password})}return NextResponse.json({ok:true,credentials})
}
export async function PATCH(request:Request){
 const teacher=await currentUser();if(!teacher||teacher.role!=='TEACHER')return NextResponse.json({ok:false,error:'仅教师可重置密码'},{status:403});const b=await request.json();const target=await prisma.classMember.findUnique({where:{classroomId_userId:{classroomId:b.classroomId,userId:b.studentId}}});const own=await prisma.classMember.findUnique({where:{classroomId_userId:{classroomId:b.classroomId,userId:teacher.id}}});if(!target||!own||own.memberRole!=='OWNER')return NextResponse.json({ok:false,error:'无权操作'},{status:403});const crypto=await import('node:crypto');const password=crypto.randomBytes(4).toString('hex').slice(0,8),passwordHash=crypto.createHash('sha256').update(password).digest('hex');await prisma.user.update({where:{id:b.studentId},data:{passwordHash,forcePasswordChange:true}});return NextResponse.json({ok:true,password})
}

export async function DELETE(request:Request){
 const teacher=await currentUser();
 if(!teacher||teacher.role!=='TEACHER')return NextResponse.json({ok:false,error:'仅教师可删除学习记录'},{status:403});
 const b=await request.json(),classroomId=String(b.classroomId||''),id=String(b.id||''),type=String(b.type||'');
 if(!classroomId||!id||!['life','simulation'].includes(type))return NextResponse.json({ok:false,error:'删除参数不完整'},{status:400});
 const own=await prisma.classMember.findUnique({where:{classroomId_userId:{classroomId,userId:teacher.id}}});
 if(!own)return NextResponse.json({ok:false,error:'无权管理该班级记录'},{status:403});
 if(type==='life'){
  const record=await prisma.lifeEvent.findUnique({where:{id}});if(!record||record.classroomId!==classroomId)return NextResponse.json({ok:false,error:'记录不存在'},{status:404});
  await prisma.$transaction([prisma.teacherReview.deleteMany({where:{targetId:id}}),prisma.lifeEvent.delete({where:{id}})]);
 }else{
  const record=await prisma.simulationRecord.findUnique({where:{id}});if(!record||record.classroomId!==classroomId)return NextResponse.json({ok:false,error:'记录不存在'},{status:404});
  await prisma.$transaction([prisma.teacherReview.deleteMany({where:{targetId:id}}),prisma.simulationRecord.delete({where:{id}})]);
 }
 return NextResponse.json({ok:true});
}
