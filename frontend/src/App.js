import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { DataIngestionProvider } from './services/DataIngestionContext';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import DataForm from './pages/DataForm';
import DataViewer from './pages/DataViewer';
import DebugPanel from './components/DebugPanel';
import './App.css';

function App() {
  return (
    <DataIngestionProvider>
      <Router>
        <div className="App">
          <Header />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/ingest" element={<DataForm />} />
              <Route path="/view" element={<DataViewer />} />
            </Routes>
          </main>
          <DebugPanel />
        </div>
      </Router>
    </DataIngestionProvider>
  );
}

export default App;
