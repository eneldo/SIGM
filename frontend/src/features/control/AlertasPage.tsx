"use client";

import { useEffect, useState, useCallback } from "react";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { AlertaGestion } from "@/types";
import { formatDate, getEstadoBadgeClass } from "@/lib/utils";
import { AlertTriangle, CheckCircle, XCircle } from "lucide-react";

const severidadColors: Record<string, string> = {
  INFO: "bg-blue-100 text-blue-800",
  BAJA: "bg-green-100 text-green-800",
  MEDIA: "bg-yellow-100 text-yellow-800",
  ALTA: "bg-orange-100 text-orange-800",
  CRITICA: "bg-red-100 text-red-800",
};

export default function AlertasPage() {
  const { token } = useAuth();
  const [alertas, setAlertas] = useState<AlertaGestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [filtro, setFiltro] = useState("ABIERTA");

  const loadAlertas = useCallback(() => {
    if (token) {
      api.get<AlertaGestion[]>(`/planeacion/alertas?estado=${filtro}`, token ?? undefined)
        .then(setAlertas)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [token, filtro]);

  useEffect(() => { loadAlertas(); }, [token, filtro, loadAlertas]);

  const atender = async (id: string) => {
    await api.post(`/planeacion/alertas/${id}/atender`, {}, token ?? undefined);
    loadAlertas();
  };

  const cerrar = async (id: string) => {
    await api.post(`/planeacion/alertas/${id}/cerrar`, {}, token ?? undefined);
    loadAlertas();
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 border-b border-gray-200 pb-2">
          {["ABIERTA", "ATENDIDA", "CERRADA"].map((estado) => (
            <button
              key={estado}
              onClick={() => setFiltro(estado)}
              className={`px-4 py-2 text-sm font-medium rounded-t-lg ${
                filtro === estado
                  ? "bg-primary-50 text-primary-700 border-b-2 border-primary-600"
                  : "text-gray-500"
              }`}
            >
              {estado}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-24 bg-gray-100 rounded-xl animate-pulse" />
          ))}
        </div>
      ) : alertas.length === 0 ? (
        <div className="card p-12 text-center">
          <CheckCircle className="mx-auto h-12 w-12 text-green-300" />
          <p className="mt-4 text-gray-500">No hay alertas {filtro.toLowerCase()}</p>
        </div>
      ) : (
        <div className="space-y-3">
          {alertas.map((alerta) => (
            <div key={alerta.id} className="card p-5">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="h-5 w-5 text-orange-500 mt-0.5" />
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-medium text-gray-900">{alerta.tipo}</h3>
                      <span className={`badge ${severidadColors[alerta.severidad] || "bg-gray-100"}`}>
                        {alerta.severidad}
                      </span>
                      <span className={`badge ${getEstadoBadgeClass(alerta.estado)}`}>
                        {alerta.estado}
                      </span>
                    </div>
                    <p className="mt-1 text-sm text-gray-600">{alerta.mensaje}</p>
                    <p className="mt-1 text-xs text-gray-400">
                      {alerta.entidad_tipo} | {formatDate(alerta.fecha_generacion)}
                    </p>
                  </div>
                </div>
                {alerta.estado === "ABIERTA" && (
                  <div className="flex gap-2">
                    <button onClick={() => atender(alerta.id)} className="btn-secondary text-xs">
                      Atender
                    </button>
                    <button onClick={() => cerrar(alerta.id)} className="btn-danger text-xs">
                      Cerrar
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
