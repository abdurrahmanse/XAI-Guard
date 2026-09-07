"use client";
import React from "react";
import { LoginForm } from "@xaiguard/ui";

export default function LoginPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-muted/20 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-[300px] bg-gradient-to-b from-primary/5 to-transparent pointer-events-none" />
      <LoginForm appName="XAI-Guard Admin Console" postLoginRoute="/models" />
    </div>
  );
}
