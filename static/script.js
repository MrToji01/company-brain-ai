const form = document.getElementById("questionForm");
const input = document.getElementById("questionInput");
const chat = document.getElementById("chat");
const sendButton = document.getElementById("sendButton");
const hero = document.getElementById("hero");
const suggestions = document.getElementById("suggestions");
const connectionStatus = document.getElementById("connectionStatus");
const statusDot = document.querySelector(".status-line i");

const originalSendButtonHTML = sendButton.innerHTML;

// Fill the question box when a suggestion is clicked.
function useQuestion(question) {
  input.value = question;
  input.focus();
  input.setSelectionRange(input.value.length, input.value.length);
}

// Start a new conversation in the frontend.
function clearChat() {
  chat.replaceChildren();
  hero.hidden = false;
  suggestions.hidden = false;
  input.value = "";
  input.focus();
}

// Add a user or AI message to the chat.
function addMessage(role, text, isError = false) {
  const card = document.createElement("article");
  card.className =
    "message " + (role === "You" ? "user" : "assistant");

  const header = document.createElement("div");
  header.className = "message-header";

  const avatar = document.createElement("span");
  avatar.className = "avatar";
  avatar.textContent = role === "You" ? "Y" : "CB";

  const label = document.createElement("span");
  label.textContent = role;

  header.append(avatar, label);

  const body = document.createElement("div");
  body.className = "message-body" + (isError ? " error" : "");
  body.textContent = text;

  card.append(header, body);
  chat.append(card);

  card.scrollIntoView({
    behavior: "smooth",
    block: "nearest"
  });

  return { card, body };
}

// Display graph evidence returned by the backend.
function addEvidence(card, evidence) {
  if (!Array.isArray(evidence) || evidence.length === 0) {
    return;
  }

  const details = document.createElement("details");
  details.className = "evidence-details";

  const summary = document.createElement("summary");
  summary.textContent =
    `Evidence trail (${evidence.length} record${evidence.length === 1 ? "" : "s"})`;

  const pre = document.createElement("pre");
  pre.className = "evidence-content";
  pre.textContent = JSON.stringify(evidence, null, 2);

  details.append(summary, pre);
  card.append(details);
}

// Check that the server returned JSON.
async function readJsonResponse(response) {
  const contentType = response.headers.get("content-type") || "";

  if (!contentType.includes("application/json")) {
    throw new Error(
      `Server returned a non-JSON response (HTTP ${response.status}). ` +
      "Run python web_app.py and open http://127.0.0.1:5000."
    );
  }

  return response.json();
}

// Check the Flask backend and FalkorDB connection.
async function checkBackend() {
  connectionStatus.textContent = "Checking backend...";
  statusDot.classList.remove("online");

  try {
    const response = await fetch("/health", {
      method: "GET",
      headers: { Accept: "application/json" },
      cache: "no-store"
    });

    const data = await readJsonResponse(response);

    if (!response.ok || data.status !== "ok") {
      throw new Error(
        data.message || `Health check failed (HTTP ${response.status})`
      );
    }

    const nodeText =
      data.nodes !== undefined ? ` Graph nodes: ${data.nodes}.` : "";

    connectionStatus.textContent =
      `Connected to Flask backend.${nodeText}`;

    statusDot.classList.add("online");
  } catch (error) {
    connectionStatus.textContent =
      "Backend unavailable. Run python web_app.py and open http://127.0.0.1:5000.";

    statusDot.classList.remove("online");
    console.error("Backend health check failed:", error);
  }
}

// Sidebar buttons.
document.getElementById("focusChat").addEventListener("click", () => {
  input.focus();
});

document.getElementById("newChat").addEventListener("click", clearChat);

document.getElementById("checkBackend").addEventListener(
  "click",
  checkBackend
);

// Suggestion buttons.
document.querySelectorAll("[data-question]").forEach((button) => {
  button.addEventListener("click", () => {
    useQuestion(button.dataset.question || "");
  });
});

// Send a question to the Flask /ask API.
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = input.value.trim();

  if (!question || sendButton.disabled) {
    return;
  }

  hero.hidden = true;
  suggestions.hidden = true;

  addMessage("You", question);
  input.value = "";

  sendButton.disabled = true;
  sendButton.textContent = "Thinking...";

  const pending = addMessage(
    "Company Brain",
    "Searching the company graph..."
  );

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: JSON.stringify({ question })
    });

    const data = await readJsonResponse(response);

    if (!response.ok) {
      pending.body.textContent =
        data.answer ||
        data.message ||
        `The server could not process this question (HTTP ${response.status}).`;

      pending.body.classList.add("error");
    } else {
      pending.body.textContent =
        data.answer || "The backend returned an empty answer.";

      addEvidence(pending.card, data.evidence);
    }
  } catch (error) {
    pending.body.textContent =
      error instanceof Error
        ? error.message
        : "Could not connect to the backend. Start Flask and refresh the page.";

    pending.body.classList.add("error");
    console.error("Question request failed:", error);
  } finally {
    sendButton.disabled = false;
    sendButton.innerHTML = originalSendButtonHTML;
    input.focus();
  }
});

// Enter sends; Shift + Enter creates a new line.
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

// Automatically check the backend when the page loads.
checkBackend();
// Smooth cursor glow
document.addEventListener("mousemove", (event) => {
  document.documentElement.style.setProperty(
    "--cursor-x",
    `${event.clientX}px`
  );

  document.documentElement.style.setProperty(
    "--cursor-y",
    `${event.clientY}px`
  );
});
document.addEventListener("mousemove", (event) => {
    document.body.style.setProperty("--cursor-x", `${event.clientX}px`);
    document.body.style.setProperty("--cursor-y", `${event.clientY}px`);
});