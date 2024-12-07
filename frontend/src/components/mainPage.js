import React from "react";
import { useNavigate } from "react-router-dom";

const MainPage = () => {
  const navigate = useNavigate();

  return (
    <div style={{ fontFamily: "Arial, sans-serif", textAlign: "center", marginTop: "100px" }}>
      <h1 style={{ fontSize: "3rem", marginBottom: "40px" }}>Welcome to Stock Trading Application</h1>
      <div>
        <button
          onClick={() => navigate("/login")}
          style={{
            padding: "10px 20px",
            fontSize: "1rem",
            margin: "10px",
            backgroundColor: "#007BFF",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Login
        </button>
        <button
          onClick={() => navigate("/register")}
          style={{
            padding: "10px 20px",
            fontSize: "1rem",
            margin: "10px",
            backgroundColor: "#28a745",
            color: "white",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Register
        </button>
      </div>
    </div>
  );
};

export default MainPage;
