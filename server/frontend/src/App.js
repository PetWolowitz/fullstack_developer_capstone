import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";  // Importa il componente di registrazione
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      {/* Rotta per il login */}
      <Route path="/login" element={<LoginPanel />} />
      {/* Rotta per la registrazione */}
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}

export default App;
