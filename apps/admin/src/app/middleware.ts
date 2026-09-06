import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Stub for JWT Role checking.
  // Analysts are redirected back to the dashboard if they attempt to access /admin
  const token = request.cookies.get('jwt');
  if (token && token.value === 'analyst-role-stub') {
    return NextResponse.redirect(new URL('http://localhost:3001')); // Dashboard URL
  }
  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
}
