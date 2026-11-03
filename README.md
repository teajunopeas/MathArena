# MathArena

MathArena is a local space for practicing math problems in focused sessions: choose a topic, solve a problem, check an answer, and review the solution.

## Included prototype

- Filters by topic and difficulty.
- Random selection from the filtered problems.
- Numeric answer input with tolerance-based checking.
- A step-by-step solution that can be revealed after an attempt.
- One sample problem written for this prototype; it does not come from an external database.

## Open in VS Code

1. Open the `MathArena` folder in VS Code.
2. Open the Command Palette, run **Tasks: Run Task**, and choose **MathArena: Local server**.
3. Open `http://localhost:8000/src/` in your browser.
4. To stop the server, focus the task terminal and press `Ctrl+C`.

Python 3 must be available as `py` on Windows. No external packages or internet connection are required.

## Structure

- `src/`: prototype web interface.
- `data/problems.json`: problems in JSON format.
- `schemas/problem.schema.json`: proposed schema for each problem.
- `docs/PRODUCTO.md`: product proposal and scope.
- `docs/FLUJO_IMPORTACION.md`: process for adding and classifying sources.
- `.vscode/`: workspace task and settings.

## Current limitations

Answer checking currently supports only numeric answers with a simple absolute tolerance. It does not interpret symbolic expressions, verify proofs, or import content automatically. Topic classification is intended to be assisted and reviewed; see `docs/FLUJO_IMPORTACION.md`.

