import { Routes, Route } from "react-router-dom";
import AuthRoutes from "./routes/authRoutes";
import PageNotExist from "./pages/error/404";

function App() {
  return (
    <Routes>
      <Route path="/auth/*" element={<AuthRoutes />} />

      {/* 404 Page */}
      <Route path="*" element={<PageNotExist />} />
    </Routes>
  );
}

export default App;
