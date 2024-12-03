import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import StockLookup from './components/stockLookup';

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path="/lookup-stock" element={<StockLookup />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
