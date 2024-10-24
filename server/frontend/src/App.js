import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";  // Importa il componente di registrazione
import { Routes, Route } from "react-router-dom";
import Dealers from './components/Dealers/Dealers';
import Dealer from "./components/Dealers/Dealer";
import PostReview from "./components/Dealers/PostReview"

function App() {
  return (
    <Routes>
      {/* Rotta per il login */}
      <Route path="/login" element={<LoginPanel />} />
      {/* Rotta per la registrazione */}
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealers/>} />
      <Route path="/dealer/:id" element={<Dealer/>} />   
      <Route path="/postreview/:id" element={<PostReview/>} />
    </Routes>
  );
}

export default App;
