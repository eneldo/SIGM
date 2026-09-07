"use client";

import { AuthProvider } from "@/lib/auth-context";
import AppRouter from "./router";

export default function Home() {
  return (
    <AuthProvider>
      <AppRouter />
    </AuthProvider>
  );
}
