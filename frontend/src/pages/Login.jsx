import { useState, useContext } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function Login() {
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      // ✅ IMPORTANT: withCredentials so cookie is stored in browser
      const res = await axios.post(
        "http://localhost:8000/auth/jwt/login",
        formData,
        {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          withCredentials: true,
        }
      );

      // ✅ If backend is cookie-based, token may not exist (204 response)
      console.log("LOGIN STATUS:", res.status);
      console.log("LOGIN DATA:", res.data);

      // ✅ Save only user
      localStorage.setItem("user", JSON.stringify({ email }));
      localStorage.removeItem("token"); // ✅ remove bad token

      login({ email });

      navigate("/home");
    } catch (err) {
      console.log(err);
      setError("Invalid email or password");
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-br from-slate-900 to-indigo-800 text-white">
      <form
        onSubmit={handleSubmit}
        className="bg-white/10 p-8 rounded-xl shadow-xl w-96 backdrop-blur-md"
      >
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>

        {error && <p className="text-red-400 mb-3 text-sm text-center">{error}</p>}

        <input
          type="email"
          placeholder="Email"
          className="w-full mb-4 p-2 rounded bg-white/20 border border-white/30"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full mb-6 p-2 rounded bg-white/20 border border-white/30"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          className="w-full bg-blue-500 hover:bg-blue-600 transition rounded py-2 font-semibold"
        >
          Log In
        </button>
      </form>
    </div>
  );
}