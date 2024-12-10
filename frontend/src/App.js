import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './homePage';
import LoginPage from './loginPage';
import RegisterPage from './registerPage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Routes>
    </Router>
  );
};

export default App;

// import React from 'react';
// import { BrowserRouter, Routes, Route } from 'react-router-dom';
// import StockLookup from './components/stockLookup';

// function App() {
//   return (
//     <BrowserRouter>
//       <div className="App">
//         <Routes>
//           <Route path="/lookup-stock" element={<StockLookup />} />
//         </Routes>
//       </div>
//     </BrowserRouter>
//   );
// }

// export default App;

// import React, { useState } from "react";
// import { Layout, Card, Typography, Row, Col } from "antd";
// import HistoricalData from "./components/historicalData";
// import StockLookup from "./components/stockLookup";
// import BuyStock from "./components/buyStock";
// import SellStock from "./components/sellStock";

// const { Title } = Typography;
// const { Header, Content } = Layout;

// function App() {
//   const [range, setRange] = useState("1d");
//   return (
//     <Layout>
//       <Header>
//       <Title level={2} style={{ color: "white", textAlign: "center", margin: 10 }}>
//           Stock Trading Platform
//         </Title>
//       </Header>
//       <Content style={{ padding: "50px" }}>
//         <Row gutter={[20, 20]}>
//           {/* Stock Lookup */}
//           <Col xs={24} sm={12} lg={12}>
//               <StockLookup />
//           </Col>

//           {/* Historical Data Card */}
//           <Col xs={24} sm={12} lg={12}>
//             <HistoricalData range={range} />
//           </Col>

//           {/* Buy Stock Card */}
//           <Col xs={24} sm={12} lg={12}>
//             <Card title="Buy Stock" bordered>
//               {/* TODO: Add the logic*/}
//               <BuyStock />
//             </Card>
//           </Col>

//           {/* Sell Stock Card */}
//           <Col xs={24} sm={12} lg={12}>
//             <Card title="Sell Stock" bordered>
//               {/* TODO: Add the logic*/}
//               <SellStock />
//             </Card>
//           </Col>
//         </Row>
//       </Content>
//     </Layout>
//   );
// }

// export default App;
