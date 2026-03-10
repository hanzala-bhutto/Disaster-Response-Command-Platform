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
  const styles = {
    low: 'bg-sky-100 text-sky-700 ring-sky-200',
    medium: 'bg-amber-100 text-amber-800 ring-amber-200',
    high: 'bg-red-100 text-red-700 ring-red-200',
    critical: 'bg-rose-100 text-rose-700 ring-rose-200',
    new: 'bg-blue-100 text-blue-700 ring-blue-200',
    in_progress: 'bg-violet-100 text-violet-700 ring-violet-200',
    resolved: 'bg-emerald-100 text-emerald-700 ring-emerald-200',
    todo: 'bg-slate-100 text-slate-700 ring-slate-200',
    done: 'bg-emerald-100 text-emerald-700 ring-emerald-200',
    flood: 'bg-cyan-100 text-cyan-700 ring-cyan-200',
    fire: 'bg-orange-100 text-orange-700 ring-orange-200',
    earthquake: 'bg-stone-100 text-stone-700 ring-stone-200',
    storm: 'bg-indigo-100 text-indigo-700 ring-indigo-200',
    heatwave: 'bg-yellow-100 text-yellow-800 ring-yellow-200',
    other: 'bg-gray-100 text-gray-700 ring-gray-200',
  };

  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold capitalize ring-1 ${styles[value] ?? 'bg-gray-100 text-gray-700 ring-gray-200'}`}
    >
      {value.replace('_', ' ')}
    </span>
  );
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
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <section className="mb-8 overflow-hidden rounded-3xl bg-gradient-to-r from-slate-900 via-blue-900 to-blue-600 px-6 py-8 text-white shadow-2xl shadow-blue-900/10 sm:px-8">
          <div className="max-w-3xl">
            <p className="mb-3 inline-flex rounded-full bg-white/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-blue-100">
              Phase 2 Dashboard
            </p>
            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">Disaster Response Command Platform</h1>
            <p className="mt-3 text-sm leading-6 text-blue-50 sm:text-base">
              Phase 2 dashboard: create incidents, track tasks, and prepare for RabbitMQ, RAG, and AI orchestration.
            </p>
          </div>
        </section>

        <div className="grid gap-6 lg:grid-cols-2">
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">Create Incident</h2>
            <p className="mt-1 text-sm text-slate-500">Use this form to add a new disaster event into the system.</p>
            <form className="mt-6 space-y-4" onSubmit={handleIncidentSubmit}>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-slate-700">Title</label>
                <input
                  className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={incidentForm.title}
                  onChange={(event) => setIncidentForm({ ...incidentForm, title: event.target.value })}
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-slate-700">Type</label>
                <select
                  className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={incidentForm.type}
                  onChange={(event) => setIncidentForm({ ...incidentForm, type: event.target.value })}
                >
                  <option value="flood">Flood</option>
                  <option value="fire">Fire</option>
                  <option value="earthquake">Earthquake</option>
                  <option value="storm">Storm</option>
                  <option value="heatwave">Heatwave</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-slate-700">Severity</label>
                <select
                  className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={incidentForm.severity}
                  onChange={(event) => setIncidentForm({ ...incidentForm, severity: event.target.value })}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-slate-700">Location</label>
                <input
                  className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={incidentForm.location}
                  onChange={(event) => setIncidentForm({ ...incidentForm, location: event.target.value })}
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-slate-700">Description</label>
                <textarea
                  rows="4"
                  className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={incidentForm.description}
                  onChange={(event) => setIncidentForm({ ...incidentForm, description: event.target.value })}
                />
              </div>
              <div className="flex flex-wrap gap-3">
                <button className="rounded-2xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700" type="submit">
                  Create incident
                </button>
              </div>
            </form>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">Create Task</h2>
            <p className="mt-1 text-sm text-slate-500">Manually assign an operational task to a response team.</p>
            <form className="mt-6 space-y-4" onSubmit={handleTaskSubmit}>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-slate-700">Incident</label>
                <select
                  className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={taskForm.incident_id}
                  onChange={(event) => setTaskForm({ ...taskForm, incident_id: event.target.value })}
                >
                  <option value="">Select an incident</option>
                  {incidentOptions.map((option) => (
                    <option key={option.value} value={option.value}>{option.label}</option>
                  ))}
                </select>
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-slate-700">Task title</label>
                <input
                  className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={taskForm.title}
                  onChange={(event) => setTaskForm({ ...taskForm, title: event.target.value })}
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-slate-700">Team</label>
                <input
                  className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={taskForm.team}
                  onChange={(event) => setTaskForm({ ...taskForm, team: event.target.value })}
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-slate-700">Priority</label>
                <select
                  className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100"
                  value={taskForm.priority}
                  onChange={(event) => setTaskForm({ ...taskForm, priority: event.target.value })}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <div className="flex flex-wrap gap-3">
                <button
                  className="rounded-2xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
                  type="submit"
                  disabled={!taskForm.incident_id}
                >
                  Create task
                </button>
              </div>
            </form>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <div>
                <h2 className="text-xl font-semibold text-slate-900">Active Incidents</h2>
                <p className="mt-1 text-sm text-slate-500">Current incidents stored by the incident service.</p>
              </div>
              <div className="rounded-2xl bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600">{incidents.length} total</div>
            </div>
            {loading ? <p className="mt-4 text-sm text-slate-500">Loading...</p> : null}
            {!loading && incidents.length === 0 ? <p className="mt-4 text-sm text-slate-500">No incidents yet.</p> : null}
            <div className="mt-6 space-y-4">
              {incidents.map((incident) => (
                <article className="rounded-3xl border border-slate-200 bg-slate-50 p-5" key={incident.id}>
                  <div className="mb-3 flex flex-wrap gap-2">
                    <Badge value={incident.severity} />
                    <Badge value={incident.status} />
                    <Badge value={incident.type} />
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900">{incident.title}</h3>
                  <p className="mt-1 text-sm text-slate-500">{incident.location}</p>
                  <p className="mt-3 text-sm leading-6 text-slate-700">{incident.description}</p>
                  <div className="mt-4 flex flex-wrap gap-3">
                    <button
                      className="rounded-2xl bg-slate-200 px-4 py-2 text-sm font-medium text-slate-800 transition hover:bg-slate-300"
                      onClick={() => updateIncidentStatus(incident.id, 'in_progress')}
                    >
                      Mark in progress
                    </button>
                    <button
                      className="rounded-2xl bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-800 transition hover:bg-emerald-200"
                      onClick={() => updateIncidentStatus(incident.id, 'resolved')}
                    >
                      Resolve
                    </button>
                    <button
                      className="rounded-2xl bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700"
                      onClick={() => deleteIncident(incident.id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <div>
                <h2 className="text-xl font-semibold text-slate-900">Coordination Tasks</h2>
                <p className="mt-1 text-sm text-slate-500">Tasks owned by the coordination service.</p>
              </div>
              <div className="rounded-2xl bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600">{tasks.length} total</div>
            </div>
            {loading ? <p className="mt-4 text-sm text-slate-500">Loading...</p> : null}
            {!loading && tasks.length === 0 ? <p className="mt-4 text-sm text-slate-500">No tasks yet.</p> : null}
            <div className="mt-6 space-y-4">
              {tasks.map((task) => (
                <article className="rounded-3xl border border-slate-200 bg-slate-50 p-5" key={task.id}>
                  <div className="mb-3 flex flex-wrap gap-2">
                    <Badge value={task.priority} />
                    <Badge value={task.status} />
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900">{task.title}</h3>
                  <p className="mt-1 text-sm text-slate-500">Team: {task.team}</p>
                  <p className="mt-1 break-all text-xs text-slate-400">Incident ID: {task.incident_id}</p>
                  <div className="mt-4 flex flex-wrap gap-3">
                    <button
                      className="rounded-2xl bg-slate-200 px-4 py-2 text-sm font-medium text-slate-800 transition hover:bg-slate-300"
                      onClick={() => updateTaskStatus(task.id, 'in_progress')}
                    >
                      Start
                    </button>
                    <button
                      className="rounded-2xl bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-800 transition hover:bg-emerald-200"
                      onClick={() => updateTaskStatus(task.id, 'done')}
                    >
                      Complete
                    </button>
                    <button
                      className="rounded-2xl bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700"
                      onClick={() => deleteTask(task.id)}
                    >
                      Delete
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </section>
        </div>

        {error ? (
          <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
            {error}
          </div>
        ) : null}
      </div>
    </div>
  );
}

export default App;
