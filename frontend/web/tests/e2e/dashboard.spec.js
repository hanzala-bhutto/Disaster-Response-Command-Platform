import { expect, test } from '@playwright/test';

function createInitialState() {
  const incidents = [
    {
      id: 'incident-1',
      title: 'River overflow near central bridge',
      type: 'flood',
      severity: 'high',
      location: 'Zone A',
      description: 'Water level is rising and nearby streets are partially blocked.',
      status: 'new',
      created_at: '2026-03-18T10:00:00Z',
    },
  ];

  const tasks = [
    {
      id: 'task-1',
      incident_id: 'incident-1',
      title: 'Review flood response for Zone A',
      team: 'Operations',
      priority: 'high',
      status: 'todo',
      created_at: '2026-03-18T10:05:00Z',
    },
  ];

  const notifications = [
    {
      id: 'notification-1',
      incident_id: 'incident-1',
      task_id: null,
      title: 'New incident received',
      message: 'River overflow near central bridge reported at Zone A',
      level: 'warning',
      source_event: 'incident.created',
      created_at: '2026-03-18T10:06:00Z',
    },
  ];

  const documents = [
    {
      id: 'document-1',
      title: 'Flood Response Quick Guide',
      category: 'SOP',
      incident_type: 'flood',
      source: 'Sample Manual',
      content_preview: 'When flooding is reported, first confirm affected zones and blocked roads.',
      chunk_count: 3,
      created_at: '2026-03-18T10:10:00Z',
    },
  ];

  const workflowRuns = [
    {
      run_id: 'run-1',
      incident_id: 'incident-1',
      workflow_type: 'response_plan',
      mode: 'fallback',
      summary: 'Initial response plan generated for the active flood incident.',
      response_plan: ['Confirm impact area', 'Dispatch operations team'],
      resource_needs: ['Operations lead', 'Field response team'],
      caution_notes: ['Validate flood depth before vehicle dispatch'],
      public_message: 'Emergency teams are responding to flooding in Zone A.',
      evidence: [
        {
          document_title: 'Flood Response Quick Guide',
          source: 'Sample Manual',
          incident_type: 'flood',
          chunk_index: 0,
          text: 'Prioritize evacuation for low-lying areas and communicate shelter locations.',
          score: 0.92,
        },
      ],
      created_at: '2026-03-18T10:12:00Z',
    },
  ];

  return { incidents, tasks, notifications, documents, workflowRuns };
}

async function registerApiMocks(page) {
  const state = createInitialState();

  await page.route('**/incidents', async (route) => {
    const method = route.request().method();
    if (method === 'GET') {
      await route.fulfill({ json: state.incidents });
      return;
    }

    if (method === 'POST') {
      const payload = route.request().postDataJSON();
      const newIncident = {
        id: `incident-${state.incidents.length + 1}`,
        status: 'new',
        created_at: '2026-03-18T12:00:00Z',
        ...payload,
      };
      state.incidents.unshift(newIncident);
      await route.fulfill({ status: 201, json: newIncident });
      return;
    }

    await route.fallback();
  });

  await page.route('**/tasks', async (route) => {
    const method = route.request().method();
    if (method === 'GET') {
      await route.fulfill({ json: state.tasks });
      return;
    }

    if (method === 'POST') {
      const payload = route.request().postDataJSON();
      const newTask = {
        id: `task-${state.tasks.length + 1}`,
        status: 'todo',
        created_at: '2026-03-18T12:05:00Z',
        ...payload,
      };
      state.tasks.unshift(newTask);
      await route.fulfill({ status: 201, json: newTask });
      return;
    }

    await route.fallback();
  });

  await page.route('**/notifications', async (route) => {
    await route.fulfill({ json: state.notifications });
  });

  await page.route('**/knowledge/documents', async (route) => {
    const method = route.request().method();
    if (method === 'GET') {
      await route.fulfill({ json: state.documents });
      return;
    }

    if (method === 'POST') {
      const payload = route.request().postDataJSON();
      const newDocument = {
        id: `document-${state.documents.length + 1}`,
        title: payload.title,
        category: payload.category,
        incident_type: payload.incident_type,
        source: payload.source,
        content_preview: payload.content.slice(0, 160),
        chunk_count: 2,
        created_at: '2026-03-18T12:10:00Z',
      };
      state.documents.unshift(newDocument);
      await route.fulfill({ status: 201, json: newDocument });
      return;
    }

    await route.fallback();
  });

  await page.route('**/knowledge/search', async (route) => {
    const payload = route.request().postDataJSON();
    await route.fulfill({
      json: {
        query: payload.query,
        matches: [
          {
            id: 'match-1',
            document_id: 'document-1',
            document_title: 'Flood Response Quick Guide',
            incident_type: payload.incident_type ?? 'flood',
            source: 'Sample Manual',
            chunk_index: 0,
            text: 'Prioritize evacuation for low-lying areas and communicate shelter locations.',
            score: 0.91,
          },
        ],
      },
    });
  });

  await page.route('**/ai/workflows/run', async (route) => {
    const payload = route.request().postDataJSON();
    const result = {
      run_id: `run-${state.workflowRuns.length + 1}`,
      incident_id: payload.incident_id,
      workflow_type: payload.workflow_type,
      mode: 'fallback',
      summary: 'Automated response plan generated from mocked evidence.',
      response_plan: ['Confirm incident scope', 'Coordinate field response'],
      resource_needs: ['Operations lead', 'Comms support'],
      caution_notes: ['Validate field conditions before dispatch'],
      public_message: 'Emergency teams are responding and more information will follow.',
      evidence: [
        {
          document_title: 'Flood Response Quick Guide',
          source: 'Sample Manual',
          incident_type: 'flood',
          chunk_index: 0,
          text: 'Prioritize evacuation for low-lying areas and communicate shelter locations.',
          score: 0.94,
        },
      ],
      created_at: '2026-03-18T12:15:00Z',
    };
    state.workflowRuns.unshift(result);
    await route.fulfill({ json: result });
  });

  await page.route('**/ai/workflow-runs', async (route) => {
    await route.fulfill({ json: { runs: state.workflowRuns } });
  });
}

