# MathArena — goal and proposed deliverable

## Project goal

MathArena will be a personal application for continuously practicing university-level mathematics problems in a focused, distraction-free environment. Problems can come from different sources, be organized by subject and topic, and be solved inside the application. The user can save their attempts and personal solutions.

The project is also a way to learn programming. Most of the project-specific logic —the problem model, importing, classification, filters, practice sessions, and saving attempts— will be built step by step. Libraries will be used for specialized infrastructure that is not the learning goal, such as SQLite for persistence and, later, a library for rendering LaTeX.

## Proposed minimum deliverable

A local MathArena prototype, developed progressively, that allows the user to:

1. Add problems from one or more identified sources.
2. Convert them to a shared internal format while preserving provenance, license, language, and available metadata.
3. Organize and filter the catalog by subject, topic, and, when possible, level.
4. Display a problem in a clean practice screen with text input and visual support for mathematical notation/LaTeX.
5. Save the user's written solution and review previous attempts.
6. Show an official solution or explanation when the source provides one.

The initial goal is to **practice and save one's own work**, not to automatically determine whether a free-form proof is correct. The first deliverable can use a small set of problems, even if added manually, to learn and validate the workflow before automating more sources.

## First-version scope

- A local, personal-use application.
- A catalog stored in SQLite.
- A shared model for problems, topics, sources, and personal solutions/attempts.
- Incremental importing: start with one source and add adapters once the basic workflow works.
- Subject/topic filters and problem selection.
- A text response editor, with mathematical rendering in the interface when that feature is added.
- Saving and retrieving personal attempts.
- Source, license/attribution, and review-status tracking.
- Human review for solutions and tags whose reliability has not been confirmed.

## Out of scope for the minimum version

- Automatic evaluation of mathematical proofs.
- Automatic partial credit for free-form answers.
- Formalization or systematic checking with Lean 4.
- Multiplayer, rankings, accounts, or online synchronization.
- Importing large collections without checking rights, structure, and quality.

## Learning approach and technology

The application should teach useful programming concepts without requiring the user to rebuild generic infrastructure. The user wants to develop MathArena's own logic and decisions; using an existing database such as SQLite is a sensible choice. Python can be used for the model, importers, and application logic; FastAPI could be introduced when it makes sense to separate the interface from data operations through an API.

Suggested learning order:

1. Python basics: types, conditionals, loops, functions, and modules.
2. Read and validate JSON files and understand exceptions.
3. Query SQLite from Python and design simple tables and relationships.
4. Separate code into functions/modules for the catalog, importing, and practice.
5. Build an importer for one specific source format.
6. Add a web interface and, when useful, FastAPI as an API between the interface and application logic.
7. Add mathematical rendering or specialized evaluation libraries as needed.

There is no need to master the entire list before starting: each step can be implemented when the prototype needs it.

## Sources, importing, and classification

Sources may use different formats and may not be written in Python. MathArena should convert each format through an adapter into its shared model. When importing, preserve the original identifier and source reference, and check what the specific license allows before copying or redistributing content.

Tags help find problems from a syllabus, but should not be treated as correct just because a classifier suggested them. Start with a small taxonomy and manual/reviewed tags; later, measure automatic classification against a human-labeled reference set. See `FLUJO_IMPORTACION.md`.

## Future ideas — exploratory, not committed

These ideas may become expansions if the core practice experience proves useful:

- **Answer checking by type:** start with numeric answers using a tolerance; later explore fractions, equivalent expressions, and other formats. Each type needs an explicit criterion and test examples.
- **Partial credit:** later, use step-based rubrics or reviewable criteria for problems designed for them. Do not assign arbitrary scores to free-form proofs.
- **Lean 4:** explore formalization and verification of selected results once the problem model is stable and there is a clear need.
- **Versus mode:** two participants solve the same problem or a comparable round. Correctness should matter more than speed; treat time and hints as secondary factors. This requires a sufficiently large catalog, suitable checkers, and balanced rules.
- **Game interference:** explore brief, announced, reversible effects. One experiment idea was to visually change some operators for a few seconds. This is not a decided feature; it should not silently alter submitted text or prevent solving.
- **Missions, streaks, or topic challenges:** possible game layers over individual practice, without replacing the mathematical goal.
- **Concept library:** link problems to related definitions and theorems and let users consult them from the solving session, ideally in a side panel that keeps the problem in view. Later, concepts could form a central catalog linked to each other and to problems. The source and review status of each definition/theorem should also be recorded.

Before developing competitive mechanics, try them in paper rounds or a small prototype. Observe whether players understand the rules, feel the game is fair, experience interruptions, and want to play again. Compare a baseline round with one that adds a single mechanic to distinguish excitement from friction.

## Minimum-deliverable acceptance criteria

- A small set of problems can be loaded with documented sources and rights.
- Records are normalized to the MathArena model and can be filtered by topic.
- The screen supports focused work and lets the user write a solution.
- Attempts can be saved and reviewed later.
- Solutions published by the source are distinguished from user-written solutions.
- The system does not claim to verify a proof when it has only stored or displayed it.
- Documentation makes clear which parts are implemented and which remain future ideas.

