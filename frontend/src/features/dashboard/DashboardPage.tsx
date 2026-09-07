"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { DashboardResumen } from "@/types";
import { FolderOpen, Target, Briefcase, FileText, AlertTriangle, TrendingUp } from "lucide-react";
import { formatNumber } from "@/lib/utils";

export default function DashboardPage() {
  const { token } = useAuth();
  const [data, setData] = useState<DashboardResumen | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      api.get<DashboardResumen>("/planeacion/dashboard", token)
        .then(setData)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [token]);

  if (loading) {
    return <div className="animate-pulse space-y-4">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="h-32 bg-gray-200 rounded-xl" />
      ))}
    </div>;
  }

  if (!data) return <p className="text-gray-500">No se pudo cargar el dashboard</p>;

  const stats = [
    { label: "Planes de Acción", value: data.total_planes, icon: FolderOpen, color: "text-blue-600 bg-blue-100" },
    { label: "Metas", value: data.total_metas, icon: Target, color: "text-green-600 bg-green-100" },
    { label: "Proyectos", value: data.total_proyectos, icon: Briefcase, color: "text-purple-600 bg-purple-100" },
    { label: "Contratos", value: data.total_contratos, icon: FileText, color: "text-orange-600 bg-orange-100" },
    { label: "Metas con Avance", value: data.metas_con_avance, icon: TrendingUp, color: "text-teal-600 bg-teal-100" },
    { label: "Alertas Abiertas", value: data.alertas_abiertas, icon: AlertTriangle, color: "text-red-600 bg-red-100" },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="card p-6">
            <div className="flex items-center gap-4">
              <div className={`p-3 rounded-lg ${stat.color}`}>
                <stat.icon className="h-6 w-6" />
              </div>
              <div>
                <p className="text-sm text-gray-500">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900">{formatNumber(stat.value)}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Resumen del Sistema</h3>
        <p className="text-gray-600">
          SIGM Colombia está operativo. El sistema tiene{" "}
          <strong>{data.total_metas} metas</strong> registradas,{" "}
          <strong>{data.total_proyectos} proyectos</strong> en ejecución, y{" "}
          <strong>{data.alertas_abiertas} alertas</strong> abiertas que requieren atención.
        </p>
      </div>
    </div>
  );
}
