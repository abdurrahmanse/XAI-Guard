import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("access_token")?.value;
  const isAuthPage = request.nextUrl.pathname.startsWith("/login");
  const isApiAuthRoute = request.nextUrl.pathname.startsWith("/api/auth");

  // Allow next internals and api auth routes
  if (isApiAuthRoute) {
    return NextResponse.next();
  }

  if (!token) {
    if (!isAuthPage) {
      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("next", request.nextUrl.pathname);
      return NextResponse.redirect(loginUrl);
    }
    return NextResponse.next();
  }

  // Token exists - Decode and check expiry
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    const now = Math.floor(Date.now() / 1000);
    
    if (payload.exp && payload.exp < now) {
      // Expired token
      if (!isAuthPage) {
        const loginUrl = new URL("/login", request.url);
        loginUrl.searchParams.set("next", request.nextUrl.pathname);
        const response = NextResponse.redirect(loginUrl);
        response.cookies.delete("access_token");
        return response;
      }
    } else {
      // Valid token
      if (isAuthPage) {
        return NextResponse.redirect(new URL("/", request.url));
      }
    }
  } catch (error) {
    // Malformed token
    if (!isAuthPage) {
      const loginUrl = new URL("/login", request.url);
      const response = NextResponse.redirect(loginUrl);
      response.cookies.delete("access_token");
      return response;
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
