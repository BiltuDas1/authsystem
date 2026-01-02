import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import Login from "../pages/Login";
import Register from "../pages/Register";
import { Flip, ToastContainer } from "react-toastify";

function AuthRoutes() {
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  params.set("source", "verify-email");

  return (
    <>
      <Routes>
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        <Route
          path="verify-email"
          element={<Navigate to={`/auth/login?${params.toString()}`} replace />}
        />
      </Routes>
      <div>
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
          transition={Flip}
        />
      </div>
    </>
  );
}

export default AuthRoutes;
