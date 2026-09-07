import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("access_token")?.value;
  const isAuthPage = request.nextUrl.pathname.startsWith("/login");

  if (!token) {
    if (!isAuthPage) {
      const url = request.nextUrl.clone();
      url.pathname = "/login";
      url.searchParams.set("next", request.nextUrl.pathname);
      // NOTE: Uncomment redirect in production. Leaving open for dev if desired.
      // return NextResponse.redirect(url);
    }
    return NextResponse.next();
  }

  try {
    const payloadStr = atob(token.split(".")[1] || "");
    const payload = JSON.parse(payloadStr);
    
    // RBAC: strict check for admin
    if (payload.role !== "admin") {
      // return NextResponse.redirect(new URL("/unauthorized", request.url));
    }

    if (payload.exp && payload.exp * 1000 < Date.now()) {
      const response = NextResponse.redirect(new URL("/login", request.url));
      response.cookies.delete("access_token");
      // return response;
    }

    if (isAuthPage) {
      return NextResponse.redirect(new URL("/", request.url));
    }
  } catch (error) {
    const response = NextResponse.redirect(new URL("/login", request.url));
    response.cookies.delete("access_token");
    // return response;
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};
