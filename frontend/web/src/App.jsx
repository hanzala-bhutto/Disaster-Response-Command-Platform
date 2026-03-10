import { useEffect, useMemo, useState } from 'react';
import { api } from './api';

const emptyIncidentForm = {
  title: '',
  type: 'flood',
  severity: 'medium',
  location: '',
  description: '',
};

const emptyTaskForm = {
  incident_id: '',
  title: '',
  team: '',
  priority: 'medium',
};

function Badge({ value }) {
  return <span className={`badge ${value}`}>{value.replace('_', ' ')}</span>;
}

function App() {
  const [incidents, setIncidents] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [incidentForm, setIncidentForm] = useState(emptyIncidentForm);
  const [taskForm, setTaskForm] = useState(emptyTaskForm);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const incidentOptions = useMemo(
    () => incidents.map((incident) => ({ value: incident.id, label: `${incident.title} - ${incident.location}` })),
    [incidents],
  );

  async function loadData() {
    setLoading(true);
    setError('');

    try {
      const [incidentData, taskData] = await Promise.all([api.listIncidents(), api.listTasks()]);
      setIncidents(incidentData);
      setTasks(taskData);
      setTaskForm((current) => ({
        ...current,
        incident_id: current.incident_id || incidentData[0]?.id || '',
      }));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function handleIncidentSubmit(event) {
    event.preventDefault();
    setError('');

    try {
      await api.createIncident(incidentForm);
      setIncidentForm(emptyIncidentForm);
      await loadData();
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  async function handleTaskSubmit(event) {
    event.preventDefault();
    setError('');

    try {
      await api.createTask(taskForm);
      setTaskForm((current) => ({ ...emptyTaskForm, incident_id: current.incident_id }));
      await loadData();
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  async function updateIncidentStatus(incidentId, status) {
    setError('');

    try {
      await api.updateIncident(incidentId, { status });
      await loadData();
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  async function updateTaskStatus(taskId, status) {
    setError('');

    try {
      await api.updateTask(taskId, { status });
      await loadData();
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  async function deleteIncident(incidentId) {
    setError('');

    try {
      await api.deleteIncident(incidentId);
      await loadData();
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  async function deleteTask(taskId) {
    setError('');

    try {
      await api.deleteTask(taskId);
      await loadData();
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  return (
    <div className="app-shell">
      <section className="hero">
        <h1>Disaster Response Command Platform</h1>
        <p>
          Phase 2 dashboard: create incidents, track tasks, and prepare for RabbitMQ, RAG, and AI orchestration.
        </p>
      </section>

      <div className="grid">
        <section className="panel">
          <h2>Create Incident</h2>
          <form className="form-grid" onSubmit={handleIncidentSubmit}>
            <div className="field">
              <label>Title</label>
              <input value={incidentForm.title} onChange={(event) => setIncidentForm({ ...incidentForm, title: event.target.value })} />
            </div>
            <div className="field">
              <label>Type</label>
              <select value={incidentForm.type} onChange={(event) => setIncidentForm({ ...incidentForm, type: event.target.value })}>
                <option value="flood">Flood</option>
                <option value="fire">Fire</option>
                <option value="earthquake">Earthquake</option>
                <option value="storm">Storm</option>
                <option value="heatwave">Heatwave</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div className="field">
              <label>Severity</label>
              <select value={incidentForm.severity} onChange={(event) => setIncidentForm({ ...incidentForm, severity: event.target.value })}>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
            <div className="field">
              <label>Location</label>
              <input value={incidentForm.location} onChange={(event) => setIncidentForm({ ...incidentForm, location: event.target.value })} />
            </div>
            <div className="field">
              <label>Description</label>
              <textarea rows="4" value={incidentForm.description} onChange={(event) => setIncidentForm({ ...incidentForm, description: event.target.value })} />
            </div>
            <div className="actions">
              <button className="primary" type="submit">Create incident</button>
            </div>
          </form>
        </section>

        <section className="panel">
          <h2>Create Task</h2>
          <form className="form-grid" onSubmit={handleTaskSubmit}>
            <div className="field">
              <label>Incident</label>
              <select value={taskForm.incident_id} onChange={(event) => setTaskForm({ ...taskForm, incident_id: event.target.value })}>
                <option value="">Select an incident</option>
                {incidentOptions.map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>
            <div className="field">
              <label>Task title</label>
              <input value={taskForm.title} onChange={(event) => setTaskForm({ ...taskForm, title: event.target.value })} />
            </div>
            <div className="field">
              <label>Team</label>
              <input value={taskForm.team} onChange={(event) => setTaskForm({ ...taskForm, team: event.target.value })} />
            </div>
            <div className="field">
              <label>Priority</label>
              <select value={taskForm.priority} onChange={(event) => setTaskForm({ ...taskForm, priority: event.target.value })}>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
            <div className="actions">
              <button className="primary" type="submit" disabled={!taskForm.incident_id}>Create task</button>
            </div>
          </form>
        </section>

        <section className="panel">
          <h2>Active Incidents</h2>
          {loading ? <p>Loading...</p> : null}
          {!loading && incidents.length === 0 ? <p className="empty">No incidents yet.</p> : null}
          <div className="card-list">
            {incidents.map((incident) => (
              <article className="card" key={incident.id}>
                <div className="badge-row">
                  <Badge value={incident.severity} />
                  <Badge value={incident.status} />
                  <Badge value={incident.type} />
                </div>
                <h3>{incident.title}</h3>
                <p className="meta">{incident.location}</p>
                <p>{incident.description}</p>
                <div className="actions">
                  <button className="secondary" onClick={() => updateIncidentStatus(incident.id, 'in_progress')}>Mark in progress</button>
                  <button className="secondary" onClick={() => updateIncidentStatus(incident.id, 'resolved')}>Resolve</button>
                  <button className="danger" onClick={() => deleteIncident(incident.id)}>Delete</button>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="panel">
          <h2>Coordination Tasks</h2>
          {loading ? <p>Loading...</p> : null}
          {!loading && tasks.length === 0 ? <p className="empty">No tasks yet.</p> : null}
          <div className="card-list">
            {tasks.map((task) => (
              <article className="card" key={task.id}>
                <div className="badge-row">
                  <Badge value={task.priority} />
                  <Badge value={task.status} />
                </div>
                <h3>{task.title}</h3>
                <p className="meta">Team: {task.team}</p>
                <p className="meta">Incident ID: {task.incident_id}</p>
                <div className="actions">
                  <button className="secondary" onClick={() => updateTaskStatus(task.id, 'in_progress')}>Start</button>
                  <button className="secondary" onClick={() => updateTaskStatus(task.id, 'done')}>Complete</button>
                  <button className="danger" onClick={() => deleteTask(task.id)}>Delete</button>
                </div>
              </article>
            ))}
          </div>
        </section>
      </div>

      {error ? <p className="error">{error}</p> : null}
    </div>
  );
}

export default App;
