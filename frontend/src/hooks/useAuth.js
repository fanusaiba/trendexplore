import { useContext } from "react";
import { AuthContext } from "../hooks/useAuth";

export const useAuth = () => {
  return useContext(AuthContext);
};
