import { NextResponse } from 'next/server'
import { NextRequest } from 'next/server'

// This function runs on the Node.js runtime
export function middleware(request: NextRequest) {
  const token = request.cookies.get('next-auth.session-token') || 
               request.cookies.get('__Secure-next-auth.session-token')
  
  const isLoggedIn = !!token
  const { pathname } = request.nextUrl
  
  // Allow access to auth routes and static files
  if (
    pathname.startsWith('/api/auth') ||
    pathname.includes('.') ||
    pathname.startsWith('/_next/') ||
    pathname === '/auth/signin'
  ) {
    return NextResponse.next()
  }

  // If user is not logged in and trying to access protected route
  if (!isLoggedIn) {
    const callbackUrl = encodeURIComponent(pathname + request.nextUrl.search)
    return NextResponse.redirect(
      new URL(`/auth/signin?callbackUrl=${callbackUrl}`, request.nextUrl.origin)
    )
  }

  return NextResponse.next()
}

// Only run middleware on specific paths
export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|api/auth).*)',
  ],
}
