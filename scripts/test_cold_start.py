"""Phase 6 Cold-Start Live HTTPS Deployment Validation."""

import json
import time
import urllib.request

LIVE_URL = "https://type-styles-compounds-competitors.trycloudflare.com"

def test_cold_start_live():
    print(f"=================================================================")
    print(f"      Phase 6 Cold-Start Live Deployment Verification            ")
    print(f"      Target: {LIVE_URL}")
    print(f"=================================================================")

    # 1. Cold GET /health
    print("\n[STEP 1] Testing Live /health endpoint...")
    with urllib.request.urlopen(f"{LIVE_URL}/health") as resp:
        assert resp.status == 200
        health_data = json.loads(resp.read().decode())
        print("  Status 200 OK:", health_data)

    # 2. Cold GET /screen1.html
    print("\n[STEP 2] Testing Live /screen1.html (Upload Screen)...")
    with urllib.request.urlopen(f"{LIVE_URL}/screen1.html") as resp:
        assert resp.status == 200
        html = resp.read().decode()
        assert "ClausePilot" in html
        assert "Informational tool" in html
        print(f"  Status 200 OK (Loaded {len(html)} bytes, Disclaimer verified)")

    # 3. Trigger live contract analysis via POST /api/analyze
    print("\n[STEP 3] Triggering contract analysis on Live URL...")
    req = urllib.request.Request(
        f"{LIVE_URL}/api/analyze",
        data=json.dumps({"sample_id": "design-agency-msa"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode())
        session_id = data["session_id"]
        print(f"  Session created successfully: {session_id}")

    # 4. Poll live status
    print("\n[STEP 4] Polling live analysis status...")
    completed = False
    for i in range(120):
        time.sleep(1)
        with urllib.request.urlopen(f"{LIVE_URL}/api/status/{session_id}") as s_resp:
            st = json.loads(s_resp.read().decode())
            if st["completed"]:
                completed = True
                print(f"  Live pipeline complete: {st['percent']}% (Found {st['clauses_found_so_far']} clauses)")
                break

    assert completed, "Live analysis timed out"

    # 5. Fetch live results
    print("\n[STEP 5] Fetching live results...")
    with urllib.request.urlopen(f"{LIVE_URL}/api/results/{session_id}") as r_resp:
        results = json.loads(r_resp.read().decode())
        print(f"  Results verified: {results['clause_count']} clauses, {results['flagged_count']} flagged, Risk Score: {results['risk_score']}")

    # 6. Fetch live counter draft
    print("\n[STEP 6] Fetching live counter draft...")
    with urllib.request.urlopen(f"{LIVE_URL}/api/counter_draft/{session_id}?tone=firm") as cd_resp:
        cd = json.loads(cd_resp.read().decode())
        print(f"  Counter Draft (Firm): Acceptance={cd['predicted_acceptance_pct']}%, Subject='{cd['subject']}'")

    # 7. Fetch live attorney prep
    print("\n[STEP 7] Fetching live attorney prep sheet...")
    with urllib.request.urlopen(f"{LIVE_URL}/api/attorney_prep/{session_id}") as ap_resp:
        ap = json.loads(ap_resp.read().decode())
        print(f"  Attorney Prep Sheet: {len(ap['questions'])} question groups, Est. Minutes={ap['estimated_call_minutes']}")

    # 8. Secret leakage check
    print("\n[STEP 8] Checking for secret leakage across responses...")
    full_dump = json.dumps([health_data, results, cd, ap])
    for secret_marker in ["AIzaSy", "gho_", "sk-"]:
        assert secret_marker not in full_dump, f"Potential secret marker '{secret_marker}' found in responses!"
        assert secret_marker not in html, f"Potential secret marker '{secret_marker}' found in client HTML!"
    print("  Zero secrets found in any client response or page HTML.")

    print("\n=================================================================")
    print("PHASE 6 DEPLOYMENT VALIDATION: ALL PASSED!")
    print(f"Live URL: {LIVE_URL}")
    print("=================================================================")

if __name__ == "__main__":
    test_cold_start_live()
