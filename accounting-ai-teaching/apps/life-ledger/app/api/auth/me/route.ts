import { NextResponse } from 'next/server';
import { currentUser } from '../../../../lib/auth';
export async function GET(){const user=await currentUser();return NextResponse.json(user?{ok:true,user:{id:user.id,username:user.username,displayName:user.displayName,role:user.role}}:{ok:false},{status:user?200:401})}
