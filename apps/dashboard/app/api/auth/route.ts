import { NextResponse } from "next/server";
import { cookies } from "next/headers";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    
    // Call the Python FastAPI backend
    const apiRes = await fetch(`${apiUrl}/v1/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      // OAuth2PasswordRequestForm expects form-urlencoded
      body: new URLSearchParams({
        username: body.username,
        password: body.password,
      }),
    });

    if (!apiRes.ok) {
      return NextResponse.json(
        { error: "Invalid credentials" },
        { status: 401 }
      );
    }

    const data = await apiRes.json();
    
    // Set the JWT cookie
    const cookieStore = await cookies();
    cookieStore.set({
      name: "access_token",
      value: data.access_token,
      httpOnly: true,
      path: "/",
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 60 * 60 * 24, // 1 day
    });

    return NextResponse.json({ success: true });
  } catch (error: any) {
    return NextResponse.json(
      { error: "Internal server error: " + error.message },
      { status: 500 }
    );
  }
}

export async function GET() {
  return new Response("Auth API");
}
