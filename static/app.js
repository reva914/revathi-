// Maps the selected task -> { endpoint, field name FastAPI expects, placeholder, label }
const TASK_CONFIG = {
  qa: {
    endpoint: "/qa",
    field: "question",
    label: "Your question:",
    placeholder: "e.g. Which is the largest ocean?",
  },
  explain: {
    endpoint: "/explain",
    field: "topic",
    label: "Topic to explain:",
    placeholder: "e.g. quantum computing",
  },
  quiz: {
    endpoint: "/quiz",
    field: "passage",
    label: "Topic or passage to quiz on:",
    placeholder: "e.g. The Pythagoras Theorem",
  },
  summarize: {
    endpoint: "/summarize",
    field: "content",
    label: "Content to summarize:",
    placeholder: "Paste a long paragraph here...",
  },
  learn: {
    endpoint: "/learn/recommendations",
    field: "topic",
    label: "Topic you want a learning path for:",
    placeholder: "e.g. SQL",
  },
};

const taskSelect = document.getElementById("task");
const inputLabel = document.getElementById("input-label");
const userInput = document.getElementById("user-input");
const form = document.getElementById("edugenie-form");
const submitBtn = document.getElementById("submit-btn");
const loadingEl = document.getElementById("loading");
const resultArea = document.getElementById("result-area");

// Update label/placeholder whenever the task changes
taskSelect.addEventListener("change", () => {
  const cfg = TASK_CONFIG[taskSelect.value];
  inputLabel.textContent = cfg.label;
  userInput.placeholder = cfg.placeholder;
  resultArea.innerHTML = "";
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const task = taskSelect.value;
  const cfg = TASK_CONFIG[task];
  const value = userInput.value.trim();

  if (!value) {
    resultArea.innerHTML = `<div class="error-box">Please enter something before submitting.</div>`;
    return;
  }

  const formData = new FormData();
  formData.append(cfg.field, value);

  setLoading(true);
  resultArea.innerHTML = "";

  try {
    const res = await fetch(cfg.endpoint, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    renderResult(task, data.result);
  } catch (err) {
    resultArea.innerHTML = `<div class="error-box">Request failed: ${err}</div>`;
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  loadingEl.classList.toggle("hidden", !isLoading);
  submitBtn.disabled = isLoading;
}

function renderResult(task, result) {
  if (task === "quiz") {
    renderQuiz(result);
    return;
  }

  // result may be a plain string, or an {error: "..."} object for any module
  if (result && typeof result === "object" && result.error) {
    resultArea.innerHTML = `<div class="error-box">${escapeHtml(result.error)}</div>`;
    return;
  }

  resultArea.innerHTML = `<div class="result-box">${escapeHtml(String(result))}</div>`;
}

function renderQuiz(result) {
  if (!Array.isArray(result)) {
    const message = (result && result.error) ? result.error : "Could not generate a quiz.";
    resultArea.innerHTML = `<div class="error-box">${escapeHtml(message)}</div>`;
    return;
  }

  resultArea.innerHTML = "";
  result.forEach((q, qIndex) => {
    const qDiv = document.createElement("div");
    qDiv.className = "quiz-question";

    const optionsHtml = q.options
      .map(
        (opt, i) => `
        <label class="quiz-option">
          <input type="radio" name="quiz-${qIndex}" value="${i}"> ${escapeHtml(opt)}
        </label>`
      )
      .join("");

    qDiv.innerHTML = `
      <h4>Q${qIndex + 1}. ${escapeHtml(q.question)}</h4>
      ${optionsHtml}
      <div class="quiz-feedback" id="feedback-${qIndex}"></div>
    `;
    resultArea.appendChild(qDiv);
  });

  const checkBtn = document.createElement("button");
  checkBtn.type = "button";
  checkBtn.textContent = "Check Answers";
  checkBtn.onclick = () => checkQuizAnswers(result);
  resultArea.appendChild(checkBtn);
}

function checkQuizAnswers(questions) {
  questions.forEach((q, qIndex) => {
    const selected = document.querySelector(`input[name="quiz-${qIndex}"]:checked`);
    const feedbackEl = document.getElementById(`feedback-${qIndex}`);

    if (!selected) {
      feedbackEl.textContent = "Please select an option.";
      feedbackEl.className = "quiz-feedback";
      return;
    }

    const isCorrect = parseInt(selected.value, 10) === q.answer_index;
    if (isCorrect) {
      feedbackEl.textContent = "✔ Correct!";
      feedbackEl.className = "quiz-feedback correct";
    } else {
      const correctText = q.options[q.answer_index];
      feedbackEl.textContent = `✘ Incorrect. Correct answer: ${correctText}`;
      feedbackEl.className = "quiz-feedback incorrect";
    }
  });
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}