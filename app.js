/**
 * Database Visualizer & Interactive Video Engine
 */

// Application State
const state = {
  currentScene: 0,
  isPlaying: false,
  autoPlayInterval: null,
  soundEnabled: true,
  audioCtx: null,
  scenes: [
    {
      id: 'scene-intro',
      title: 'What is a Database & Application Data Flow',
      badge: 'STEP 1 OF 4',
      duration: 5000
    },
    {
      id: 'scene-create',
      title: 'Step 1: CREATE TABLE EMPLOYEE (Schema Blueprint)',
      badge: 'STEP 2 OF 4',
      duration: 5000
    },
    {
      id: 'scene-insert',
      title: 'Step 2: Storing Data (INSERT INTO EMPLOYEE)',
      badge: 'STEP 3 OF 4',
      duration: 5500
    },
    {
      id: 'scene-select',
      title: 'Step 3: Retrieving Data (SELECT WHERE dept = \'Sales\')',
      badge: 'STEP 4 OF 4',
      duration: 6000
    }
  ],
  // Simulated DB Store
  database: [
    { empId: 1, name: 'Clark', dept: 'Sales' },
    { empId: 2, name: 'Dave', dept: 'Accounting' },
    { empId: 3, name: 'Ava', dept: 'Sales' }
  ]
};

// Web Audio API Sound Generator
function playTone(freq = 440, type = 'sine', duration = 0.12, volume = 0.1) {
  if (!state.soundEnabled) return;
  try {
    if (!state.audioCtx) {
      state.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (state.audioCtx.state === 'suspended') {
      state.audioCtx.resume();
    }
    const osc = state.audioCtx.createOscillator();
    const gain = state.audioCtx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, state.audioCtx.currentTime);
    gain.gain.setValueAtTime(volume, state.audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, state.audioCtx.currentTime + duration);
    osc.connect(gain);
    gain.connect(state.audioCtx.destination);
    osc.start();
    osc.stop(state.audioCtx.currentTime + duration);
  } catch (e) {
    // Audio might fail without user interaction, ignore safely
  }
}

// Sound presets
const SFX = {
  click: () => playTone(580, 'sine', 0.08, 0.05),
  next: () => {
    playTone(520, 'sine', 0.09, 0.06);
    setTimeout(() => playTone(780, 'triangle', 0.14, 0.06), 80);
  },
  insert: () => {
    playTone(330, 'triangle', 0.1, 0.08);
    setTimeout(() => playTone(660, 'sine', 0.15, 0.07), 100);
  },
  match: () => {
    playTone(523.25, 'sine', 0.1, 0.08);
    setTimeout(() => playTone(659.25, 'sine', 0.1, 0.08), 80);
    setTimeout(() => playTone(783.99, 'sine', 0.2, 0.08), 160);
  }
};

