const topicFilter = document.querySelector("#topic-filter");
const difficultyFilter = document.querySelector("#difficulty-filter");
const statement = document.querySelector("#problem-statement");
const topicList = document.querySelector("#topic-list");
const badge = document.querySelector("#difficulty-badge");
const number = document.querySelector("#problem-number");
const count = document.querySelector("#problem-count");
const answerForm = document.querySelector("#answer-form");
const answerInput = document.querySelector("#answer-input");
const feedback = document.querySelector("#feedback");
const solution = document.querySelector("#solution");
const solutionToggle = document.querySelector("#solution-toggle");
let problems = [];
let currentProblem = null;
let previousId = null;

const difficultyNames = {
  beginner: "Beginner",
  intermediate: "Intermediate",
  advanced: "Advanced"
};

async function loadProblems() {
  try {
    const response = await fetch("../data/problems.json");
    if (!response.ok) throw new Error("Could not load the problem catalog.");
    problems = await response.json();
    const topics = [...new Set(problems.flatMap((problem) => problem.topics))].sort((a, b) => a.localeCompare(b, "en"));
    for (const topic of topics) {
      const option = document.createElement("option");
      option.value = topic;
      option.textContent = topic[0].toLocaleUpperCase("en") + topic.slice(1);
      topicFilter.append(option);
    }
    showNextProblem();
  } catch (error) {
    statement.textContent = `${error.message} Start the local server from the VS Code task.`;
    document.querySelector("#next-button").disabled = true;
  }
}

function filteredProblems() {
  return problems.filter((problem) => {
    const topicMatches = topicFilter.value === "all" || problem.topics.includes(topicFilter.value);
    const difficultyMatches = difficultyFilter.value === "all" || problem.difficulty === difficultyFilter.value;
    return topicMatches && difficultyMatches;
  });
}

function showNextProblem() {
  const available = filteredProblems();
  count.textContent = `${available.length} ${available.length === 1 ? "problem" : "problems"}`;
  feedback.textContent = "";
  feedback.classList.remove("error");
  answerInput.value = "";
  solution.hidden = true;
  solutionToggle.textContent = "Show solution ↗";
  if (!available.length) {
    currentProblem = null;
    statement.textContent = "There are no problems for these filters yet.";
    topicList.replaceChildren();
    badge.textContent = "";
    number.textContent = "CATALOG";
    return;
  }
  const candidates = available.length > 1 ? available.filter((problem) => problem.id !== previousId) : available;
  currentProblem = candidates[Math.floor(Math.random() * candidates.length)];
  previousId = currentProblem.id;
  number.textContent = `PROBLEM · ${String(problems.indexOf(currentProblem) + 1).padStart(2, "0")}`;
  statement.textContent = currentProblem.statement;
  badge.textContent = difficultyNames[currentProblem.difficulty] ?? currentProblem.difficulty;
  topicList.replaceChildren(...currentProblem.topics.map((topic) => {
    const tag = document.createElement("span");
    tag.className = "topic";
    tag.textContent = topic;
    return tag;
  }));
  renderSolution();
}

function renderSolution() {
  const steps = document.createElement("ol");
  for (const step of currentProblem.solution_steps) {
    const item = document.createElement("li");
    item.textContent = step;
    steps.append(item);
  }
  const answer = document.createElement("p");
  answer.className = "solution-answer";
  answer.textContent = `Answer: ${currentProblem.answer.display}`;
  solution.replaceChildren(steps, answer);
}

answerForm.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!currentProblem) return;
  if (currentProblem.answer.type !== "numeric") {
    feedback.textContent = "This answer type still requires manual review.";
    feedback.classList.add("error");
    return;
  }
  const submitted = Number(answerInput.value.trim().replace(",", "."));
  if (!answerInput.value.trim() || !Number.isFinite(submitted)) {
    feedback.textContent = "Enter a number to check your answer.";
    feedback.classList.add("error");
    return;
  }
  const difference = Math.abs(submitted - currentProblem.answer.value);
  if (difference <= (currentProblem.answer.tolerance ?? 0)) {
    feedback.textContent = "Correct! Nicely done.";
    feedback.classList.remove("error");
  } else {
    feedback.textContent = "That does not match yet. Review your steps and try again.";
    feedback.classList.add("error");
  }
});

solutionToggle.addEventListener("click", () => {
  if (!currentProblem) return;
  solution.hidden = !solution.hidden;
  solutionToggle.textContent = solution.hidden ? "Show solution ↗" : "Hide solution ↗";
});
document.querySelector("#next-button").addEventListener("click", showNextProblem);
topicFilter.addEventListener("change", showNextProblem);
difficultyFilter.addEventListener("change", showNextProblem);
loadProblems();

