# Proposed workflow for importing and classifying problems

## 1. Register a source before importing

Record the name, URL or reference, access date, format, terms of use/license, redistribution permission, and required attribution. If the license or permission is unclear, keep only a reference for personal use and do not copy the content into a shareable catalog until the question is resolved.

## 2. Keep an input copy

Keep the source file unedited in an input area identified by source and date. Record a checksum and original filename once the production workflow is implemented. The normalized copy should be traceable back to that input.

## 3. Normalize to the shared model

Convert each record to the schema in `schemas/problem.schema.json`. Preserve the text, language, source, license, and any available solution. Do not invent a missing solution. Mark incomplete fields as pending.

## 4. Detect duplicates

Compare source identifiers and normalized statement fingerprints. Send approximate matches for review; similar-looking problems may have different conditions.

## 5. Suggest tags

Use the agreed taxonomy (for example, calculus > integration > substitution). Store suggested tags separately from confirmed tags, along with the method/model, version, and confidence. The initial version can be tagged manually.

## 6. Review a sample and measure reliability

Create a human-labeled reference set. Measure precision, recall, F1, and the confusion matrix for each topic. Keep evaluation data separate from data used to tune the classifier. Inspect errors and uncovered cases.

Do not set a universal threshold in advance: choose it based on the cost of an incorrect tag in an exam-preparation filter. Send low-confidence suggestions or high-impact topics for manual review. Record who confirmed or corrected a tag and when.

## 7. Publish to the catalog

Include only records with documented sources and rights, stable identifiers, and an explicit review status. Keep records traceable so an entry can be updated or removed if the source or its terms change.

## Suggested statuses

`imported` → `normalized` → `needs_review` → `verified` → `published`.

A tag should also have its own status (`suggested`, `confirmed`, `corrected`) so the quality of the problem statement is not confused with the quality of its classification.

