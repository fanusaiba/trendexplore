import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

export default function Profile() {
  const { user } = useContext(AuthContext);

  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-br from-slate-900 to-indigo-800 text-white">
      <div className="bg-white/10 p-8 rounded-xl w-96 backdrop-blur-md text-center">
        <h2 className="text-2xl font-bold mb-4">Profile</h2>
        <p className="mb-2">Email:</p>
        <p className="font-semibold text-lg">{user?.email}</p>
      </div>
    </div>
  ); 
}