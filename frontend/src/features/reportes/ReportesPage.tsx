"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { ReporteAvanceMeta } from "@/types";
import { formatNumber } from "@/lib/utils";
import { BarChart3 } from "lucide-react";

export default function ReportesPage() {
  const { token } = useAuth();
  const [reportes, setReportes] = useState<ReporteAvanceMeta[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      api.get<ReporteAvanceMeta[]>("/planeacion/reportes/avance-metas", token)
        .then(setReportes)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [token]);

  return (
    <div className="space-y-6">
      <div className="card p-6">
        <div className="flex items-center gap-3 mb-4">
          <BarChart3 className="h-6 w-6 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-900">Reporte de Avance por Meta</h3>
        </div>

        {loading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-20 bg-gray-100 rounded-lg animate-pulse" />
            ))}
          </div>
        ) : reportes.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No hay datos de avance disponibles</p>
        ) : (
          <div className="space-y-4">
            {reportes.map((r) => (
              <div key={r.meta_id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-sm text-primary-600">{r.meta_codigo}</span>
                      <span className="text-sm font-medium text-gray-900">{r.meta_descripcion}</span>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      Unidad: {r.unidad_medida} | Meta cuatrienio: {formatNumber(r.meta_cuatrienio)}
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold text-gray-900">{formatNumber(r.valor_avance)}</p>
                    <p className="text-xs text-gray-500">de {formatNumber(r.meta_cuatrienio)}</p>
                  </div>
                </div>

                {/* Progress bar */}
                <div className="mt-3">
                  <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                    <span>Avance</span>
                    <span>{r.porcentaje_avance ?? 0}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 h-2 rounded-full transition-all"
                      style={{ width: `${Math.min(r.porcentaje_avance ?? 0, 100)}%` }}
                    />
                  </div>
                </div>

                {/* Programación anual */}
                {r.programacion.length > 0 && (
                  <div className="mt-3 flex gap-2 flex-wrap">
                    {r.programacion.map((p) => (
                      <span key={p.vigencia} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                        {p.vigencia}: {formatNumber(p.valor)}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
