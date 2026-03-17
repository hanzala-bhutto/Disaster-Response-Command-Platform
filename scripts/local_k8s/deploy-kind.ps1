param(
    [switch]$SkipBuild,
    [switch]$SkipMonitoring
)

$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$kindConfig = Join-Path $projectRoot 'infra\k8s\kind\cluster.yaml'
$contextName = 'kind-disaster-response'

function Require-Command {
    param([string]$Name)

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

Require-Command kind
Require-Command kubectl
Require-Command docker

Push-Location $projectRoot
try {
    $clusterExists = & kind get clusters | Where-Object { $_ -eq 'disaster-response' }
    if (-not $clusterExists) {
        & kind create cluster --config $kindConfig
    }

    if (-not $SkipBuild) {
        $images = @(
            @{ Name = 'disaster-response/frontend-web:local'; Path = 'frontend/web' },
            @{ Name = 'disaster-response/api-gateway:local'; Path = 'services/api-gateway' },
            @{ Name = 'disaster-response/incident-service:local'; Path = 'services/incident-service' },
            @{ Name = 'disaster-response/coordination-service:local'; Path = 'services/coordination-service' },
            @{ Name = 'disaster-response/notification-service:local'; Path = 'services/notification-service' },
            @{ Name = 'disaster-response/rag-service:local'; Path = 'services/rag-service' },
            @{ Name = 'disaster-response/ai-orchestrator:local'; Path = 'services/ai-orchestrator' },
            @{ Name = 'disaster-response/ingestion-service:local'; Path = 'services/ingestion-service' }
        )

        foreach ($image in $images) {
            docker build -t $image.Name $image.Path
            kind load docker-image $image.Name --name disaster-response
        }
    }

    kubectl config use-context $contextName | Out-Null
    kubectl apply -k infra/k8s/base

    if (-not $SkipMonitoring) {
        kubectl apply -k infra/k8s/monitoring
    }

    Write-Host 'Local Kubernetes deployment completed.'
    Write-Host 'App host: http://disaster.local'
    Write-Host 'Grafana host: http://grafana.disaster.local'
    Write-Host 'Prometheus host: http://prometheus.disaster.local'
}
finally {
    Pop-Location
}
