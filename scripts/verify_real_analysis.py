import urllib.request
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

print("--- Submitting Sample Contract A ('design-agency-msa') ---")
start_time = time.time()

req = urllib.request.Request(
    f"{BASE_URL}/api/analyze",
    data=json.dumps({"sample_id": "design-agency-msa"}).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode())
    session_id = res["session_id"]
    print(f"Session started: {session_id}")

completed = False
for i in range(120):
    time.sleep(1)
    with urllib.request.urlopen(f"{BASE_URL}/api/status/{session_id}") as s_resp:
        st = json.loads(s_resp.read().decode())
        print(f"  [{int(time.time() - start_time)}s] Stage {st['stage']}: {st['stage_label']} ({st['percent']}%) - Clauses: {st['clauses_found_so_far']}")
        if st["completed"]:
            completed = True
            break

elapsed = time.time() - start_time
print(f"\nAnalysis completed in {elapsed:.2f} seconds!")

with urllib.request.urlopen(f"{BASE_URL}/api/results/{session_id}") as r_resp:
    res = json.loads(r_resp.read().decode())
    print(f"Total clauses: {res['clause_count']}")
    print(f"Flagged clauses: {res['flagged_count']}")
    print(f"Risk score: {res['risk_score']}")
    top_flagged = [c for c in res["clauses"] if c["severity"] in ("high", "medium")][0]
    print(f"Top Flagged Clause: {top_flagged['section']} - {top_flagged['title']}")
    print(f"Plain English: {top_flagged['plain_english']}")
    print(f"Rationale: {top_flagged['rationale']}")

with urllib.request.urlopen(f"{BASE_URL}/api/counter_draft/{session_id}?clause_id={top_flagged['id']}&tone=diplomatic") as cd_resp:
    cd = json.loads(cd_resp.read().decode())
    print(f"Counter Draft Subject: {cd['subject']}")
    print(f"Predicted Acceptance %: {cd['predicted_acceptance_pct']}%")

with urllib.request.urlopen(f"{BASE_URL}/api/attorney_prep/{session_id}") as ap_resp:
    ap = json.loads(ap_resp.read().decode())
    print(f"Attorney Prep Questions count: {len(ap['questions'])}")
    for qg in ap['questions'][:2]:
        print(f" - {qg['section']}: {qg['questions']}")
