# Frontend Web

## What this service does
This is the React dashboard for disaster operators.

## Inputs
- incidents
- tasks
- notifications
- AI results

## Outputs
- dashboard views
- forms for creating incidents
- AI assistant interactions

## Main pages
- dashboard
- incident detail
- tasks
- AI assistant
- document upload

## How to run locally
1. install dependencies with `npm install`
2. start the app with `npm run dev`
3. set `VITE_API_BASE_URL` if the gateway runs on a different URL
4. Tailwind CSS is configured through the Vite plugin
5. for Kubernetes, build the container image from `Dockerfile`

## Automated tests
Phase 8 adds Playwright-based browser tests for the dashboard.

Run the test suite with:
1. `npm run test:e2e`
2. `npm run test:e2e:headed` for a visible browser
3. `npm run test:e2e:ui` for the Playwright UI runner

The current tests mock API responses so they can validate frontend workflows without requiring the backend services, Kafka, or Kubernetes to be running.

## Included in the current UI
- incident creation form
- task creation form
- incident list
- task list
- simple status updates
- AI workflow panel
- RAG document upload and search

## Container port
- `80`
