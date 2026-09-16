import { NextResponse } from 'next/server';
import crypto from 'node:crypto';
import { prisma } from '../../../lib/prisma';
import { currentUser } from '../../../lib/auth';
export async function GET(){
 const user=await currentUser();if(!user)return NextResponse.json({ok:false,error:'请先登录'},{status:401});
 const memberships=await prisma.classMember.findMany({where:{userId:user.id},include:{classroom:{include:{course:true,cycles:{orderBy:{startsAt:'desc'}},_count:{select:{members:true}}}}}});
 return NextResponse.json({ok:true,classrooms:memberships.map(m=>({...m.classroom,memberRole:m.memberRole}))});
}
export async function POST(request:Request){
 const user=await currentUser();if(!user||user.role!=='TEACHER')return NextResponse.json({ok:false,error:'仅教师可创建班级'},{status:403});
 const b=await request.json();if(!b.name?.trim())return NextResponse.json({ok:false,error:'请填写班级名称'},{status:400});
 let course=await prisma.course.findFirst({where:{name:b.courseName||'基础会计'}});if(!course)course=await prisma.course.create({data:{name:b.courseName||'基础会计'}});
 let inviteCode='';for(let i=0;i<5;i++){inviteCode=crypto.randomBytes(3).toString('hex').toUpperCase();if(!await prisma.classroom.findUnique({where:{inviteCode}}))break}
 const classroom=await prisma.classroom.create({data:{name:b.name.trim(),term:b.term||'2026学年',inviteCode,courseId:course.id,members:{create:{userId:user.id,memberRole:'OWNER'}}},include:{course:true,_count:{select:{members:true}}}});
 return NextResponse.json({ok:true,classroom});
}
export async function PATCH(request:Request){
 const user=await currentUser();if(!user||user.role!=='STUDENT')return NextResponse.json({ok:false,error:'仅学生可加入班级'},{status:403});
 const b=await request.json();const classroom=await prisma.classroom.findUnique({where:{inviteCode:String(b.inviteCode||'').trim().toUpperCase()}});if(!classroom)return NextResponse.json({ok:false,error:'邀请码无效'},{status:404});
 await prisma.classMember.upsert({where:{classroomId_userId:{classroomId:classroom.id,userId:user.id}},update:{},create:{classroomId:classroom.id,userId:user.id,memberRole:'STUDENT'}});
 return NextResponse.json({ok:true,classroom:{id:classroom.id,name:classroom.name}});
}
