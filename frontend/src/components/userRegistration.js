import React, { useState } from "react";

const RegisterPage = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");



  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:3000/create-account", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(data.message); // success message
        setUsername("");
        setEmail("");
        setPassword("");
      } else {
        const errorData = await response.json();
        setMessage(errorData.error); // error message
      }
    } catch (error) {
      console.error("Error:", error);
      setMessage("An error occurred. Please try again.");
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", textAlign: "center", marginTop: "50px" }}>
      <h1 style={{ fontSize: "2.5rem" }}>Stock Trading Application</h1>
      <p style={{ fontSize: "1.5rem", marginBottom: "30px" }}>Log In</p>

      <div>
        <form onSubmit={handleRegister} style={{ display: "inline-block", textAlign: "left" }}>
          <div style={{ marginBottom: "10px" }}>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              style={{
                width: "200px",
                padding: "8px",
                marginBottom: "10px",
                border: "1px solid #ccc",
                borderRadius: "4px",
              }}
              required
            />
          </div>
          <div style={{ marginBottom: "10px" }}>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              style={{
                width: "200px",
                padding: "8px",
                marginBottom: "10px",
                border: "1px solid #ccc",
                borderRadius: "4px",
              }}
              required
            />
          </div>
          <button
            type="submit"
            style={{
              width: "100%",
              padding: "10px",
              backgroundColor: "#007BFF",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            Register
          </button>
        </form>
      </div>
      {message && (
        <p style={{ marginTop: "20px", color: message.includes("error") ? "red" : "green" }}>
          {message}
        </p>
      )}
    </div>
  );
};

export default RegisterPage;
