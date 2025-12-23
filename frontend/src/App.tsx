import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';

const App: React.FC = () => {
  const [description, setDescription] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [isAdding, setIsAdding] = useState(false);
  const [isSearching, setIsSearching] = useState(false);

  // Use production API URL
  const API_BASE_URL = 'https://api-zqmv.onrender.com';

  const createTask = async () => {
    if (!description.trim()) return;

    setIsAdding(true);
    try {
      const res = await axios.post(`${API_BASE_URL}/tasks`, { description });
      console.log(res.data);
      setDescription(''); // Clear input after successful creation
    } catch (error) {
      console.error('Error creating task:', error);
    } finally {
      setIsAdding(false);
    }
  };

  const searchTasks = async () => {
    if (!query.trim()) return;

    setIsSearching(true);
    try {
      const res = await axios.post(`${API_BASE_URL}/query`, { question: query });
      setResults(res.data);
    } catch (error) {
      console.error('Error searching tasks:', error);
      setResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent, action: () => void) => {
    if (e.key === 'Enter') {
      action();
    }
  };

  const getPriorityBadge = (priority: string) => {
    const colors: Record<string, string> = {
      High: 'bg-red-100 text-red-800',
      Medium: 'bg-yellow-100 text-yellow-800',
      Low: 'bg-green-100 text-green-800'
    };
    return `px-2 py-1 text-xs rounded-full ${colors[priority] || 'bg-gray-100 text-gray-800'}`;
  };

  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="w-full max-w-sm sm:max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">AI Task Manager</h1>
          <p className="text-gray-600 text-sm">Create and search tasks with AI-powered insights</p>
        </div>

        {/* Add Task Card */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Add a New Task</h2>
          <div className="space-y-3">
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              onKeyPress={(e) => handleKeyPress(e, createTask)}
              placeholder="Enter task description..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              disabled={isAdding}
            />
            <button
              onClick={createTask}
              disabled={isAdding || !description.trim()}
              className="w-full bg-blue-800 hover:bg-blue-900 disabled:bg-blue-300 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center"
            >
              {isAdding ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
              ) : null}
              Add Task
            </button>
          </div>
        </div>

        {/* Search Card */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Search Tasks</h2>
          <div className="space-y-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => handleKeyPress(e, searchTasks)}
              placeholder="Ask a question about your tasks..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all"
              disabled={isSearching}
            />
            <button
              onClick={searchTasks}
              disabled={isSearching || !query.trim()}
              className="w-full bg-emerald-700 hover:bg-emerald-800 disabled:bg-emerald-300 disabled:cursor-not-allowed text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center"
            >
              {isSearching ? (
                <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
              ) : null}
              Search
            </button>
          </div>
        </div>

        {/* Results */}
        {results.length > 0 && (
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Results ({results.length})</h2>
            <div className="space-y-4">
              {results.map((task) => (
                <div key={task.id} className="border p-4 rounded-lg">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-medium">{task.description}</h3>
                    <span className={getPriorityBadge(task.priority)}>{task.priority}</span>
                  </div>
                  <div className="text-gray-600 prose prose-sm max-w-none">
                    <ReactMarkdown>{task.summary}</ReactMarkdown>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Loading indicator for search */}
        {isSearching && results.length === 0 && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 text-center">
            <div className="flex items-center justify-center">
              <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mr-3"></div>
              <span className="text-gray-600">Processing...</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
