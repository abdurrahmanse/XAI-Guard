"use client";
import React from "react";
import { LoginForm } from "@xaiguard/ui";

export default function LoginPage() {
  return (
    <div className="flex-1 flex items-center justify-center p-6 bg-muted/20 py-24">
      <LoginForm appName="XAI-Guard Portal" postLoginRoute="http://localhost:3001" />
    </div>
  );
}
