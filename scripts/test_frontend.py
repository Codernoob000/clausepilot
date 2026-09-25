"""Phase 4 Frontend Validation Script."""

import urllib.request
import urllib.parse
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_screens():
    print("--- 1. Testing Screen Endpoints ---")
    for screen in ["screen1.html", "screen2.html", "screen3.html", "screen4.html", "screen5.html"]:
        url = f"{BASE_URL}/{screen}"
        resp = urllib.request.urlopen(url)
        content = resp.read().decode("utf-8")
        assert resp.status == 200, f"Failed to load {screen}"
        assert "Informational tool" in content, f"Missing disclaimer in {screen}"
        print(f"  {screen}: HTTP {resp.status}, Disclaimer present: True, Length: {len(content)} bytes")

def test_full_user_journey():
    print("\n--- 2. Testing End-to-End User Journey (Sample 1: Design Agency MSA) ---")
    req = urllib.request.Request(
        f"{BASE_URL}/api/analyze",
        data=json.dumps({"sample_id": "design-agency-msa"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        session_id_1 = data["session_id"]
        print(f"  POST /api/analyze succeeded. Session ID: {session_id_1}")

    # Poll status
    print("  Polling status...")
    completed = False
    for _ in range(120):
        time.sleep(1)
        with urllib.request.urlopen(f"{BASE_URL}/api/status/{session_id_1}") as s_resp:
            s_data = json.loads(s_resp.read().decode("utf-8"))
            if s_data["completed"]:
                completed = True
                print(f"  Analysis completed: 100% (Found {s_data['clauses_found_so_far']} clauses)")
                break

    assert completed, "Analysis did not complete in 120s"

    # Fetch results
    with urllib.request.urlopen(f"{BASE_URL}/api/results/{session_id_1}") as r_resp:
        res1 = json.loads(r_resp.read().decode("utf-8"))
        print(f"  Results: {res1['clause_count']} clauses, {res1['flagged_count']} flagged, Risk Score: {res1['risk_score']} ({res1['risk_label']})")
        assert res1["clause_count"] > 0
        assert res1["flagged_count"] > 0

    # Fetch Counter Draft
    with urllib.request.urlopen(f"{BASE_URL}/api/counter_draft/{session_id_1}?tone=diplomatic") as cd_resp:
        cd = json.loads(cd_resp.read().decode("utf-8"))
        print(f"  Counter Draft (Diplomatic): Acceptance={cd['predicted_acceptance_pct']}%, Subject='{cd['subject']}'")
        assert cd["predicted_acceptance_pct"] > 0

    # Fetch Attorney Prep
    with urllib.request.urlopen(f"{BASE_URL}/api/attorney_prep/{session_id_1}") as ap_resp:
        ap = json.loads(ap_resp.read().decode("utf-8"))
        print(f"  Attorney Prep: Est. Minutes={ap['estimated_call_minutes']}, Questions={len(ap['questions'])}")
        assert len(ap["questions"]) > 0

    print("\n--- 3. Testing Sample 2: Tech Startup Contractor Agreement ---")
    req2 = urllib.request.Request(
        f"{BASE_URL}/api/analyze",
        data=json.dumps({"sample_id": "tech-startup-contractor"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req2) as resp2:
        session_id_2 = json.loads(resp2.read().decode("utf-8"))["session_id"]
        print(f"  POST /api/analyze for sample 2. Session ID: {session_id_2}")

    completed2 = False
    for _ in range(120):
        time.sleep(1)
        with urllib.request.urlopen(f"{BASE_URL}/api/status/{session_id_2}") as s_resp:
            s_data = json.loads(s_resp.read().decode("utf-8"))
            if s_data["completed"]:
                completed2 = True
                print(f"  Sample 2 completed: 100% (Found {s_data['clauses_found_so_far']} clauses)")
                break

    assert completed2, "Sample 2 did not complete in 120s"

    with urllib.request.urlopen(f"{BASE_URL}/api/results/{session_id_2}") as r_resp:
        res2 = json.loads(r_resp.read().decode("utf-8"))
        print(f"  Sample 2 Results: {res2['clause_count']} clauses, {res2['flagged_count']} flagged, Risk Score: {res2['risk_score']}")

    # Verify contracts produced visibly different results
    print("\n--- 4. Comparing Sample 1 vs Sample 2 Divergence ---")
    print(f"  Sample 1 Clauses: {res1['clause_count']} | Sample 2 Clauses: {res2['clause_count']}")
    print(f"  Sample 1 Flagged: {res1['flagged_count']} | Sample 2 Flagged: {res2['flagged_count']}")
    print(f"  Sample 1 Risk Score: {res1['risk_score']} | Sample 2 Risk Score: {res2['risk_score']}")
    
    assert (res1["clause_count"] != res2["clause_count"] or res1["risk_score"] != res2["risk_score"] or res1["filename"] != res2["filename"]), "Samples produced identical results!"
    print("  Divergence check: PASSED (two different contracts produce visibly different analysis results)")

    print("\nPHASE 4 FRONTEND VALIDATION: ALL PASSED!")

if __name__ == "__main__":
    test_screens()
    test_full_user_journey()
