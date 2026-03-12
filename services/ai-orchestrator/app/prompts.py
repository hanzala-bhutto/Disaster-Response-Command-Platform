import json


def build_prompt(*, workflow_type: str, incident: dict, tasks: list[dict], notifications: list[dict], evidence: list[dict], question: str | None) -> str:
    instructions = {
        "triage": "Classify urgency, summarize the situation, identify the first response priorities, and return strict JSON.",
        "response_plan": "Create a grounded response plan using the retrieved evidence and return strict JSON.",
        "public_advisory": "Write a public-facing advisory message plus safety cautions and return strict JSON.",
    }

    return (
        "You are an emergency operations AI assistant.\n"
        f"Workflow: {workflow_type}\n"
        f"Instruction: {instructions[workflow_type]}\n"
        "Return JSON only with keys: summary, response_plan, resource_needs, caution_notes, public_message.\n"
        f"Question: {question or 'Use the incident details and evidence.'}\n"
        f"Incident: {json.dumps(incident)}\n"
        f"Tasks: {json.dumps(tasks)}\n"
        f"Notifications: {json.dumps(notifications)}\n"
        f"Evidence: {json.dumps(evidence)}\n"
    )
