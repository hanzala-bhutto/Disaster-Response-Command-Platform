from __future__ import annotations

import compileall
import sys
from pathlib import Path

SERVICE_DIRS = [
    Path('services/ai-orchestrator/app'),
    Path('services/api-gateway/app'),
    Path('services/coordination-service/app'),
    Path('services/incident-service/app'),
    Path('services/ingestion-service/app'),
    Path('services/notification-service/app'),
    Path('services/rag-service/app'),
]


def main() -> int:
    missing_paths = [str(path) for path in SERVICE_DIRS if not path.exists()]
    if missing_paths:
        print('Missing service directories:')
        for path in missing_paths:
            print(f' - {path}')
        return 1

    failed_paths: list[str] = []

    for path in SERVICE_DIRS:
        print(f'Validating {path} ...')
        ok = compileall.compile_dir(path, quiet=1, force=True)
        if not ok:
            failed_paths.append(str(path))

    if failed_paths:
        print('Python validation failed for:')
        for path in failed_paths:
            print(f' - {path}')
        return 1

    print('Python service validation passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
