import React from 'react';
import { format } from 'date-fns';
import './TaskItem.css';

const TaskItem = ({ task, onEdit, onDelete, onStatusChange }) => {
  const getPriorityClass = (priority) => {
    return `priority-${priority}`;
  };

  const getStatusClass = (status) => {
    return `status-${status}`;
  };

  const getCategoryIcon = (category) => {
    const icons = {
      work: '💼',
      personal: '👤',
      shopping: '🛒',
      other: '📋'
    };
    return icons[category] || '📋';
  };

  const handleStatusToggle = () => {
    const newStatus = task.status === 'completed' ? 'pending' : 'completed';
    onStatusChange(task.id, newStatus);
  };

  return (
    <div className={`task-item ${getStatusClass(task.status)}`}>
      <div className="task-checkbox">
        <input
          type="checkbox"
          checked={task.status === 'completed'}
          onChange={handleStatusToggle}
        />
      </div>

      <div className="task-content">
        <div className="task-header">
          <h3 className={task.status === 'completed' ? 'completed' : ''}>
            {getCategoryIcon(task.category)} {task.title}
          </h3>
          <span className={`priority-badge ${getPriorityClass(task.priority)}`}>
            {task.priority}
          </span>
        </div>

        {task.description && (
          <p className="task-description">{task.description}</p>
        )}

        <div className="task-meta">
          <span className="task-category">{task.category}</span>
          {task.due_date && (
            <span className="task-due-date">
              Due: {format(new Date(task.due_date), 'MMM dd, yyyy')}
            </span>
          )}
          <span className="task-created">
            Created: {format(new Date(task.created_at), 'MMM dd, yyyy')}
          </span>
        </div>
      </div>

      <div className="task-actions">
        <button className="btn-icon btn-edit" onClick={() => onEdit(task)} title="Edit">
          ✏️
        </button>
        <button className="btn-icon btn-delete" onClick={() => onDelete(task.id)} title="Delete">
          🗑️
        </button>
      </div>
    </div>
  );
};

export default TaskItem;
