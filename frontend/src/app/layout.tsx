import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SIGM Colombia",
  description: "Sistema Integral de Gestión Municipal",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
