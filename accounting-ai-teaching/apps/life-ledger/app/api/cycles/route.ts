import { NextResponse } from 'next/server';
import { prisma } from '../../../lib/prisma';
import { currentUser } from '../../../lib/auth';
export async function POST(request:Request){
 const user=await currentUser();if(!user||user.role!=='TEACHER')return NextResponse.json({ok:false,error:'仅教师可创建周期'},{status:403});
 const b=await request.json();const member=await prisma.classMember.findUnique({where:{classroomId_userId:{classroomId:b.classroomId,userId:user.id}}});if(!member||member.memberRole!=='OWNER')return NextResponse.json({ok:false,error:'无权管理该班级'},{status:403});
 const cycle=await prisma.learningCycle.create({data:{classroomId:b.classroomId,name:b.name,stage:Number(b.stage||1),startsAt:new Date(b.startsAt),endsAt:new Date(b.endsAt),suggestedCount:Number(b.suggestedCount||3),maxScoredCount:Number(b.maxScoredCount||5)}});return NextResponse.json({ok:true,cycle});
}
