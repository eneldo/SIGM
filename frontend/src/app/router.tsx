"use client";

import { useAuth } from "@/lib/auth-context";
import LoginPage from "@/features/auth/LoginPage";
import DashboardLayout from "@/features/layout/DashboardLayout";
import DashboardPage from "@/features/dashboard/DashboardPage";
import PlaneacionPage from "@/features/planeacion/PlaneacionPage";
import EjecucionPage from "@/features/ejecucion/EjecucionPage";
import AlertasPage from "@/features/control/AlertasPage";
import ReportesPage from "@/features/reportes/ReportesPage";
import { useState } from "react";

type Page = "dashboard" | "planeacion" | "ejecucion" | "alertas" | "reportes";

export default function AppRouter() {
  const { user, isLoading, login, logout } = useAuth();
  const [currentPage, setCurrentPage] = useState<Page>("dashboard");

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (!user) {
    return <LoginPage onLogin={login} />;
  }

  const renderPage = () => {
    switch (currentPage) {
      case "dashboard":
        return <DashboardPage />;
      case "planeacion":
        return <PlaneacionPage />;
      case "ejecucion":
        return <EjecucionPage />;
      case "alertas":
        return <AlertasPage />;
      case "reportes":
        return <ReportesPage />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <DashboardLayout
      user={user}
      currentPage={currentPage}
      onNavigate={setCurrentPage}
      onLogout={logout}
    >
      {renderPage()}
    </DashboardLayout>
  );
}