// Navigation View Tabs
function switchView(viewName) {
  SFX.click();
  document.querySelectorAll('.view-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

  const targetView = document.getElementById(`view-${viewName}`);
  const targetBtn = document.getElementById(`btn-tab-${viewName}`);
  if (targetView) targetView.classList.add('active');
  if (targetBtn) targetBtn.classList.add('active');

  if (viewName === 'interactive') {
    renderLabTable();
  }
}

// Scene Transitions in Video Player
function jumpToScene(index) {
  if (index < 0) index = 0;
  if (index >= state.scenes.length) index = state.scenes.length - 1;

  state.currentScene = index;
  const sceneData = state.scenes[index];

  // Update DOM classes
  document.querySelectorAll('.scene').forEach(s => s.classList.remove('active'));
  const activeSceneElem = document.getElementById(sceneData.id);
  if (activeSceneElem) activeSceneElem.classList.add('active');

  // Update Header text
  document.getElementById('video-scene-title').textContent = sceneData.title;
  document.getElementById('video-step-badge').textContent = sceneData.badge;

  // Update Timeline steps
  document.querySelectorAll('.timeline-step').forEach((st, idx) => {
    if (idx <= index) {
      st.classList.add('active');
    } else {
      st.classList.remove('active');
    }
  });

  // Update Progress fill
  const pct = ((index + 1) / state.scenes.length) * 100;
  document.getElementById('timeline-progress-fill').style.width = `${pct}%`;

  // Play audio chime
  SFX.next();

  // Trigger scene-specific animations
  triggerSceneAnimation(index);
}

function triggerSceneAnimation(index) {
  if (index === 2) { // INSERT scene
    const rows = ['row-clark', 'row-dave', 'row-ava'];
    rows.forEach((rId, i) => {
      const el = document.getElementById(rId);
      if (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(12px)';
        setTimeout(() => {
          el.style.transition = 'all 0.4s ease';
          el.style.opacity = '1';
          el.style.transform = 'translateY(0)';
          SFX.insert();
        }, (i + 1) * 350);
      }
    });
  } else if (index === 3) { // SELECT scene
    const evalRows = ['eval-row-1', 'eval-row-2', 'eval-row-3'];
    evalRows.forEach((rId, i) => {
      const el = document.getElementById(rId);
      if (el) {
        el.style.opacity = '0.3';
        setTimeout(() => {
          el.style.opacity = '1';
          if (rId.includes('2')) {
            playTone(250, 'sawtooth', 0.15, 0.05); // Filtered buzz
          } else {
            SFX.match(); // Match chime
          }
        }, (i + 1) * 500);
      }
    });
  }
}

// Auto-Play Tour Controller
function togglePlayPause() {
  if (state.isPlaying) {
    stopAutoPlay();
  } else {
    startAutoPlay();
  }
}

function startAutoPlay() {
  state.isPlaying = true;
  document.getElementById('play-icon').textContent = '⏸';
  document.getElementById('play-text').textContent = 'Pause Tour';
  SFX.click();

  function advance() {
    if (!state.isPlaying) return;
    let nextIndex = state.currentScene + 1;
    if (nextIndex >= state.scenes.length) {
      nextIndex = 0; // loop back
    }
    jumpToScene(nextIndex);
    const duration = state.scenes[nextIndex].duration;
    state.autoPlayInterval = setTimeout(advance, duration);
  }

  const currentDuration = state.scenes[state.currentScene].duration;
  state.autoPlayInterval = setTimeout(advance, currentDuration);
}

function stopAutoPlay() {
  state.isPlaying = false;
  if (state.autoPlayInterval) {
    clearTimeout(state.autoPlayInterval);
    state.autoPlayInterval = null;
  }
  document.getElementById('play-icon').textContent = '▶';
  document.getElementById('play-text').textContent = 'Auto-Play Tour';
  SFX.click();
}

function nextScene() {
  stopAutoPlay();
  jumpToScene(state.currentScene + 1);
}

function prevScene() {
  stopAutoPlay();
  jumpToScene(state.currentScene - 1);
}

function restartTour() {
  stopAutoPlay();
  jumpToScene(0);
}

function toggleSound() {
  state.soundEnabled = !state.soundEnabled;
  const btn = document.getElementById('btn-sound-toggle');
  btn.textContent = state.soundEnabled ? '🔊' : '🔇';
  if (state.soundEnabled) SFX.click();
}

// ==========================================================================
// Interactive Lab (SQL Simulator)
// ==========================================================================

function renderLabTable() {
  const tbody = document.getElementById('lab-table-body');
  if (!tbody) return;
  tbody.innerHTML = '';

  state.database.forEach(row => {
    const tr = document.createElement('tr');
    tr.className = 'row-card';
    tr.innerHTML = `
      <td><span class="code-chip">${String(row.empId).padStart(4, '0')}</span></td>
      <td><strong>${row.name}</strong></td>
      <td><span class="dept-pill ${row.dept.toLowerCase() === 'sales' ? 'sales' : 'acct'}">${row.dept}</span></td>
    `;
    tbody.appendChild(tr);
  });

  const countBadge = document.getElementById('lab-row-count');
  if (countBadge) countBadge.textContent = `${state.database.length} Rows Stored`;
}

function setQuery(sql) {
  const editor = document.getElementById('sql-editor');
  if (editor) {
    editor.value = sql;
    SFX.click();
  }
}

function logConsole(msg, isError = false) {
  const consoleEl = document.getElementById('console-logs');
  if (consoleEl) {
    consoleEl.textContent = msg;
    consoleEl.style.color = isError ? 'var(--accent-red)' : 'var(--accent-green)';
  }
}

function executeCustomSql() {
  const sqlInput = document.getElementById('sql-editor').value.trim();
  SFX.click();

  if (!sqlInput) {
    logConsole('Error: SQL statement is empty.', true);
    return;
  }

  // Basic SQL interpreter simulation
  const normalized = sqlInput.toLowerCase().replace(/;/g, '');

  if (normalized.startsWith('select')) {
    handleSelectQuery(sqlInput, normalized);
  } else if (normalized.startsWith('insert into')) {
    handleInsertQuery(sqlInput);
  } else if (normalized.startsWith('create table')) {
    logConsole('Table EMPLOYEE created or already exists.', false);
  } else {
    logConsole(`Executed query: ${sqlInput} (1 row affected)`, false);
  }
}

function handleSelectQuery(rawSql, normSql) {
  let results = [...state.database];

  // Check for WHERE dept = '...'
  const whereMatch = rawSql.match(/where\s+dept\s*=\s*['"]([^'"]+)['"]/i);
  if (whereMatch) {
    const targetDept = whereMatch[1].trim();
    results = results.filter(r => r.dept.toLowerCase() === targetDept.toLowerCase());
  }

  // Render results
  const resContainer = document.getElementById('lab-results-view');
  const countBadge = document.getElementById('lab-res-count');
  if (!resContainer) return;

  if (results.length === 0) {
    resContainer.innerHTML = '<div class="empty-state">0 records matched your query condition.</div>';
    if (countBadge) countBadge.textContent = '0 Rows Returned';
    logConsole(`Query executed successfully: 0 records returned.`, false);
    return;
  }

  let html = `
    <table class="db-table">
      <thead>
        <tr>
          <th>empId</th>
          <th>name</th>
          <th>dept</th>
        </tr>
      </thead>
      <tbody>
  `;

  results.forEach(r => {
    html += `
      <tr class="eval-row match">
        <td><span class="code-chip">${r.empId}</span></td>
        <td><strong>${r.name}</strong></td>
        <td><span class="dept-pill ${r.dept.toLowerCase() === 'sales' ? 'sales' : 'acct'}">${r.dept}</span></td>
      </tr>
    `;
  });

  html += `</tbody></table>`;
  resContainer.innerHTML = html;
  if (countBadge) countBadge.textContent = `${results.length} Rows Returned`;
  logConsole(`Query executed successfully: ${results.length} rows retrieved in 0.11 ms.`, false);
  SFX.match();
}

function handleInsertQuery(rawSql) {
  // Regex match VALUES (id, 'name', 'dept')
  const valMatch = rawSql.match(/values\s*\(\s*(\d+)\s*,\s*['"]([^'"]+)['"]\s*,\s*['"]([^'"]+)['"]\s*\)/i);
  if (valMatch) {
    const newId = parseInt(valMatch[1], 10);
    const newName = valMatch[2].trim();
    const newDept = valMatch[3].trim();

    // Check primary key duplicate
    if (state.database.some(r => r.empId === newId)) {
      logConsole(`Error: PRIMARY KEY constraint violation. empId ${newId} already exists!`, true);
      playTone(200, 'sawtooth', 0.2, 0.1);
      return;
    }

    state.database.push({ empId: newId, name: newName, dept: newDept });
    renderLabTable();
    logConsole(`INSERT complete: 1 row added (${newId}, '${newName}', '${newDept}'). Table size: ${state.database.length}.`, false);
    SFX.insert();
  } else {
    logConsole('Syntax Error in INSERT statement. Format: INSERT INTO EMPLOYEE VALUES (0004, \'Name\', \'Dept\');', true);
  }
}

function resetDatabase() {
  state.database = [
    { empId: 1, name: 'Clark', dept: 'Sales' },
    { empId: 2, name: 'Dave', dept: 'Accounting' },
    { empId: 3, name: 'Ava', dept: 'Sales' }
  ];
  renderLabTable();
  logConsole('Database reset to initial 3 records (Clark, Dave, Ava).', false);
  SFX.click();
}

// Initial Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('btn-play-pause')?.addEventListener('click', togglePlayPause);
  document.getElementById('btn-next-scene')?.addEventListener('click', nextScene);
  document.getElementById('btn-prev-scene')?.addEventListener('click', prevScene);
  document.getElementById('btn-restart')?.addEventListener('click', restartTour);
  document.getElementById('btn-sound-toggle')?.addEventListener('click', toggleSound);

  // Keyboard shortcut: Space to play/pause, Arrow keys for scenes
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT') return;
    if (e.code === 'Space') {
      e.preventDefault();
      togglePlayPause();
    } else if (e.code === 'ArrowRight') {
      nextScene();
    } else if (e.code === 'ArrowLeft') {
      prevScene();
    }
  });

  renderLabTable();
  jumpToScene(0);
});
