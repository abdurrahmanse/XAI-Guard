"use client";
import React from "react";
import { SignupForm } from "@xaiguard/ui";

export default function SignupPage() {
  return (
    <div className="flex-1 flex items-center justify-center p-4 sm:p-6 bg-muted/20 py-12 sm:py-24">
      <SignupForm appName="XAI-Guard Enterprise" />
    </div>
  );
}
