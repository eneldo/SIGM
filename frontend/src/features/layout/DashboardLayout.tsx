"use client";

import { type ReactNode } from "react";
import {
  LayoutDashboard,
  FileText,
  Briefcase,
  AlertTriangle,
  BarChart3,
  LogOut,
  Building2,
  Bell,
} from "lucide-react";
import type { User } from "@/types";
import { cn } from "@/lib/utils";

interface DashboardLayoutProps {
  user: User;
  currentPage: string;
  onNavigate: (page: any) => void;
  onLogout: () => void;
  children: ReactNode;
}

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "planeacion", label: "Planeación", icon: FileText },
  { id: "ejecucion", label: "Ejecución", icon: Briefcase },
  { id: "alertas", label: "Alertas", icon: AlertTriangle },
  { id: "reportes", label: "Reportes", icon: BarChart3 },
];

export default function DashboardLayout({
  user,
  currentPage,
  onNavigate,
  onLogout,
  children,
}: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="fixed inset-y-0 left-0 w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <Building2 className="h-8 w-8 text-primary-600" />
            <div>
              <h1 className="font-bold text-gray-900">SIGM</h1>
              <p className="text-xs text-gray-500">Gestión Municipal</p>
            </div>
          </div>
        </div>

        <nav className="flex-1 p-3 space-y-1">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={cn(
                "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                currentPage === item.id
                  ? "bg-primary-50 text-primary-700"
                  : "text-gray-600 hover:bg-gray-100"
              )}
            >
              <item.icon className="h-5 w-5" />
              {item.label}
            </button>
          ))}
        </nav>

        <div className="p-3 border-t border-gray-200">
          <div className="flex items-center gap-3 px-3 py-2">
            <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-700 font-medium text-sm">
              {user.nombre_completo.charAt(0)}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {user.nombre_completo}
              </p>
              <p className="text-xs text-gray-500 truncate">{user.email}</p>
            </div>
          </div>
          <button
            onClick={onLogout}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-gray-600 hover:bg-gray-100 mt-1"
          >
            <LogOut className="h-5 w-5" />
            Cerrar sesión
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="ml-64 p-6">
        <header className="mb-6 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 capitalize">{currentPage}</h2>
          </div>
          <div className="flex items-center gap-4">
            <button className="relative p-2 text-gray-500 hover:text-gray-700">
              <Bell className="h-5 w-5" />
              <span className="absolute top-1 right-1 h-2 w-2 bg-red-500 rounded-full" />
            </button>
          </div>
        </header>
        {children}
      </main>
    </div>
  );
}
