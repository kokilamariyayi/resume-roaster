// ===== Constants & System Prompt =====
const GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions';
const MODEL = 'llama-3.3-70b-versatile';

const SYSTEM_PROMPT = `You are an advanced AI Resume Intelligence System designed to perform multi-level analysis, role inference, and career optimization.

---

CORE OBJECTIVES:
1. Detect most suitable roles from resume (even if role is provided)
2. Suggest role from JD (if JD exists)
3. Perform deep resume analysis
4. Provide actionable improvements
5. Track improvement context if history exists

---

STEP 1: PREPROCESSING
- Extract and normalize structured sections: Summary, Skills, Projects, Experience, Education.

---

STEP 2: ROLE INTELLIGENCE
A. Resume-based Role Detection:
- Infer top 3 suitable roles from resume with confidence scores (%).
B. JD-based Role Suggestion (ONLY if MODE = WITH_JD):
- Infer most relevant role from Job Description with confidence score.
C. Role Alignment Logic:
- Compare TARGET_ROLE with inferred roles and highlight mismatches.

---

STEP 3: ANALYSIS LOGIC
IF MODE = WITH_JD:
- Compute ATS Match Score (0-100), Keyword Match %, and Semantic Alignment.
IF MODE = WITHOUT_JD:
- Evaluate ATS readiness and market competitiveness against industry benchmarks.

---

STEP 4: SECTION-WISE CRITIQUE
For each section: Identify weakness, explain why, and provide specific fix.

---

STEP 5: BULLET OPTIMIZATION
- Rewrite at least 3 weak bullet points into Action-driven, Metric-based, and Tool-specific statements.

---

STEP 6: SKILL GAP ANALYSIS
- Identify missing Must-have and Good-to-have skills.

---

STEP 7: PROJECT RECOMMENDATION ENGINE
- Suggest 2-3 projects aligned with missing skills and target role.

---

STEP 8: SCORE HISTORY ANALYSIS (If USER_HISTORY exists)
- Compare current ATS score with past scores and provide trend insights.

---

STEP 9: FINAL OUTPUT FORMAT (STRICT)

1. Detected Roles (from Resume):
   - Role 1 (Confidence %)
   - Role 2 (Confidence %)
   - Role 3 (Confidence %)

2. Suggested Role (from JD, if available):

3. Role Alignment Insight:
   - Match / Mismatch explanation

4. ATS Score:
5. Role Match Score:

6. Key Gaps:
   - ...

7. Section-wise Feedback:
   - Summary:
   - Skills:
   - Projects:
   - Experience:

8. Improved Bullet Points:
   - Before:
   - After:

9. Missing Skills:
   - Must-have:
   - Good-to-have:

10. Recommended Projects:
   - ...

11. Score Trend (if history provided):

12. Final Verdict:
   - Direct, critical, and actionable

---

CONSTRAINTS:
- Avoid generic statements.
- Be critical but constructive.
- Focus on real-world hiring relevance.
- Prioritize actionable insights.`;

// ===== DOM Elements =====
const apiKeyInput = document.getElementById('apiKeyInput');
const targetRoleInput = document.getElementById('targetRole');
const resumeTextInput = document.getElementById('resumeText');
const jdTextInput = document.getElementById('jdText');
const jdGroup = document.getElementById('jdGroup');
const modeInfo = document.getElementById('modeInfo');
const modeWithoutJdBtn = document.getElementById('modeWithoutJdBtn');
const modeWithJdBtn = document.getElementById('modeWithJdBtn');
const generateBtn = document.getElementById('generateBtn');
const resultsSection = document.getElementById('resultsSection');
const reportContent = document.getElementById('reportContent');
const historyList = document.getElementById('historyList');
const copyBtn = document.getElementById('copyBtn');
const toast = document.getElementById('toast');

// State
let currentMode = 'WITHOUT_JD';

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', () => {
    initParticles();
    setupEventListeners();
    renderHistory();
    
    // Load saved API key if exists
    const savedKey = localStorage.getItem('GROQ_API_KEY');
    if (savedKey) apiKeyInput.value = savedKey;
});

// ===== Background Particles =====
function initParticles() {
    const container = document.getElementById('bgParticles');
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 8 + 's';
        particle.style.animationDuration = (8 + Math.random() * 10) + 's';
        particle.style.opacity = 0.1 + Math.random() * 0.3;
        particle.style.width = particle.style.height = (3 + Math.random() * 5) + 'px';
        container.appendChild(particle);
    }
}

// ===== Event Listeners =====
function setupEventListeners() {
    // Mode toggles
    modeWithoutJdBtn.addEventListener('click', () => setMode('WITHOUT_JD'));
    modeWithJdBtn.addEventListener('click', () => setMode('WITH_JD'));

    // Save API key on blur
    apiKeyInput.addEventListener('blur', () => {
        if (apiKeyInput.value.trim()) {
            localStorage.setItem('GROQ_API_KEY', apiKeyInput.value.trim());
        }
    });

    // Generate
    generateBtn.addEventListener('click', handleGenerate);
    
    // Copy
    copyBtn.addEventListener('click', handleCopy);
}

