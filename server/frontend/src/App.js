import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";  // Importa il componente di registrazione
import { Routes, Route } from "react-router-dom";
import Dealers from './components/Dealers/Dealers';

function App() {
  return (
    <Routes>
      {/* Rotta per il login */}
      <Route path="/login" element={<LoginPanel />} />
      {/* Rotta per la registrazione */}
      <Route path="/register" element={<Register />} />
      {/* Rotta per i concessionari */}
      <Route path="/dealers" element={<Dealers/>} />
    </Routes>
  );
}

export default App;
