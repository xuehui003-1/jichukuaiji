import {NextResponse} from 'next/server';
import {currentUser} from '../../../lib/auth';
import {prisma} from '../../../lib/prisma';

export async function GET(){
 const u=await currentUser();
 if(!u)return NextResponse.json({ok:false,error:'请先登录'},{status:401});
 if(u.role==='TEACHER'){
  const records=await prisma.aILiteracyAttempt.findMany({orderBy:{createdAt:'desc'},take:200,include:{student:{select:{displayName:true,username:true}}}});
  const safe=records.map(x=>({...x,student:{displayName:x.student.displayName.slice(0,1)+'同学',username:x.student.username.replace(/.(?=.{2})/g,'*')}}));
  return NextResponse.json({ok:true,role:'TEACHER',records:safe});
 }
 const records=await prisma.aILiteracyAttempt.findMany({where:{studentId:u.id},orderBy:{createdAt:'desc'},take:30});
 return NextResponse.json({ok:true,role:'STUDENT',records});
}

export async function POST(req:Request){
 const u=await currentUser();
 if(!u||u.role!=='STUDENT')return NextResponse.json({ok:false,error:'请使用学生账号登录'},{status:403});
 const b=await req.json();
 const record=await prisma.aILiteracyAttempt.create({data:{studentId:u.id,taskType:String(b.kind),title:String(b.title),firstAnswerJson:JSON.stringify(b.firstAnswer||{}),firstScore:Number(b.firstScore)||0,diagnosisJson:JSON.stringify(b.tags||[]),revisedAnswerJson:JSON.stringify(b.revisedAnswer||{}),revisedScore:Number(b.revisedScore)||0,revisionNote:String(b.revisionNote||''),status:'REVISED'}});
 return NextResponse.json({ok:true,id:record.id});
}

export async function PATCH(req:Request){
 const u=await currentUser();
 if(!u||u.role!=='TEACHER')return NextResponse.json({ok:false,error:'仅教师可复核'},{status:403});
 const b=await req.json();
 await prisma.aILiteracyAttempt.update({where:{id:String(b.id)},data:{status:b.action==='RETURNED'?'RETURNED':'REVIEWED',teacherNote:String(b.teacherNote||''),reviewedAt:new Date()}});
 return NextResponse.json({ok:true});
}
