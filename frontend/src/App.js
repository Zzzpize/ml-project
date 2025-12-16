import React, { useState, useEffect } from 'react';
import './App.css';
import HistorySidebar from './components/HistorySidebar';
import TicketForm from './components/TicketForm';
import ResultDisplay from './components/ResultDisplay';
import { predictTicket } from './services/apiService';

function App() {
  const [history, setHistory] = useState([]);
  const [currentResult, setCurrentResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    try {
      const storedHistory = localStorage.getItem('ticketHistory');
      if (storedHistory) {
        setHistory(JSON.parse(storedHistory));
      }
    } catch (e) {
      console.error("Failed to parse history from localStorage", e);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('ticketHistory', JSON.stringify(history));
  }, [history]);

  const handleFormSubmit = async (subject, description) => {
    setIsLoading(true);
    setError('');
    setCurrentResult(null);

    try {
      const result = await predictTicket(subject, description);

      const formattedResult = {
        equipment: result.equipment,
        failure_point: result.failure_point,
        serial_number: result.serial_number
      };
      setCurrentResult(formattedResult);

      const newHistoryItem = { subject, description, result: formattedResult };
      setHistory(prevHistory => [newHistoryItem, ...prevHistory]);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <HistorySidebar history={history} />
      <main className="main-content">
        <h1 className="main-title">Автоматическая диспетчеризация заявок</h1>
        <p className="main-subtitle">Введите данные заявки, и система определит проблему</p>
        <TicketForm onSubmit={handleFormSubmit} isLoading={isLoading} />

        {isLoading && <div className="spinner"></div>}
        {error && <div className="error-message">{error}</div>}
        {currentResult && <ResultDisplay result={currentResult} />}
      </main>
    </div>
  );
}

export default App;