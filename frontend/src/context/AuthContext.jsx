import { createContext, useContext } from "react";

export const AuthContext = createContext(null);

// optional helper hook (nice to use everywhere)
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used inside <AuthProvider />");
  }
  return ctx;
}