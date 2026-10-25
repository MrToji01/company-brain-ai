import os
import csv
from falkordb import FalkorDB
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "6379"))
GRAPH_NAME = os.getenv("GRAPH_NAME", "company_brain")


def seed_company_graph():
    csv_file = os.getenv("DATASET_CSV", "dataset.csv")
    if not os.path.isfile(csv_file):
        raise FileNotFoundError(
            f"Could not find {csv_file!r} in {os.getcwd()}. "
            "Put dataset.csv in the project folder or set DATASET_CSV."
        )

    print(f"Connecting to FalkorDB at {DB_HOST}:{DB_PORT}...")
    db = FalkorDB(host=DB_HOST, port=DB_PORT)
    graph = db.select_graph(GRAPH_NAME)

    try:
        # WARNING: this resets the selected graph before importing the CSV.
        confirm = os.getenv("CONFIRM_CLEAR_GRAPH", "").strip().lower()
        if confirm != "yes":
            raise RuntimeError(
                "Safety stop: seeding clears the existing graph. "
                "To confirm, set CONFIRM_CLEAR_GRAPH=yes and run seed.py again."
            )

        print(f"Clearing old data from graph {GRAPH_NAME!r}...")
        graph.query("MATCH (n) DETACH DELETE n")

        count = 0
        with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError("dataset.csv is empty or has no header row.")

            for row in reader:
                # Strip whitespace and safely handle blank/None CSV cells.
                row = {
                    (key or "").strip(): (value or "").strip()
                    for key, value in row.items()
                }

                emp_id = row.get("employee_id") or row.get("id")
                full_name = row.get("full_name") or " ".join(
                    part for part in (
                        row.get("first_name", ""),
                        row.get("last_name", "")
                    ) if part
                )
                if not emp_id or not full_name:
                    continue

                department = row.get("department") or "General"
                project_id = row.get("project_id")
                project_name = row.get("project_name")
                job_title = row.get("job_title") or row.get("role")
                email = row.get("email")
                location = row.get("location")
                skills = row.get("skills")
                status = row.get("employment_status") or row.get("status")
                hire_date = row.get("hire_date")
                manager_id = row.get("manager_id")

                # Use project name as a fallback key if project_id is missing.
                project_key = project_id or project_name or "PROJ-GENERAL"
                project_label = project_name or "General Operations"

                cypher = """
                    MERGE (d:Department {name: $department})
                    MERGE (p:Project {id: $project_id})
                    SET p.name = CASE
                        WHEN $project_name <> '' THEN $project_name
                        WHEN p.name IS NULL THEN 'General Operations'
                        ELSE p.name
                    END
                    MERGE (e:Employee {employee_id: $emp_id})
                    SET e.id = $emp_id,
                        e.name = $full_name,
                        e.email = $email,
                        e.job_title = $job_title,
                        e.role = $job_title,
                        e.location = $location,
                        e.skills = $skills,
                        e.employment_status = $status,
                        e.status = $status,
                        e.hire_date = $hire_date,
                        e.manager_id = $manager_id
                    MERGE (e)-[:BELONGS_TO]->(d)
                """
                params = {
                    "department": department,
                    "project_id": project_key,
                    "project_name": project_name or project_label,
                    "emp_id": emp_id,
                    "full_name": full_name,
                    "email": email,
                    "job_title": job_title,
                    "location": location,
                    "skills": skills,
                    "status": status,
                    "hire_date": hire_date,
                    "manager_id": manager_id,
                }

                if project_name:
                    cypher += """
                        MERGE (e)-[:WORKS_ON]->(p)
                    """

                graph.query(cypher, params)
                count += 1

                if count % 100 == 0:
                    print(f"Processed {count} employee records...")

        print(f"Successfully imported {count} employee records into {GRAPH_NAME!r}.")
        print("Tip: employee profiles and project relationships are now indexed consistently.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_company_graph()
