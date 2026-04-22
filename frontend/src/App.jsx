import React, { useState, useEffect } from 'react';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import FilterBar from './components/FilterBar';
import { getTasks, createTask, updateTask, deleteTask, getStats } from './services/api';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [filters, setFilters] = useState({ category: '', status: '' });
  const [stats, setStats] = useState(null);

  // Fetch tasks on component mount and when filters change
  useEffect(() => {
    fetchTasks();
    fetchStats();
  }, [filters]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const params = {};
      if (filters.category) params.category = filters.category;
      if (filters.status) params.status = filters.status;

      const response = await getTasks(params);
      setTasks(response.data);
    } catch (err) {
      setError(err.message || 'Failed to fetch tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await getStats();
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  const handleCreateTask = async (taskData) => {
    try {
      await createTask(taskData);
      setShowForm(false);
      fetchTasks();
      fetchStats();
    } catch (err) {
      alert('Failed to create task: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleUpdateTask = async (taskData) => {
    try {
      await updateTask(editingTask.id, taskData);
      setEditingTask(null);
      setShowForm(false);
      fetchTasks();
      fetchStats();
    } catch (err) {
      alert('Failed to update task: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      await deleteTask(taskId);
      fetchTasks();
      fetchStats();
    } catch (err) {
      alert('Failed to delete task: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  const handleStatusChange = async (taskId, newStatus) => {
    try {
      await updateTask(taskId, { status: newStatus });
      fetchTasks();
      fetchStats();
    } catch (err) {
      alert('Failed to update status: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
  };

  const handleNewTask = () => {
    setEditingTask(null);
    setShowForm(true);
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="container">
          <h1>📝 Task Manager</h1>
          <p>Manage your tasks efficiently</p>
        </div>
      </header>

      <main className="container">
        {!showForm && (
          <div className="action-bar">
            <button className="btn btn-new-task" onClick={handleNewTask}>
              + New Task
            </button>
          </div>
        )}

        {showForm && (
          <TaskForm
            onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
            initialData={editingTask}
            onCancel={handleCancelForm}
          />
        )}

        <FilterBar
          filters={filters}
          onFilterChange={handleFilterChange}
          stats={stats}
        />

        <TaskList
          tasks={tasks}
          loading={loading}
          error={error}
          onEdit={handleEditTask}
          onDelete={handleDeleteTask}
          onStatusChange={handleStatusChange}
        />
      </main>

      <footer className="app-footer">
        <div className="container">
          <p>Built with React + FastAPI + PostgreSQL + Docker</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