function setMode(mode) {
    currentMode = mode;
    if (mode === 'WITH_JD') {
        modeWithJdBtn.classList.add('active');
        modeWithoutJdBtn.classList.remove('active');
        modeWithJdBtn.querySelector('input').checked = true;
        jdGroup.style.display = 'block';
        modeInfo.style.display = 'none';
    } else {
        modeWithoutJdBtn.classList.add('active');
        modeWithJdBtn.classList.remove('active');
        modeWithoutJdBtn.querySelector('input').checked = true;
        jdGroup.style.display = 'none';
        modeInfo.style.display = 'block';
    }
}

// ===== History Management =====
function getHistory() {
    return JSON.parse(localStorage.getItem('career_history') || '[]');
}

function saveHistory(role, score, mode) {
    const history = getHistory();
    history.push({
        date: new Date().toLocaleString([], { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }),
        role: role,
        score: score,
        mode: mode
    });
    
    // Keep only last 5
    if (history.length > 5) history.shift();
    
    localStorage.setItem('career_history', JSON.stringify(history));
    renderHistory();
}

function renderHistory() {
    const history = getHistory();
    if (history.length === 0) {
        historyList.innerHTML = '<div class="empty-history">No history found. Start your first analysis!</div>';
        return;
    }

    historyList.innerHTML = '';
    // Reverse to show newest first
    [...history].reverse().forEach(entry => {
        historyList.innerHTML += `
            <div class="metric-card">
                <div class="metric-title">${escapeHtml(entry.role)}</div>
                <div class="metric-score">Score: ${escapeHtml(entry.score)}</div>
                <div class="metric-date">🕒 ${entry.date} • ${entry.mode.replace('_', ' ')}</div>
            </div>
        `;
    });
}

// ===== Toast Notifications =====
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = 'toast show toast-' + type;
    setTimeout(() => {
        toast.className = 'toast';
    }, 3000);
}

// ===== Generate Logic =====
async function handleGenerate() {
    const apiKey = apiKeyInput.value.trim();
    const targetRole = targetRoleInput.value.trim();
    const resumeText = resumeTextInput.value.trim();
    const jdText = jdTextInput.value.trim();

    // Validation
    if (!apiKey) {
        showToast('Please enter your Groq API Key', 'error');
        apiKeyInput.focus();
        return;
    }
    if (!targetRole) {
        showToast('Please specify a Target Role', 'error');
        targetRoleInput.focus();
        return;
    }
    if (!resumeText) {
        showToast('Please paste your Resume content', 'error');
        resumeTextInput.focus();
        return;
    }
    if (currentMode === 'WITH_JD' && !jdText) {
        showToast('Please paste the Job Description', 'error');
        jdTextInput.focus();
        return;
    }

    setLoading(true);
    resultsSection.style.display = 'none';

    try {
        const historyJson = JSON.stringify(getHistory());
        
        const userContent = `
MODE: ${currentMode}
TARGET_ROLE: ${targetRole}
RESUME_INPUT: ${resumeText}
JOB_DESCRIPTION_INPUT: ${currentMode === 'WITH_JD' ? jdText : ''}
USER_HISTORY: ${historyJson}
`;

        const response = await fetch(GROQ_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`,
            },
            body: JSON.stringify({
                model: MODEL,
                messages: [
                    { role: 'system', content: SYSTEM_PROMPT },
                    { role: 'user', content: userContent },
                ],
                temperature: 0.85,
                max_tokens: 3000,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData?.error?.message || `API request failed (${response.status})`);
        }

        const data = await response.json();
        const resultText = data.choices[0].message.content;

        // Parse Markdown to HTML
        reportContent.innerHTML = marked.parse(resultText);
        
        // Extract Score for History
        let score = "N/A";
        const scoreMatch = resultText.match(/ATS Score:\s*(\d+)/i);
        if (scoreMatch) {
            score = scoreMatch[1];
        }

        saveHistory(targetRole, score, currentMode);
        
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        showToast('✨ Analysis Complete!');

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        setLoading(false);
    }
}

function handleCopy() {
    const text = reportContent.innerText;
    navigator.clipboard.writeText(text).then(() => {
        showToast('✓ Report copied to clipboard!');
    }).catch(() => {
        showToast('Failed to copy', 'error');
    });
}

// ===== Helpers =====
function setLoading(isLoading) {
    const btnContent = generateBtn.querySelector('.btn-content');
    const btnLoading = generateBtn.querySelector('.btn-loading');

    if (isLoading) {
        btnContent.style.display = 'none';
        btnLoading.style.display = 'flex';
        generateBtn.disabled = true;
    } else {
        btnContent.style.display = 'flex';
        btnLoading.style.display = 'none';
        generateBtn.disabled = false;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
