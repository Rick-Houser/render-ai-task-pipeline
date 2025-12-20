import React, { useState } from 'react';
import axios from 'axios';

const App: React.FC = () => {
  const [description, setDescription] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);

  const createTask = async () => {
    try {
      const res = await axios.post('http://localhost:8000/tasks', { description });
      console.log(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  const searchTasks = async () => {
    try {
      const res = await axios.post('http://localhost:8000/query', { question: query });
      setResults(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl">AI Task Manager</h1>
      <input type="text" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Task Description" className="border p-2" />
      <button onClick={createTask} className="bg-blue-500 text-white p-2">Add Task</button>
      <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search Query" className="border p-2 mt-4" />
      <button onClick={searchTasks} className="bg-green-500 text-white p-2">Search</button>
      <ul>{results.map((r, i) => <li key={i}>{r.summary}</li>)}</ul>
    </div>
  );
};

export default App;
