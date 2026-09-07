"use client";

import { createContext, useContext, useState, useEffect, type ReactNode } from "react";
import { api } from "@/lib/api";
import type { User } from "@/types";

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (email: string, password: string, tenantSlug: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const savedToken = localStorage.getItem("sigm_token");
    if (savedToken) {
      setToken(savedToken);
      api.get<User>("/auth/users/me", savedToken)
        .then(setUser)
        .catch(() => {
          localStorage.removeItem("sigm_token");
          setToken(null);
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (email: string, password: string, tenantSlug: string) => {
    const result = await api.post<{ access_token: string }>("/auth/login", {
      email,
      password,
      tenant_slug: tenantSlug,
    });
    localStorage.setItem("sigm_token", result.access_token);
    setToken(result.access_token);
    const userData = await api.get<User>("/auth/users/me", result.access_token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem("sigm_token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
