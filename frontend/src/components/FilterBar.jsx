import React from 'react';
import './FilterBar.css';

const FilterBar = ({ filters, onFilterChange, stats }) => {
  return (
    <div className="filter-bar">
      <div className="filter-section">
        <label>Category:</label>
        <select
          value={filters.category}
          onChange={(e) => onFilterChange('category', e.target.value)}
        >
          <option value="">All Categories</option>
          <option value="work">💼 Work</option>
          <option value="personal">👤 Personal</option>
          <option value="shopping">🛒 Shopping</option>
          <option value="other">📋 Other</option>
        </select>
      </div>

      <div className="filter-section">
        <label>Status:</label>
        <select
          value={filters.status}
          onChange={(e) => onFilterChange('status', e.target.value)}
        >
          <option value="">All Status</option>
          <option value="pending">⏳ Pending</option>
          <option value="in_progress">🔄 In Progress</option>
          <option value="completed">✅ Completed</option>
        </select>
      </div>

      {stats && (
        <div className="stats-section">
          <div className="stat">
            <span className="stat-label">Total:</span>
            <span className="stat-value">{stats.total_tasks}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Pending:</span>
            <span className="stat-value pending">{stats.by_status.pending}</span>
          </div>
          <div className="stat">
            <span className="stat-label">In Progress:</span>
            <span className="stat-value progress">{stats.by_status.in_progress}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Completed:</span>
            <span className="stat-value completed">{stats.by_status.completed}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterBar;
