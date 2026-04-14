import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Navigate,
  useNavigate,
} from "react-router-dom";
import { useContext } from "react";
import Home from "./pages/Home.jsx";
import Chat from "./pages/Chat.jsx";
import Compare from "./pages/Compare.jsx";
import Login from "./pages/Login.jsx";
import Signup from "./pages/Signup.jsx";
import AuthProvider from "./context/AuthProvider";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthContext } from "./context/AuthContext";
import Profile from "./pages/Profile.jsx";


function AppContent() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-indigo-900 text-white">

      <nav className="bg-white/10 backdrop-blur-md shadow-md p-4 flex justify-between items-center rounded-xl mx-6 my-4">
        <h1 className="text-2xl font-bold text-blue-300">
          TrendExplore 🌍
        </h1>

        <div className="space-x-4">

          {user && (
            <>
              <Link to="/home" className="hover:text-blue-400">Home</Link>
              <Link to="/compare" className="hover:text-blue-400">Compare</Link>
              <Link to="/chat" className="hover:text-blue-400">Chat</Link>

              <button
                onClick={handleLogout}
                className="bg-red-500 px-3 py-1 rounded hover:bg-red-600 transition"
              >
                Logout
              </button>
            </>
          )}

          {!user && (
            <>
              <Link to="/login" className="hover:text-blue-400">Login</Link>
              <Link to="/signup" className="hover:text-blue-400">Signup</Link>
            </>
          )}

        </div>
      </nav>

      <Routes>

        <Route path="/" element={<Navigate to="/login" />} />

        {/* Public */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Protected */}
        <Route
          path="/home"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />

        <Route
          path="/compare"
          element={
            <ProtectedRoute>
              <Compare />
            </ProtectedRoute>
          }
        />

        <Route
          path="/chat"
          element={
            <ProtectedRoute>
              <Chat />
            </ProtectedRoute>
          }
        />
        

      </Routes>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}
