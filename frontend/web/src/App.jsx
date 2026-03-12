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

const emptyKnowledgeForm = {
  title: '',
  category: 'SOP',
  incident_type: 'flood',
  source: '',
  content: '',
};

const emptySearchForm = {
  query: '',
  incident_type: 'all',
  limit: 5,
};

const emptyAiForm = {
  incident_id: '',
  workflow_type: 'response_plan',
  question: '',
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
    llm: 'bg-violet-100 text-violet-700 ring-violet-200',
    fallback: 'bg-slate-100 text-slate-700 ring-slate-200',
    triage: 'bg-blue-100 text-blue-700 ring-blue-200',
    response_plan: 'bg-emerald-100 text-emerald-700 ring-emerald-200',
    public_advisory: 'bg-amber-100 text-amber-800 ring-amber-200',
  };

  return (
    <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold capitalize ring-1 ${styles[value] ?? 'bg-gray-100 text-gray-700 ring-gray-200'}`}>
      {String(value).replace('_', ' ')}
    </span>
  );
}

function ListBlock({ title, items }) {
  return (
    <div>
      <h4 className="text-sm font-semibold text-slate-800">{title}</h4>
      <ul className="mt-2 space-y-2 text-sm text-slate-700">
        {items.length === 0 ? <li className="text-slate-500">No items returned.</li> : null}
        {items.map((item, index) => (
          <li className="rounded-2xl bg-slate-50 px-4 py-3" key={`${title}-${index}`}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function App() {
  const [incidents, setIncidents] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [workflowRuns, setWorkflowRuns] = useState([]);
  const [latestWorkflowResult, setLatestWorkflowResult] = useState(null);
  const [incidentForm, setIncidentForm] = useState(emptyIncidentForm);
  const [taskForm, setTaskForm] = useState(emptyTaskForm);
  const [knowledgeForm, setKnowledgeForm] = useState(emptyKnowledgeForm);
  const [searchForm, setSearchForm] = useState(emptySearchForm);
  const [aiForm, setAiForm] = useState(emptyAiForm);
  const [loading, setLoading] = useState(true);
  const [aiLoading, setAiLoading] = useState(false);
  const [error, setError] = useState('');

  const incidentOptions = useMemo(
    () => incidents.map((incident) => ({ value: incident.id, label: `${incident.title} - ${incident.location}` })),
    [incidents],
  );

  async function loadData() {
    setLoading(true);
    setError('');

    try {
      const [incidentData, taskData, notificationData, documentData, workflowData] = await Promise.all([
        api.listIncidents(),
        api.listTasks(),
        api.listNotifications(),
        api.listKnowledgeDocuments(),
        api.listAiWorkflowRuns(),
      ]);
      setIncidents(incidentData);
      setTasks(taskData);
      setNotifications(notificationData);
      setDocuments(documentData);
      setWorkflowRuns(workflowData.runs ?? []);
      setLatestWorkflowResult((current) => current ?? workflowData.runs?.[0] ?? null);
      setTaskForm((current) => ({ ...current, incident_id: current.incident_id || incidentData[0]?.id || '' }));
      setAiForm((current) => ({ ...current, incident_id: current.incident_id || incidentData[0]?.id || '' }));
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

  async function handleKnowledgeSubmit(event) {
    event.preventDefault();
    setError('');
    try {
      await api.createKnowledgeDocument(knowledgeForm);
      setKnowledgeForm(emptyKnowledgeForm);
      await loadData();
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  async function handleKnowledgeSearch(event) {
    event.preventDefault();
    setError('');
    try {
      const result = await api.searchKnowledge({
        query: searchForm.query,
        incident_type: searchForm.incident_type === 'all' ? null : searchForm.incident_type,
        limit: Number(searchForm.limit),
      });
      setSearchResults(result.matches);
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  async function handleAiWorkflow(event) {
    event.preventDefault();
    setError('');
    setAiLoading(true);
    try {
      const result = await api.runAiWorkflow({
        incident_id: aiForm.incident_id,
        workflow_type: aiForm.workflow_type,
        question: aiForm.question || null,
      });
      setLatestWorkflowResult(result);
      await loadData();
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setAiLoading(false);
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
          <div className="max-w-4xl">
            <p className="mb-3 inline-flex rounded-full bg-white/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-blue-100">Phase 5 Dashboard</p>
            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">Disaster Response Command Platform</h1>
            <p className="mt-3 text-sm leading-6 text-blue-50 sm:text-base">
              Phase 5 adds AI orchestration. The system gathers incident context, reuses RAG evidence, and produces structured workflow outputs in either real LLM mode or safe fallback mode.
            </p>
          </div>
        </section>

        <div className="grid gap-6 lg:grid-cols-2">
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
            <div className="grid gap-6 lg:grid-cols-[1.1fr_1.4fr]">
              <div>
                <h2 className="text-xl font-semibold text-slate-900">Run AI Workflow</h2>
                <p className="mt-1 text-sm text-slate-500">Choose an incident and a workflow. The orchestrator will collect context, retrieve evidence, and return a structured result.</p>
                <form className="mt-6 space-y-4" onSubmit={handleAiWorkflow}>
                  <div className="space-y-1.5">
                    <label className="text-sm font-medium text-slate-700">Incident</label>
                    <select className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={aiForm.incident_id} onChange={(event) => setAiForm({ ...aiForm, incident_id: event.target.value })}>
                      <option value="">Select an incident</option>
                      {incidentOptions.map((option) => (
                        <option key={option.value} value={option.value}>{option.label}</option>
                      ))}
                    </select>
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-sm font-medium text-slate-700">Workflow</label>
                    <select className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={aiForm.workflow_type} onChange={(event) => setAiForm({ ...aiForm, workflow_type: event.target.value })}>
                      <option value="triage">Triage</option>
                      <option value="response_plan">Response plan</option>
                      <option value="public_advisory">Public advisory</option>
                    </select>
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-sm font-medium text-slate-700">Optional question</label>
                    <textarea rows="4" className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={aiForm.question} onChange={(event) => setAiForm({ ...aiForm, question: event.target.value })} placeholder="Example: What should be the first 30 minutes response plan?" />
                  </div>
                  <button className="rounded-2xl bg-violet-600 px-5 py-3 font-semibold text-white transition hover:bg-violet-700 disabled:cursor-not-allowed disabled:bg-slate-300" type="submit" disabled={!aiForm.incident_id || aiLoading}>
                    {aiLoading ? 'Running workflow...' : 'Run workflow'}
                  </button>
                </form>
              </div>

              <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
                <div className="flex flex-wrap items-center gap-2">
                  <h2 className="text-xl font-semibold text-slate-900">Latest AI Result</h2>
                  {latestWorkflowResult ? <Badge value={latestWorkflowResult.workflow_type} /> : null}
                  {latestWorkflowResult ? <Badge value={latestWorkflowResult.mode} /> : null}
                </div>
                {!latestWorkflowResult ? <p className="mt-4 text-sm text-slate-500">No AI workflow has been run yet.</p> : null}
                {latestWorkflowResult ? (
                  <div className="mt-4 space-y-5">
                    <div>
                      <h3 className="text-sm font-semibold text-slate-800">Summary</h3>
                      <p className="mt-2 rounded-2xl bg-white px-4 py-3 text-sm leading-6 text-slate-700">{latestWorkflowResult.summary}</p>
                    </div>
                    <div className="grid gap-4 lg:grid-cols-2">
                      <ListBlock title="Response Plan" items={latestWorkflowResult.response_plan} />
                      <ListBlock title="Resource Needs" items={latestWorkflowResult.resource_needs} />
                    </div>
                    <ListBlock title="Caution Notes" items={latestWorkflowResult.caution_notes} />
                    <div>
                      <h3 className="text-sm font-semibold text-slate-800">Public Message</h3>
                      <p className="mt-2 rounded-2xl bg-white px-4 py-3 text-sm leading-6 text-slate-700">{latestWorkflowResult.public_message}</p>
                    </div>
                    <div>
                      <h3 className="text-sm font-semibold text-slate-800">Grounding Evidence</h3>
                      <div className="mt-2 space-y-3">
                        {latestWorkflowResult.evidence.length === 0 ? <p className="text-sm text-slate-500">No evidence was retrieved for this run.</p> : null}
                        {latestWorkflowResult.evidence.map((item, index) => (
                          <article className="rounded-2xl bg-white px-4 py-3" key={`${item.document_title}-${index}`}>
                            <div className="flex flex-wrap items-center gap-2">
                              <Badge value={item.incident_type} />
                              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">{item.source}</span>
                              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">Score {item.score.toFixed(3)}</span>
                            </div>
                            <h4 className="mt-3 text-sm font-semibold text-slate-800">{item.document_title}</h4>
                            <p className="mt-2 text-sm leading-6 text-slate-700">{item.text}</p>
                          </article>
                        ))}
                      </div>
                    </div>
                  </div>
                ) : null}
              </div>
            </div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
            <div className="flex items-center justify-between gap-3">
              <div>
                <h2 className="text-xl font-semibold text-slate-900">Workflow History</h2>
                <p className="mt-1 text-sm text-slate-500">Each run shows which workflow was used and whether the output came from the LLM or fallback mode.</p>
              </div>
              <div className="rounded-2xl bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600">{workflowRuns.length} total</div>
            </div>
            {!loading && workflowRuns.length === 0 ? <p className="mt-4 text-sm text-slate-500">No workflow runs yet.</p> : null}
            <div className="mt-6 grid gap-4 lg:grid-cols-2">
              {workflowRuns.map((run) => (
                <article className="rounded-3xl border border-slate-200 bg-slate-50 p-5" key={run.run_id}>
                  <div className="mb-3 flex flex-wrap gap-2">
                    <Badge value={run.workflow_type} />
                    <Badge value={run.mode} />
                  </div>
                  <p className="text-sm leading-6 text-slate-700">{run.summary}</p>
                  <div className="mt-4 flex flex-wrap gap-3">
                    <button className="rounded-2xl bg-violet-100 px-4 py-2 text-sm font-medium text-violet-800 transition hover:bg-violet-200" onClick={() => setLatestWorkflowResult(run)}>
                      View details
                    </button>
                  </div>
                </article>
              ))}
            </div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">Create Incident</h2>
            <p className="mt-1 text-sm text-slate-500">Use this form to add a new disaster event into the system.</p>
            <form className="mt-6 space-y-4" onSubmit={handleIncidentSubmit}>
              <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Title</label><input className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={incidentForm.title} onChange={(event) => setIncidentForm({ ...incidentForm, title: event.target.value })} /></div>
              <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Type</label><select className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={incidentForm.type} onChange={(event) => setIncidentForm({ ...incidentForm, type: event.target.value })}><option value="flood">Flood</option><option value="fire">Fire</option><option value="earthquake">Earthquake</option><option value="storm">Storm</option><option value="heatwave">Heatwave</option><option value="other">Other</option></select></div>
              <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Severity</label><select className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={incidentForm.severity} onChange={(event) => setIncidentForm({ ...incidentForm, severity: event.target.value })}><option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option><option value="critical">Critical</option></select></div>
              <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Location</label><input className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={incidentForm.location} onChange={(event) => setIncidentForm({ ...incidentForm, location: event.target.value })} /></div>
              <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Description</label><textarea rows="4" className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={incidentForm.description} onChange={(event) => setIncidentForm({ ...incidentForm, description: event.target.value })} /></div>
              <button className="rounded-2xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700" type="submit">Create incident</button>
            </form>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">Create Task</h2>
            <p className="mt-1 text-sm text-slate-500">Manually assign an operational task to a response team.</p>
            <form className="mt-6 space-y-4" onSubmit={handleTaskSubmit}>
              <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Incident</label><select className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={taskForm.incident_id} onChange={(event) => setTaskForm({ ...taskForm, incident_id: event.target.value })}><option value="">Select an incident</option>{incidentOptions.map((option) => (<option key={option.value} value={option.value}>{option.label}</option>))}</select></div>
              <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Task title</label><input className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={taskForm.title} onChange={(event) => setTaskForm({ ...taskForm, title: event.target.value })} /></div>
              <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Team</label><input className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={taskForm.team} onChange={(event) => setTaskForm({ ...taskForm, team: event.target.value })} /></div>
              <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Priority</label><select className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={taskForm.priority} onChange={(event) => setTaskForm({ ...taskForm, priority: event.target.value })}><option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option><option value="critical">Critical</option></select></div>
              <button className="rounded-2xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300" type="submit" disabled={!taskForm.incident_id}>Create task</button>
            </form>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
            <div className="grid gap-6 lg:grid-cols-2">
              <div>
                <h2 className="text-xl font-semibold text-slate-900">Add Knowledge Document</h2>
                <p className="mt-1 text-sm text-slate-500">Add SOPs, playbooks, and guidance that the RAG service can chunk and store in Qdrant.</p>
                <form className="mt-6 space-y-4" onSubmit={handleKnowledgeSubmit}>
                  <div className="grid gap-4 sm:grid-cols-2">
                    <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Title</label><input className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={knowledgeForm.title} onChange={(event) => setKnowledgeForm({ ...knowledgeForm, title: event.target.value })} /></div>
                    <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Category</label><input className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={knowledgeForm.category} onChange={(event) => setKnowledgeForm({ ...knowledgeForm, category: event.target.value })} /></div>
                    <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Incident type</label><select className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={knowledgeForm.incident_type} onChange={(event) => setKnowledgeForm({ ...knowledgeForm, incident_type: event.target.value })}><option value="flood">Flood</option><option value="fire">Fire</option><option value="earthquake">Earthquake</option><option value="storm">Storm</option><option value="heatwave">Heatwave</option><option value="other">Other</option></select></div>
                    <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Source</label><input className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={knowledgeForm.source} onChange={(event) => setKnowledgeForm({ ...knowledgeForm, source: event.target.value })} /></div>
                  </div>
                  <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Content</label><textarea rows="8" className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={knowledgeForm.content} onChange={(event) => setKnowledgeForm({ ...knowledgeForm, content: event.target.value })} /></div>
                  <button className="rounded-2xl bg-slate-900 px-5 py-3 font-semibold text-white transition hover:bg-slate-800" type="submit">Add document to knowledge base</button>
                </form>
              </div>

              <div>
                <h2 className="text-xl font-semibold text-slate-900">Search Knowledge Base</h2>
                <p className="mt-1 text-sm text-slate-500">Search for the most relevant chunks that the AI workflows can reuse.</p>
                <form className="mt-6 space-y-4" onSubmit={handleKnowledgeSearch}>
                  <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Query</label><input className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={searchForm.query} onChange={(event) => setSearchForm({ ...searchForm, query: event.target.value })} /></div>
                  <div className="grid gap-4 sm:grid-cols-2">
                    <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Incident type filter</label><select className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={searchForm.incident_type} onChange={(event) => setSearchForm({ ...searchForm, incident_type: event.target.value })}><option value="all">All</option><option value="flood">Flood</option><option value="fire">Fire</option><option value="earthquake">Earthquake</option><option value="storm">Storm</option><option value="heatwave">Heatwave</option><option value="other">Other</option></select></div>
                    <div className="space-y-1.5"><label className="text-sm font-medium text-slate-700">Result limit</label><input type="number" min="1" max="10" className="w-full rounded-2xl border border-slate-300 px-4 py-3 outline-none transition focus:border-blue-500 focus:ring-4 focus:ring-blue-100" value={searchForm.limit} onChange={(event) => setSearchForm({ ...searchForm, limit: event.target.value })} /></div>
                  </div>
                  <button className="rounded-2xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700" type="submit">Search knowledge</button>
                </form>
                <div className="mt-6 space-y-3">
                  {searchResults.length === 0 ? <p className="text-sm text-slate-500">No retrieval results yet.</p> : null}
                  {searchResults.map((result) => (
                    <article className="rounded-2xl border border-slate-200 bg-slate-50 p-4" key={result.id}>
                      <div className="flex flex-wrap items-center gap-2"><Badge value={result.incident_type} /><span className="rounded-full bg-slate-200 px-3 py-1 text-xs font-semibold text-slate-700">Score {result.score.toFixed(3)}</span></div>
                      <h3 className="mt-3 text-base font-semibold text-slate-900">{result.document_title}</h3>
                      <p className="mt-1 text-xs text-slate-500">{result.source} · Chunk {result.chunk_index}</p>
                      <p className="mt-3 text-sm leading-6 text-slate-700">{result.text}</p>
                    </article>
                  ))}
                </div>
              </div>
            </div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
            <div className="flex items-center justify-between gap-3"><div><h2 className="text-xl font-semibold text-slate-900">Knowledge Documents</h2><p className="mt-1 text-sm text-slate-500">These are the documents that have been chunked and indexed for retrieval.</p></div><div className="rounded-2xl bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600">{documents.length} total</div></div>
            {loading ? <p className="mt-4 text-sm text-slate-500">Loading...</p> : null}
            {!loading && documents.length === 0 ? <p className="mt-4 text-sm text-slate-500">No knowledge documents yet.</p> : null}
            <div className="mt-6 grid gap-4 lg:grid-cols-2">
              {documents.map((document) => (
                <article className="rounded-3xl border border-slate-200 bg-slate-50 p-5" key={document.id}><div className="mb-3 flex flex-wrap gap-2"><Badge value={document.incident_type} /><span className="rounded-full bg-slate-200 px-3 py-1 text-xs font-semibold text-slate-700">{document.category}</span><span className="rounded-full bg-slate-200 px-3 py-1 text-xs font-semibold text-slate-700">{document.chunk_count} chunks</span></div><h3 className="text-lg font-semibold text-slate-900">{document.title}</h3><p className="mt-1 text-sm text-slate-500">Source: {document.source}</p><p className="mt-3 text-sm leading-6 text-slate-700">{document.content_preview}...</p></article>
              ))}
            </div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between gap-3"><div><h2 className="text-xl font-semibold text-slate-900">Active Incidents</h2><p className="mt-1 text-sm text-slate-500">Current incidents stored by the incident service.</p></div><div className="rounded-2xl bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600">{incidents.length} total</div></div>
            {loading ? <p className="mt-4 text-sm text-slate-500">Loading...</p> : null}
            {!loading && incidents.length === 0 ? <p className="mt-4 text-sm text-slate-500">No incidents yet.</p> : null}
            <div className="mt-6 space-y-4">{incidents.map((incident) => (<article className="rounded-3xl border border-slate-200 bg-slate-50 p-5" key={incident.id}><div className="mb-3 flex flex-wrap gap-2"><Badge value={incident.severity} /><Badge value={incident.status} /><Badge value={incident.type} /></div><h3 className="text-lg font-semibold text-slate-900">{incident.title}</h3><p className="mt-1 text-sm text-slate-500">{incident.location}</p><p className="mt-3 text-sm leading-6 text-slate-700">{incident.description}</p><div className="mt-4 flex flex-wrap gap-3"><button className="rounded-2xl bg-slate-200 px-4 py-2 text-sm font-medium text-slate-800 transition hover:bg-slate-300" onClick={() => updateIncidentStatus(incident.id, 'in_progress')}>Mark in progress</button><button className="rounded-2xl bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-800 transition hover:bg-emerald-200" onClick={() => updateIncidentStatus(incident.id, 'resolved')}>Resolve</button><button className="rounded-2xl bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700" onClick={() => deleteIncident(incident.id)}>Delete</button></div></article>))}</div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between gap-3"><div><h2 className="text-xl font-semibold text-slate-900">Coordination Tasks</h2><p className="mt-1 text-sm text-slate-500">Tasks owned by the coordination service.</p></div><div className="rounded-2xl bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600">{tasks.length} total</div></div>
            {loading ? <p className="mt-4 text-sm text-slate-500">Loading...</p> : null}
            {!loading && tasks.length === 0 ? <p className="mt-4 text-sm text-slate-500">No tasks yet.</p> : null}
            <div className="mt-6 space-y-4">{tasks.map((task) => (<article className="rounded-3xl border border-slate-200 bg-slate-50 p-5" key={task.id}><div className="mb-3 flex flex-wrap gap-2"><Badge value={task.priority} /><Badge value={task.status} /></div><h3 className="text-lg font-semibold text-slate-900">{task.title}</h3><p className="mt-1 text-sm text-slate-500">Team: {task.team}</p><p className="mt-1 break-all text-xs text-slate-400">Incident ID: {task.incident_id}</p><div className="mt-4 flex flex-wrap gap-3"><button className="rounded-2xl bg-slate-200 px-4 py-2 text-sm font-medium text-slate-800 transition hover:bg-slate-300" onClick={() => updateTaskStatus(task.id, 'in_progress')}>Start</button><button className="rounded-2xl bg-emerald-100 px-4 py-2 text-sm font-medium text-emerald-800 transition hover:bg-emerald-200" onClick={() => updateTaskStatus(task.id, 'done')}>Complete</button><button className="rounded-2xl bg-red-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-red-700" onClick={() => deleteTask(task.id)}>Delete</button></div></article>))}</div>
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:col-span-2">
            <div className="flex items-center justify-between gap-3"><div><h2 className="text-xl font-semibold text-slate-900">Event Notifications</h2><p className="mt-1 text-sm text-slate-500">Notifications created by the notification service from RabbitMQ events.</p></div><div className="rounded-2xl bg-slate-100 px-3 py-2 text-sm font-medium text-slate-600">{notifications.length} total</div></div>
            {!loading && notifications.length === 0 ? <p className="mt-4 text-sm text-slate-500">No notifications yet.</p> : null}
            <div className="mt-6 space-y-3">{notifications.map((notification) => (<article className="rounded-2xl border border-slate-200 bg-slate-50 p-4" key={notification.id}><div className="flex flex-wrap items-center gap-2"><Badge value={notification.level === 'critical' ? 'critical' : notification.level === 'warning' ? 'high' : 'low'} /><span className="rounded-full bg-slate-200 px-3 py-1 text-xs font-semibold text-slate-700">{notification.source_event}</span></div><h3 className="mt-3 text-base font-semibold text-slate-900">{notification.title}</h3><p className="mt-1 text-sm text-slate-600">{notification.message}</p></article>))}</div>
          </section>
        </div>

        {error ? <div className="mt-6 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-red-700">{error}</div> : null}
      </div>
    </div>
  );
}

export default App;
