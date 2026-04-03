import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={<div className="p-4 text-2xl font-bold">QuickBite</div>}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
