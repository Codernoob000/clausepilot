"""Wire all 5 Google Stitch HTML screens to real FastAPI backend per frontend-wiring-spec.md."""

import os
import re

TEMPLATES_DIR = "templates"

def wire_screen1():
    path = os.path.join(TEMPLATES_DIR, "screen1.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Persona & Title cleanup
    html = html.replace("Maya Lin", "Demo User")
    html = html.replace("Product Designer", "Contractor")
    html = html.replace("Master Services Agreement - Apex Studio.pdf", "Contract Analysis Workspace")
    html = html.replace("Apex Studio", "Client Organization")

    # Step navigation
    html = html.replace('data-path="upload-contract" href="#"', 'data-path="upload-contract" href="/screen1.html"')
    html = html.replace('data-path="analysis-and-progress" href="#"', 'data-path="analysis-and-progress" href="/screen2.html"')
    html = html.replace('data-path="clause-breakdown-and-benchmarks" href="#"', 'data-path="clause-breakdown-and-benchmarks" href="/screen3.html"')
    html = html.replace('data-path="counter-proposal-draft" href="#"', 'data-path="counter-proposal-draft" href="/screen4.html"')
    html = html.replace('data-path="attorney-prep-sheet" href="#"', 'data-path="attorney-prep-sheet" href="/screen5.html"')

    # Replace simulated upload with real API wiring
    new_script = """<script>
  (function initUploadInteractions() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const pasteToggle = document.getElementById('paste-text-toggle');
    const pasteDrawer = document.getElementById('paste-drawer');
    const closePaste = document.getElementById('close-paste-drawer');
    const submitRawBtn = document.getElementById('submit-raw-text-btn');
    const uploadStatusCard = document.getElementById('upload-status-card');
    const progressBarFill = document.getElementById('progress-bar-fill');
    const percentText = document.getElementById('parsing-percentage');
    const fileNameText = document.getElementById('uploaded-filename');
    const fileSizeText = document.getElementById('uploaded-filesize');
    const rawTextArea = document.getElementById('raw-contract-text');
    const sampleCards = document.querySelectorAll('.sample-card');

    if (!dropZone || !fileInput) return;

    browseBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      fileInput.click();
    });

    dropZone.addEventListener('click', () => {
      fileInput.click();
    });

    if (pasteToggle && pasteDrawer) {
      pasteToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        pasteDrawer.classList.toggle('hidden');
      });
    }

    if (closePaste && pasteDrawer) {
      closePaste.addEventListener('click', () => {
        pasteDrawer.classList.add('hidden');
      });
    }

    ['dragenter', 'dragover'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('bg-secondary-container/20', 'shadow-xl');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('bg-secondary-container/20', 'shadow-xl');
      }, false);
    });

    dropZone.addEventListener('drop', (e) => {
      const files = e.dataTransfer.files;
      if (files.length > 0) uploadFile(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
      if (fileInput.files.length > 0) uploadFile(fileInput.files[0]);
    });

    if (submitRawBtn) {
      submitRawBtn.addEventListener('click', () => {
        const text = rawTextArea ? rawTextArea.value.trim() : '';
        if (!text) {
          alert('Please paste contract text first.');
          return;
        }
        const blob = new Blob([text], { type: 'text/plain' });
        const file = new File([blob], 'Custom_Pasted_Contract.txt', { type: 'text/plain' });
        uploadFile(file);
      });
    }

    sampleCards.forEach(card => {
      card.addEventListener('click', () => {
        const type = card.getAttribute('data-sample');
        let sample_id = 'design-agency-msa';
        let displayName = 'Design_Agency_MSA.pdf';
        if (type === 'contractor') {
          sample_id = 'tech-startup-contractor';
          displayName = 'Tech_Startup_Contractor_Agreement.pdf';
        } else if (type === 'licensing') {
          sample_id = 'content-media-retainer';
          displayName = 'Content_Media_Retainer.pdf';
        }
        
        showProgress(displayName, 'Curated benchmark sample');
        fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sample_id: sample_id })
        })
        .then(res => {
          if (!res.ok) throw new Error('Analysis request failed');
          return res.json();
        })
        .then(data => {
          progressBarFill.style.width = '100%';
          percentText.textContent = '100%';
          setTimeout(() => {
            window.location.href = `/screen2.html?session=${data.session_id}`;
          }, 350);
        })
        .catch(err => {
          alert('Error analyzing sample contract: ' + err.message);
          uploadStatusCard.classList.add('hidden');
        });
      });
    });

    function showProgress(name, size) {
      uploadStatusCard.classList.remove('hidden');
      dropZone.scrollIntoView({ behavior: 'smooth', block: 'center' });
      fileNameText.textContent = name;
      fileSizeText.textContent = size + ' · Initializing GenAI extraction pipeline...';
      progressBarFill.style.width = '35%';
      percentText.textContent = '35%';
    }

    function uploadFile(file) {
      const sizeStr = (file.size / (1024 * 1024)).toFixed(1) + ' MB';
      showProgress(file.name, sizeStr);

      const formData = new FormData();
      formData.append('file', file);

      fetch('/api/analyze', {
        method: 'POST',
        body: formData
      })
      .then(res => {
        if (!res.ok) {
          return res.json().then(e => { throw new Error(e.detail || 'Upload failed'); });
        }
        return res.json();
      })
      .then(data => {
        progressBarFill.style.width = '100%';
        percentText.textContent = '100%';
        fileSizeText.textContent = sizeStr + ' · Document loaded. Launching diagnostics...';
        setTimeout(() => {
          window.location.href = `/screen2.html?session=${data.session_id}`;
        }, 400);
      })
      .catch(err => {
        alert('Upload Error: ' + err.message);
        uploadStatusCard.classList.add('hidden');
      });
    }
  })();
</script>"""

    html = re.sub(r'<script>\s*\(function initUploadInteractions\(\).*?</script>', new_script, html, flags=re.DOTALL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Wired screen1.html")


def wire_screen2():
    path = os.path.join(TEMPLATES_DIR, "screen2.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Persona & Title cleanup
    html = html.replace("Maya Lin", "Demo User")
    html = html.replace("Product Designer", "Contractor")
    html = html.replace("Master Services Agreement - Apex Studio.pdf", "Contract Analysis Workspace")
    html = html.replace("Apex Studio", "Client Organization")

    # Step navigation placeholder links
    html = html.replace('data-path="upload-contract" href="#"', 'data-path="upload-contract" id="nav-step-1" href="/screen1.html"')
    html = html.replace('data-path="analysis-and-progress" href="#"', 'data-path="analysis-and-progress" id="nav-step-2" href="/screen2.html"')
    html = html.replace('data-path="clause-breakdown-and-benchmarks" href="#"', 'data-path="clause-breakdown-and-benchmarks" id="nav-step-3" href="/screen3.html"')
    html = html.replace('data-path="counter-proposal-draft" href="#"', 'data-path="counter-proposal-draft" id="nav-step-4" href="/screen4.html"')
    html = html.replace('data-path="attorney-prep-sheet" href="#"', 'data-path="attorney-prep-sheet" id="nav-step-5" href="/screen5.html"')

    # Replace fake progress simulator with real polling engine
    new_script = """<script>
  (function initRealProgressPoller() {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session');

    if (!sessionId) {
      alert('No active session ID found. Redirecting to upload.');
      window.location.href = '/screen1.html';
      return;
    }

    // Thread session ID through all navigation links
    ['nav-step-1', 'nav-step-2', 'nav-step-3', 'nav-step-4', 'nav-step-5'].forEach((id, idx) => {
      const el = document.getElementById(id);
      if (el) el.href = `/screen${idx+1}.html?session=${sessionId}`;
    });

    const progressFill = document.getElementById('progress-fill');
    const percentLabel = document.getElementById('progress-percent-label');
    const etaLabel = document.getElementById('live-eta');
    const countdownElement = document.getElementById('countdown-num');
    const docTitle = document.querySelector('header span.truncate');
    const pageCountEl = document.querySelector('.page-count-badge');
    const clauseCountEl = document.querySelector('.clause-count-badge');

    // Pipeline step indicators
    const stepCards = document.querySelectorAll('.pipeline-step-item');

    let pollInterval = setInterval(checkStatus, 1000);
    checkStatus();

    function checkStatus() {
      fetch(`/api/status/${sessionId}`)
        .then(res => {
          if (!res.ok) throw new Error('Status poll failed');
          return res.json();
        })
        .then(data => {
          if (progressFill) progressFill.style.width = data.percent + '%';
          if (percentLabel) percentLabel.textContent = data.percent + '%';
          if (countdownElement) countdownElement.textContent = data.eta_seconds || 1;
          if (etaLabel) {
            etaLabel.textContent = data.completed ? 'Analysis Complete' : `Est. remaining: ~${data.eta_seconds}s`;
          }

          // Update header badges
          const pageBadges = document.querySelectorAll('.header-meta-badge');
          if (pageBadges.length >= 2) {
            pageBadges[0].textContent = `${data.page_count} Pages`;
            pageBadges[1].textContent = `${data.clauses_found_so_far} Clauses identified`;
          }

          // Update discovery stream live ticker
          const ticker = document.getElementById('live-discovery-ticker');
          if (ticker) {
            ticker.textContent = `Analyzing clause ${data.clauses_found_so_far} against 28 market benchmarks (${data.stage_label})...`;
          }

          if (data.completed) {
            clearInterval(pollInterval);
            if (progressFill) progressFill.style.width = '100%';
            if (percentLabel) percentLabel.textContent = '100%';
            setTimeout(() => {
              window.location.href = `/screen3.html?session=${sessionId}`;
            }, 600);
          }
        })
        .catch(err => {
          console.warn('Poll error:', err);
        });
    }
  })();
</script>"""

    html = re.sub(r'<script>\s*\(function initProgressSimulator\(\).*?</script>', new_script, html, flags=re.DOTALL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Wired screen2.html")


def wire_screen3():
    path = os.path.join(TEMPLATES_DIR, "screen3.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Persona & Title cleanup
    html = html.replace("Maya Lin", "Demo User")
    html = html.replace("Product Designer", "Contractor")
    html = html.replace("Master Services Agreement - Apex Studio.pdf", "Contract Analysis Workspace")
    html = html.replace("Apex Studio", "Client Organization")
    html = html.replace("Apex", "Client")

    # Step navigation
    html = html.replace('data-path="upload-contract" href="#"', 'data-path="upload-contract" id="nav-step-1" href="/screen1.html"')
    html = html.replace('data-path="analysis-and-progress" href="#"', 'data-path="analysis-and-progress" id="nav-step-2" href="/screen2.html"')
    html = html.replace('data-path="clause-breakdown-and-benchmarks" href="#"', 'data-path="clause-breakdown-and-benchmarks" id="nav-step-3" href="/screen3.html"')
    html = html.replace('data-path="counter-proposal-draft" href="#"', 'data-path="counter-proposal-draft" id="nav-step-4" href="/screen4.html"')
    html = html.replace('data-path="attorney-prep-sheet" href="#"', 'data-path="attorney-prep-sheet" id="nav-step-5" href="/screen5.html"')

    # Replace static clause cards container and script with dynamic data loader
    new_script = """<script>
  let sessionData = null;

  function toggleClause(cardId) {
    const card = document.getElementById(cardId);
    if (!card) return;
    const content = card.querySelector('.clause-content');
    const chevron = card.querySelector('.clause-chevron');
    
    if (content.classList.contains('hidden')) {
      content.classList.remove('hidden');
      content.classList.add('flex');
      if (chevron) chevron.classList.add('rotate-180');
    } else {
      content.classList.add('hidden');
      content.classList.remove('flex');
      if (chevron) chevron.classList.remove('rotate-180');
    }
  }

  (function initResultsRenderer() {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session');

    if (!sessionId) {
      alert('No active session found. Redirecting to upload.');
      window.location.href = '/screen1.html';
      return;
    }

    // Thread session across navigation
    ['nav-step-1', 'nav-step-2', 'nav-step-3', 'nav-step-4', 'nav-step-5'].forEach((id, idx) => {
      const el = document.getElementById(id);
      if (el) el.href = `/screen${idx+1}.html?session=${sessionId}`;
    });

    fetch(`/api/results/${sessionId}`)
      .then(res => {
        if (!res.ok) throw new Error('Results not ready');
        return res.json();
      })
      .then(data => {
        sessionData = data;
        renderResults(data, sessionId);
      })
      .catch(err => {
        console.error('Error fetching results:', err);
        // Retry in 1.5s in case still completing
        setTimeout(() => {
          fetch(`/api/results/${sessionId}`).then(r => r.json()).then(data => {
            sessionData = data;
            renderResults(data, sessionId);
          });
        }, 1500);
      });

    function renderResults(data, sid) {
      // Top bar filename
      const titleEl = document.querySelector('header span.truncate');
      if (titleEl) titleEl.textContent = data.filename;

      // Summary stat cards
      const statNums = document.querySelectorAll('.summary-stat-value');
      if (statNums.length >= 4) {
        statNums[0].textContent = data.clause_count;
        statNums[1].textContent = data.flagged_count;
        statNums[2].textContent = `${data.risk_score}/100`;
        statNums[3].textContent = data.risk_label;
      }

      // Action button link to counter-draft
      const counterBtn = document.getElementById('btn-goto-counter');
      const topClause = (data.clauses.find(c => c.severity === 'high') || data.clauses[0]);
      if (counterBtn && topClause) {
        counterBtn.href = `/screen4.html?session=${sid}&clause=${topClause.id}`;
      }

      // Render Dynamic Clause Cards
      const container = document.getElementById('clauses-container');
      if (!container) return;

      container.innerHTML = '';
      data.clauses.forEach((clause, idx) => {
        const isFlagged = clause.severity === 'high' || clause.severity === 'medium';
        const sevColor = clause.severity === 'high' 
          ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' 
          : (clause.severity === 'medium' ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30');
        const sevLabel = clause.severity.toUpperCase() + ' RISK';

        const cardHtml = `
        <div id="clause-card-${clause.id}" class="bg-surface-container rounded-2xl border ${isFlagged ? 'border-outline-variant/60 shadow-md' : 'border-outline-variant/20'} overflow-hidden transition-all mb-4">
          <div onclick="toggleClause('clause-card-${clause.id}')" class="p-6 cursor-pointer flex items-center justify-between gap-4 hover:bg-surface-container-high/40 transition-colors">
            <div class="flex items-center gap-4 flex-1">
              <span class="px-3 py-1 rounded-full text-xs font-bold border ${sevColor}">${sevLabel}</span>
              <div>
                <div class="text-xs text-on-surface-variant font-medium">${clause.section} · ${clause.category}</div>
                <h3 class="text-base font-bold text-on-surface mt-0.5">${clause.title}</h3>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <div class="text-right hidden sm:block">
                <div class="text-xs text-on-surface-variant">Market Standard Adoption</div>
                <div class="text-sm font-semibold text-primary">${clause.market_adoption_pct}% baseline</div>
              </div>
              <span class="material-symbols-outlined clause-chevron transition-transform duration-200 text-on-surface-variant">expand_more</span>
            </div>
          </div>
          
          <div class="clause-content hidden flex-col border-t border-outline-variant/30 p-6 bg-surface/50">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
              <!-- As Written -->
              <div class="p-4 rounded-xl bg-surface-container border border-outline-variant/40 flex flex-col justify-between">
                <div>
                  <div class="flex items-center gap-2 text-xs font-semibold text-rose-400 mb-2">
                    <span class="material-symbols-outlined text-sm">gavel</span>
                    <span>As Written in Contract</span>
                  </div>
                  <p class="text-xs text-on-surface-variant leading-relaxed font-mono bg-surface/80 p-3 rounded-lg border border-outline-variant/20">${clause.original_text}</p>
                </div>
              </div>

              <!-- Plain English -->
              <div class="p-4 rounded-xl bg-surface-container border border-outline-variant/40 flex flex-col justify-between">
                <div>
                  <div class="flex items-center gap-2 text-xs font-semibold text-amber-400 mb-2">
                    <span class="material-symbols-outlined text-sm">translate</span>
                    <span>Plain-English Impact</span>
                  </div>
                  <p class="text-sm text-on-surface leading-relaxed">${clause.plain_english}</p>
                  ${clause.rationale ? `<div class="mt-3 p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-xs text-amber-300"><strong>Deviation:</strong> ${clause.rationale}</div>` : ''}
                </div>
              </div>

              <!-- Market Standard -->
              <div class="p-4 rounded-xl bg-surface-container border border-outline-variant/40 flex flex-col justify-between">
                <div>
                  <div class="flex items-center gap-2 text-xs font-semibold text-emerald-400 mb-2">
                    <span class="material-symbols-outlined text-sm">verified</span>
                    <span>Balanced Market Standard</span>
                  </div>
                  <p class="text-xs text-on-surface-variant leading-relaxed italic bg-surface/80 p-3 rounded-lg border border-outline-variant/20">"${clause.market_standard_text}"</p>
                  <div class="mt-3 flex items-center justify-between text-xs text-emerald-400">
                    <span>${clause.market_adoption_pct}% Industry Adoption</span>
                    <a href="/screen4.html?session=${sid}&clause=${clause.id}" class="underline font-semibold hover:text-emerald-300">Draft Counter &rarr;</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>`;

        container.insertAdjacentHTML('beforeend', cardHtml);
      });
    }
  })();
</script>"""

    # Wrap the clause cards container so our script can inject dynamically
    html = re.sub(r'<div id="clause-card-1".*?</div>\s*</div>\s*</div>\s*(?=<section|<div class="flex items-center justify-between)', '<div id="clauses-container"></div>', html, flags=re.DOTALL)
    html = re.sub(r'<script>\s*function toggleClause.*?\(cardId\).*?</script>', new_script, html, flags=re.DOTALL)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Wired screen3.html")


def wire_screen4():
    path = os.path.join(TEMPLATES_DIR, "screen4.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Persona & Title cleanup
    html = html.replace("Maya Lin", "Demo User")
    html = html.replace("Product Designer", "Contractor")
    html = html.replace("Master Services Agreement - Apex Studio.pdf", "Contract Analysis Workspace")
    html = html.replace("Apex Studio", "Client Organization")
    html = html.replace("Elena", "Client Team")
    html = html.replace("Apex", "Client")

    # Step navigation
    html = html.replace('data-path="upload-contract" href="#"', 'data-path="upload-contract" id="nav-step-1" href="/screen1.html"')
    html = html.replace('data-path="analysis-and-progress" href="#"', 'data-path="analysis-and-progress" id="nav-step-2" href="/screen2.html"')
    html = html.replace('data-path="clause-breakdown-and-benchmarks" href="#"', 'data-path="clause-breakdown-and-benchmarks" id="nav-step-3" href="/screen3.html"')
    html = html.replace('data-path="counter-proposal-draft" href="#"', 'data-path="counter-proposal-draft" id="nav-step-4" href="/screen4.html"')
    html = html.replace('data-path="attorney-prep-sheet" href="#"', 'data-path="attorney-prep-sheet" id="nav-step-5" href="/screen5.html"')

    # Replace hardcoded toneData script with live API fetching
    new_script = """<script>
    (function initCounterDraftUI() {
      const urlParams = new URLSearchParams(window.location.search);
      const sessionId = urlParams.get('session');
      let currentClauseId = urlParams.get('clause');
      let currentTone = 'diplomatic';
      let fullResults = null;
      let flaggedClauses = [];
      let currentFlaggedIndex = 0;

      if (!sessionId) {
        alert('No active session found. Redirecting to upload.');
        window.location.href = '/screen1.html';
        return;
      }

      // Thread session across navigation
      ['nav-step-1', 'nav-step-2', 'nav-step-3', 'nav-step-4', 'nav-step-5'].forEach((id, idx) => {
        const el = document.getElementById(id);
        if (el) el.href = `/screen${idx+1}.html?session=${sessionId}`;
      });

      const emailSubject = document.getElementById('email-subject');
      const emailBody = document.getElementById('email-body');
      const copyBtn = document.getElementById('btn-copy-email');
      const toast = document.getElementById('copy-toast');
      const acceptanceLabel = document.getElementById('predicted-acceptance-badge');
      const originalTextEl = document.getElementById('original-clause-text');
      const proposedTextEl = document.getElementById('proposed-counter-text');
      const priorityLabel = document.getElementById('clause-priority-label');
      const prevClauseBtn = document.getElementById('prev-clause-btn');
      const nextClauseBtn = document.getElementById('next-clause-btn');
      const docTitle = document.querySelector('header span.truncate');

      // Fetch Results first to populate clause carousel
      fetch(`/api/results/${sessionId}`)
        .then(r => r.json())
        .then(data => {
          fullResults = data;
          if (docTitle) docTitle.textContent = data.filename;
          flaggedClauses = data.clauses.filter(c => c.severity === 'high' || c.severity === 'medium');
          if (flaggedClauses.length === 0) flaggedClauses = data.clauses;

          if (currentClauseId) {
            const foundIdx = flaggedClauses.findIndex(c => c.id === currentClauseId);
            if (foundIdx !== -1) currentFlaggedIndex = foundIdx;
          }

          loadClauseDraft();
        });

      function loadClauseDraft() {
        const clause = flaggedClauses[currentFlaggedIndex];
        if (!clause) return;

        if (priorityLabel) {
          priorityLabel.textContent = `Priority ${currentFlaggedIndex + 1} of ${flaggedClauses.length} to Counter: ${clause.title}`;
        }
        if (originalTextEl) {
          originalTextEl.textContent = clause.original_text;
        }

        // Call backend counter-draft API
        fetch(`/api/counter_draft/${sessionId}?clause_id=${clause.id}&tone=${currentTone}`)
          .then(r => r.json())
          .then(draft => {
            if (emailSubject) emailSubject.value = draft.subject;
            if (emailBody) emailBody.value = draft.body;
            if (proposedTextEl) proposedTextEl.textContent = draft.proposed_clause;
            if (acceptanceLabel) {
              acceptanceLabel.textContent = `Predicted Acceptance ${draft.predicted_acceptance_pct}%`;
            }
          });
      }

      // Tone Buttons
      const toneButtons = document.querySelectorAll('#tone-selector .tone-btn');
      toneButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          toneButtons.forEach(b => {
            b.classList.remove('bg-primary-container', 'text-on-primary', 'shadow-sm', 'font-semibold');
            b.classList.add('text-on-surface-variant');
          });
          btn.classList.remove('text-on-surface-variant');
          btn.classList.add('bg-primary-container', 'text-on-primary', 'shadow-sm', 'font-semibold');

          currentTone = btn.getAttribute('data-tone') || 'diplomatic';
          loadClauseDraft();
        });
      });

      // Next / Prev Clause Carousel
      if (prevClauseBtn) {
        prevClauseBtn.addEventListener('click', () => {
          if (currentFlaggedIndex > 0) {
            currentFlaggedIndex--;
            loadClauseDraft();
          }
        });
      }
      if (nextClauseBtn) {
        nextClauseBtn.addEventListener('click', () => {
          if (currentFlaggedIndex < flaggedClauses.length - 1) {
            currentFlaggedIndex++;
            loadClauseDraft();
          }
        });
      }

      // Copy Button
      if (copyBtn && emailBody) {
        copyBtn.addEventListener('click', () => {
          navigator.clipboard.writeText(emailBody.value).then(() => {
            if (toast) {
              toast.classList.remove('translate-y-20', 'opacity-0');
              toast.classList.add('translate-y-0', 'opacity-100');
              setTimeout(() => {
                toast.classList.remove('translate-y-0', 'opacity-100');
                toast.classList.add('translate-y-20', 'opacity-0');
              }, 2500);
            }
          });
        });
      }
    })();
  </script>"""

    html = re.sub(r'<script>\s*\(function\(\)\s*\{.*?const toneData =.*?</script>', new_script, html, flags=re.DOTALL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Wired screen4.html")


def wire_screen5():
    path = os.path.join(TEMPLATES_DIR, "screen5.html")
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # Persona & Title cleanup
    html = html.replace("Maya Lin", "Demo User")
    html = html.replace("Product Designer", "Contractor")
    html = html.replace("Master Services Agreement - Apex Studio.pdf", "Contract Analysis Workspace")
    html = html.replace("Apex Studio", "Client Organization")
    html = html.replace("Apex", "Client")

    # Step navigation
    html = html.replace('data-path="upload-contract" href="#"', 'data-path="upload-contract" id="nav-step-1" href="/screen1.html"')
    html = html.replace('data-path="analysis-and-progress" href="#"', 'data-path="analysis-and-progress" id="nav-step-2" href="/screen2.html"')
    html = html.replace('data-path="clause-breakdown-and-benchmarks" href="#"', 'data-path="clause-breakdown-and-benchmarks" id="nav-step-3" href="/screen3.html"')
    html = html.replace('data-path="counter-proposal-draft" href="#"', 'data-path="counter-proposal-draft" id="nav-step-4" href="/screen4.html"')
    html = html.replace('data-path="attorney-prep-sheet" href="#"', 'data-path="attorney-prep-sheet" id="nav-step-5" href="/screen5.html"')

    # Replace hardcoded questions script with dynamic attorney prep fetching
    new_script = """<script>
  (function initDynamicPrepSheet() {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get('session');

    if (!sessionId) {
      alert('No active session found. Redirecting to upload.');
      window.location.href = '/screen1.html';
      return;
    }

    // Thread session across navigation
    ['nav-step-1', 'nav-step-2', 'nav-step-3', 'nav-step-4', 'nav-step-5'].forEach((id, idx) => {
      const el = document.getElementById(id);
      if (el) el.href = `/screen${idx+1}.html?session=${sessionId}`;
    });

    const checkedCountEl = document.getElementById('checkedCount');
    const notesArea = document.getElementById('meetingNotes');
    const charCountEl = document.getElementById('charCount');
    const clearNotesBtn = document.getElementById('clearNotesBtn');
    const copyBtn = document.getElementById('copyQuestionsBtn');
    const copyBtnText = document.getElementById('copyBtnText');
    const emailBtn = document.getElementById('emailSummaryBtn');
    const exportBtn = document.getElementById('exportPdfBtn');
    const questionsContainer = document.getElementById('questionsContainer');
    const docTitle = document.querySelector('header span.truncate');

    let prepData = null;

    fetch(`/api/attorney_prep/${sessionId}`)
      .then(r => r.json())
      .then(data => {
        prepData = data;
        renderPrep(data);
      })
      .catch(err => {
        console.error('Error fetching attorney prep:', err);
      });

    function renderPrep(data) {
      if (docTitle) docTitle.textContent = data.agreement_name;

      // Update header metrics
      const headerStats = document.querySelectorAll('.header-meta-stat');
      if (headerStats.length >= 3) {
        headerStats[0].textContent = `${data.estimated_call_minutes[0]}-${data.estimated_call_minutes[1]} min`;
        headerStats[1].textContent = data.jurisdiction;
        headerStats[2].textContent = `${data.questions.length} Flagged Topics`;
      }

      if (!questionsContainer) return;
      questionsContainer.innerHTML = '';

      let totalQuestions = 0;
      data.questions.forEach((qGroup, gIdx) => {
        const prioColor = qGroup.priority === 'high' ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' : 'bg-amber-500/10 text-amber-400 border-amber-500/30';
        
        let qItemsHtml = '';
        qGroup.questions.forEach((q, qIdx) => {
          totalQuestions++;
          qItemsHtml += `
          <label class="flex items-start gap-3 p-3 rounded-xl bg-surface/60 border border-outline-variant/30 hover:border-outline-variant/60 cursor-pointer transition-colors">
            <input type="checkbox" class="prep-check mt-1 rounded text-primary focus:ring-primary h-4 w-4 bg-surface border-outline-variant" />
            <span class="text-sm text-on-surface leading-snug">${q}</span>
          </label>`;
        });

        const groupCard = `
        <div class="p-6 rounded-2xl bg-surface-container border border-outline-variant/40 mb-6">
          <div class="flex items-center justify-between mb-3">
            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold border ${prioColor}">${qGroup.priority.toUpperCase()} PRIORITY</span>
            <span class="text-xs text-on-surface-variant font-mono">Clause ID: ${qGroup.clause_id}</span>
          </div>
          <h3 class="text-base font-bold text-on-surface mb-2">${qGroup.section}</h3>
          <p class="text-xs text-on-surface-variant mb-4 bg-surface/50 p-2.5 rounded-lg border border-outline-variant/20">${qGroup.rationale}</p>
          <div class="space-y-2.5">
            ${qItemsHtml}
          </div>
        </div>`;

        questionsContainer.insertAdjacentHTML('beforeend', groupCard);
      });

      // Update counter
      function updateCount() {
        const checkboxes = document.querySelectorAll('.prep-check');
        const checked = Array.from(checkboxes).filter(cb => cb.checked).length;
        if (checkedCountEl) checkedCountEl.textContent = `${checked} of ${totalQuestions}`;
      }

      document.querySelectorAll('.prep-check').forEach(cb => {
        cb.addEventListener('change', updateCount);
      });
      updateCount();
    }

    // LocalStorage Notes
    if (notesArea && charCountEl) {
      const savedNotes = localStorage.getItem(`clausepilot_notes_${sessionId}`);
      if (savedNotes) {
        notesArea.value = savedNotes;
        charCountEl.textContent = `${savedNotes.length} characters`;
      }

      notesArea.addEventListener('input', () => {
        const len = notesArea.value.length;
        charCountEl.textContent = `${len} characters`;
        localStorage.setItem(`clausepilot_notes_${sessionId}`, notesArea.value);
      });
    }

    if (clearNotesBtn && notesArea) {
      clearNotesBtn.addEventListener('click', () => {
        notesArea.value = '';
        if (charCountEl) charCountEl.textContent = '0 characters';
        localStorage.removeItem(`clausepilot_notes_${sessionId}`);
      });
    }

    // Copy Questions
    if (copyBtn && copyBtnText) {
      copyBtn.addEventListener('click', () => {
        if (!prepData) return;
        let lines = [`Contract Consultation: ${prepData.agreement_name} (${prepData.jurisdiction})`, ''];
        prepData.questions.forEach(qg => {
          lines.push(`--- ${qg.section} (${qg.priority.toUpperCase()}) ---`);
          lines.push(`Risk: ${qg.rationale}`);
          qg.questions.forEach(q => lines.push(`- ${q}`));
          lines.push('');
        });

        navigator.clipboard.writeText(lines.join('\\n')).then(() => {
          copyBtnText.textContent = 'Copied to Clipboard!';
          setTimeout(() => { copyBtnText.textContent = 'Copy Questions'; }, 2000);
        });
      });
    }

    // Email
    if (emailBtn) {
      emailBtn.addEventListener('click', () => {
        if (!prepData) return;
        const subject = encodeURIComponent(`Attorney Consultation Prep - ${prepData.agreement_name}`);
        const body = encodeURIComponent(`Hello,\n\nPlease find prepared below the key flagged clauses and questions for our upcoming contract review session regarding ${prepData.agreement_name}.\n\nEstimated time: ${prepData.estimated_call_minutes[0]}-${prepData.estimated_call_minutes[1]} min.\n\nBest regards,`);
        window.location.href = `mailto:?subject=${subject}&body=${body}`;
      });
    }

    if (exportBtn) {
      exportBtn.addEventListener('click', () => {
        window.print();
      });
    }
  })();
</script>"""

    # Replace hardcoded questions container with dynamic hook
    html = re.sub(r'<div class="flex items-center gap-3">.*?<div class="space-y-6">.*?</div>\s*</div>\s*(?=<div class="lg:col-span-1)', '<div id="questionsContainer" class="space-y-4"></div>', html, flags=re.DOTALL)
    html = re.sub(r'<script>\s*\(function initPrepSheet\(\).*?</script>', new_script, html, flags=re.DOTALL)

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Wired screen5.html")

if __name__ == "__main__":
    wire_screen1()
    wire_screen2()
    wire_screen3()
    wire_screen4()
    wire_screen5()
    print("All 5 screens wired successfully!")
