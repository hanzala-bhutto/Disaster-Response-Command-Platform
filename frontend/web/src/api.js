const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Request failed');
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const api = {
  listIncidents: () => request('/incidents'),
  createIncident: (payload) => request('/incidents', { method: 'POST', body: JSON.stringify(payload) }),
  updateIncident: (id, payload) => request(`/incidents/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),
  deleteIncident: (id) => request(`/incidents/${id}`, { method: 'DELETE' }),
  listTasks: () => request('/tasks'),
  createTask: (payload) => request('/tasks', { method: 'POST', body: JSON.stringify(payload) }),
  updateTask: (id, payload) => request(`/tasks/${id}`, { method: 'PATCH', body: JSON.stringify(payload) }),
  deleteTask: (id) => request(`/tasks/${id}`, { method: 'DELETE' }),
  listNotifications: () => request('/notifications'),
  listKnowledgeDocuments: () => request('/knowledge/documents'),
  createKnowledgeDocument: (payload) => request('/knowledge/documents', { method: 'POST', body: JSON.stringify(payload) }),
  searchKnowledge: (payload) => request('/knowledge/search', { method: 'POST', body: JSON.stringify(payload) }),
};