test.beforeEach(async ({ page }) => {
  await registerApiMocks(page);
});

test('loads the command dashboard with seeded data', async ({ page }) => {
  await page.goto('/');

  const incidentsSection = page.locator('section').filter({ has: page.getByRole('heading', { name: 'Active Incidents' }) });
  const tasksSection = page.locator('section').filter({ has: page.getByRole('heading', { name: 'Coordination Tasks' }) });
  const notificationsSection = page.locator('section').filter({ has: page.getByRole('heading', { name: 'Event Notifications' }) });

  await expect(page.getByRole('heading', { name: 'Disaster Response Command Platform' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Active Incidents' })).toBeVisible();
  await expect(incidentsSection.getByRole('heading', { name: 'River overflow near central bridge' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Coordination Tasks' })).toBeVisible();
  await expect(tasksSection.getByRole('heading', { name: 'Review flood response for Zone A' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Event Notifications' })).toBeVisible();
  await expect(notificationsSection.getByRole('heading', { name: 'New incident received' })).toBeVisible();
});

test('creates a new incident through the form', async ({ page }) => {
  await page.goto('/');

  const incidentSection = page.locator('section').filter({ has: page.getByRole('heading', { name: 'Create Incident' }) });
  const incidentsListSection = page.locator('section').filter({ has: page.getByRole('heading', { name: 'Active Incidents' }) });

  await incidentSection.locator('input').nth(0).fill('Wildfire near the northern ridge');
  await incidentSection.locator('input').nth(1).fill('Zone C');
  await incidentSection.locator('textarea').fill('Smoke is moving toward nearby homes.');
  await incidentSection.getByRole('button', { name: 'Create incident' }).click();

  await expect(incidentsListSection.getByRole('heading', { name: 'Wildfire near the northern ridge' })).toBeVisible();
  await expect(incidentsListSection.getByText('Zone C', { exact: true })).toBeVisible();
});

test('runs the AI workflow and shows the latest result', async ({ page }) => {
  await page.goto('/');

  const latestResultSection = page.locator('section').filter({ has: page.getByRole('heading', { name: 'Run AI Workflow' }) });

  await page.getByRole('button', { name: 'Run workflow' }).click();

  await expect(page.getByRole('heading', { name: 'Latest AI Result' })).toBeVisible();
  await expect(latestResultSection.getByText('Automated response plan generated from mocked evidence.')).toBeVisible();
  await expect(latestResultSection.getByText('Confirm incident scope')).toBeVisible();
  await expect(latestResultSection.getByText('Emergency teams are responding and more information will follow.')).toBeVisible();
});
