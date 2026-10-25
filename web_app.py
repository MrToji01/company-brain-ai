from flask import Flask, render_template, request, jsonify
import re
from app import CompanyBrainAgent

app = Flask(__name__)
agent = CompanyBrainAgent()


def asks_for_employee(question):
    """Return the employee name phrase for common employee lookup questions."""
    patterns = [
        r"\bwho\s+is\s+(.+?)(?=[?.!,]|$)",
        r"\btell\s+me\s+about\s+(.+?)(?=[?.!,]|$)",
        r"\bdetails\s+about\s+(.+?)(?=[?.!,]|$)",
        r"\bfind\s+employee(?:\s+named)?\s+(.+?)(?=[?.!,]|$)",
        r"\bsearch\s+employee(?:\s+named)?\s+(.+?)(?=[?.!,]|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    try:
        result = agent.graph.ro_query(
            "MATCH (n) RETURN count(n) AS total"
        )
        total = result.result_set[0][0] if result.result_set else 0
        return jsonify({
            "status": "ok",
            "nodes": total
        }), 200
    except Exception as error:
        print(f"Health error: {type(error).__name__}: {error}")
        return jsonify({"status": "error"}), 503


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        question = data.get("question", "")

        if not isinstance(question, str) or not question.strip():
            return jsonify({
                "answer": "Please enter a question."
            }), 400

        question = question.strip()

        
        # Allow employee ID and email searches without requiring a full name.
        has_employee_id = bool(
            re.search(r"\bEMP[-_ ]?\d+\b", question, re.IGNORECASE)
        )
        has_email = bool(
            re.search(
                r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
                question,
                re.IGNORECASE
            )
        )

        # Require a full name only for name-based employee searches.
        employee_name = asks_for_employee(question)

        if employee_name and not has_employee_id and not has_email:
            cleaned_name = re.sub(
                r"\s+", " ", employee_name
            ).strip(" \t\n.,?!")

            if len(cleaned_name.split()) < 2:
                return jsonify({
                    "answer": (
                        "Please provide the employee's full name so I can find "
                        "the correct person. For example: “Who is Kavya Gupta?”"
                    ),
                    "needs_full_name": True
                }), 200

        result = agent.answer_question(question)

        return jsonify({
            "answer": result.get("answer", "No answer was returned."),
            "terms": result.get("terms", []),
            "evidence": result.get("evidence", [])
        }), 200

    except Exception as error:
        print(f"Backend error: {type(error).__name__}: {error}")
        return jsonify({
            "answer": (
                "Something went wrong while searching the company graph. "
                "Check the Flask terminal for the detailed error."
            )
        }), 500


if __name__ == "__main__":
    print("Company Brain Web App starting...")
    print("Open http://127.0.0.1:5000")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
