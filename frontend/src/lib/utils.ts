import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("es-CO").format(value);
}

export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("es-CO", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function getEstadoBadgeClass(estado: string): string {
  const map: Record<string, string> = {
    ACTIVO: "bg-green-100 text-green-800",
    ACTIVA: "bg-green-100 text-green-800",
    FORMULACION: "bg-yellow-100 text-yellow-800",
    BORRADOR: "bg-gray-100 text-gray-800",
    APROBADO: "bg-blue-100 text-blue-800",
    EJECUCION: "bg-blue-100 text-blue-800",
    CERRADO: "bg-gray-100 text-gray-800",
    SUSPENDIDO: "bg-red-100 text-red-800",
    PENDIENTE: "bg-yellow-100 text-yellow-800",
    EN_EJECUCION: "bg-blue-100 text-blue-800",
    CUMPLIDA: "bg-green-100 text-green-800",
    VENCIDA: "bg-red-100 text-red-800",
    CANCELADA: "bg-red-100 text-red-800",
    PLANEADO: "bg-gray-100 text-gray-800",
    TERMINADO: "bg-green-100 text-green-800",
    LIQUIDADO: "bg-gray-100 text-gray-800",
    ABIERTA: "bg-red-100 text-red-800",
    ATENDIDA: "bg-yellow-100 text-yellow-800",
  };
  return map[estado] || "bg-gray-100 text-gray-800";
}
