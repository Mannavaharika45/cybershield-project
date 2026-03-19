const API_BASE_URL = 'https://cybershield-project-7e4c.onrender.com';

// Utility element selectors
const getEl = id => document.getElementById(id);

// Configs for icons and colors based on classification
const themeConfig = {
    fake: { icon: 'fa-triangle-exclamation', color: 'bg-red-500', text: 'text-red-400', glow: 'text-glow-red' },
    real: { icon: 'fa-check', color: 'bg-green-500', text: 'text-green-400', glow: 'text-glow-green' },
    scam: { icon: 'fa-biohazard', color: 'bg-orange-500', text: 'text-orange-400', glow: 'text-glow-red' },
    safe: { icon: 'fa-shield-check', color: 'bg-blue-500', text: 'text-blue-400', glow: 'text-glow-blue' },
    phishing: { icon: 'fa-radiation', color: 'bg-purple-600', text: 'text-purple-400', glow: 'text-glow-red' },
    legit: { icon: 'fa-lock', color: 'bg-teal-500', text: 'text-teal-400', glow: 'text-glow-green' }
};

// Generic UI toggler
function toggleState(containerId, state) {
    const states = ['DefaultState', 'LoadingState', 'Analysis'];
    // Specifically crafted for our ID naming conventions (e.g., scamDefaultState)
    const prefix = containerId.replace('ResultContainer', '');

    states.forEach(s => {
        const el = getEl(prefix + s);
        if (el) {
            if (s === state) {
                el.classList.remove('hidden');
            } else {
                el.classList.add('hidden');
            }
        }
    });
}

// Render Results Generic
function renderResult(prefix, data, type) {
    let theme;
    if (type === 'fake_news') theme = data.is_fake ? themeConfig.fake : themeConfig.real;
    else if (type === 'scam') theme = data.is_scam ? themeConfig.scam : themeConfig.safe;
    else if (type === 'phishing') theme = data.is_phishing ? themeConfig.phishing : themeConfig.legit;

    // Label
    const labelEl = getEl(prefix + 'ResultLabel');
    if (labelEl) {
        labelEl.innerText = data.label;
        labelEl.className = `text-2xl lg:text-3xl font-bold ${theme.text} ${theme.glow}`;
    }

    // Icon
    const iconEl = getEl(prefix + 'IconBadge');
    if (iconEl) {
        iconEl.className = `w-12 h-12 rounded-full flex items-center justify-center text-xl text-white shadow-lg ${theme.color}`;
        iconEl.innerHTML = `<i class="fa-solid ${theme.icon}"></i>`;
    }

    // Confidence Bar
    const confText = getEl(prefix + 'ConfidenceText');
    const confBar = getEl(prefix + 'ConfidenceBar');
    if (confText && confBar) {
        const score = typeof data.confidence !== 'undefined' ? data.confidence : data.risk_score;
        confText.innerText = `${score}${type === 'phishing' ? ' / 100' : '%'}`;

        // Reset animation
        confBar.style.width = '0%';
        confBar.className = `h-full rounded-full score-fill transition-all duration-1000 w-0 ${theme.color}`;

        setTimeout(() => {
            confBar.style.width = `${score}%`;
        }, 100);
    }

    // Switch state
    toggleState(prefix + 'ResultContainer', 'Analysis');
}

/* ================== FAKE NEWS DETECTION ================== */
const newsInput = getEl('newsInput');
const analyzeBtn = getEl('analyzeBtn');
const clearBtn = getEl('clearBtn');

if (analyzeBtn && newsInput) {
    analyzeBtn.addEventListener('click', async () => {
        const text = newsInput.value.trim();
        if (!text) return alert("Please enter text to analyze.");

        toggleState('ResultContainer', 'LoadingState');

        try {
            const token = localStorage.getItem('cybershield_token') || '';
            const res = await fetch(`${API_BASE_URL}/api/detect-fake-news`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ text })
            });
            const data = await res.json();
            renderResult('', data, 'fake_news');
        } catch (err) {
            console.error(err);
            alert("Connection error to detection engine.");
            toggleState('ResultContainer', 'DefaultState');
        }
    });

    clearBtn.addEventListener('click', () => {
        newsInput.value = '';
        toggleState('ResultContainer', 'DefaultState');
    });
}

/* ================== SCAM MESSAGE DETECTION ================== */
const scamInput = getEl('scamInput');
const analyzeScamBtn = getEl('analyzeScamBtn');
const clearScamBtn = getEl('clearScamBtn');

if (analyzeScamBtn && scamInput) {
    analyzeScamBtn.addEventListener('click', async () => {
        const text = scamInput.value.trim();
        if (!text) return alert("Please enter a message to analyze.");

        toggleState('scamResultContainer', 'LoadingState');

        try {
            const token = localStorage.getItem('cybershield_token') || '';
            const res = await fetch(`${API_BASE_URL}/api/detect-scam`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ text })
            });
            const data = await res.json();
            renderResult('scam', data, 'scam');
        } catch (err) {
            console.error(err);
            alert("Connection error to detection engine.");
            toggleState('scamResultContainer', 'DefaultState');
        }
    });

    clearScamBtn.addEventListener('click', () => {
        scamInput.value = '';
        toggleState('scamResultContainer', 'DefaultState');
    });
}

/* ================== PHISHING LINK SCANNER ================== */
const urlInput = getEl('urlInput');
const analyzeUrlBtn = getEl('analyzeUrlBtn');
const clearUrlBtn = getEl('clearUrlBtn');
const urlFindingsList = getEl('urlFindingsList');

if (analyzeUrlBtn && urlInput) {
    analyzeUrlBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        if (!url) return alert("Please enter a URL to scan.");

        // Basic frontend validation
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            alert("URL must start with http:// or https://");
            return;
        }

        toggleState('urlResultContainer', 'LoadingState');

        try {
            const token = localStorage.getItem('cybershield_token') || '';
            const res = await fetch(`${API_BASE_URL}/api/detect-phishing`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ url })
            });
            const data = await res.json();

            // Populate reasons list
            if (urlFindingsList) {
                urlFindingsList.innerHTML = '';
                data.reasons.forEach(r => {
                    const li = document.createElement('li');
                    li.innerText = r;
                    if (data.is_phishing) li.classList.add('text-red-400');
                    else li.classList.add('text-green-400');
                    urlFindingsList.appendChild(li);
                });
            }

            renderResult('url', data, 'phishing');
        } catch (err) {
            console.error(err);
            alert("Connection error to detection engine.");
            toggleState('urlResultContainer', 'DefaultState');
        }
    });

    clearUrlBtn.addEventListener('click', () => {
        urlInput.value = '';
        toggleState('urlResultContainer', 'DefaultState');
    });
}


/* ================== SCREENSHOT OCR PATROL ================== */
const dropZone = getEl('dropZone');
const fileInput = getEl('fileInput');
const imagePreviewContainer = getEl('imagePreviewContainer');
const imagePreview = getEl('imagePreview');
const removeImageBtn = getEl('removeImageBtn');
const analyzeImageBtn = getEl('analyzeImageBtn');
const extractedTextContent = getEl('extractedTextContent');

let selectedFile = null;

if (dropZone && fileInput) {
    // Drag and Drop Aesthetics
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('border-teal-400'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('border-teal-400'), false);
    });

    // Handle Drop
    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });

    // Handle Click Selection
    fileInput.addEventListener('change', function () {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length === 0) return;

        const file = files[0];
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file (PNG/JPG).');
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            alert('File is too large. Max size is 5MB.');
            return;
        }

        selectedFile = file;

        // Show Preview
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreviewContainer.classList.remove('hidden');
            imagePreviewContainer.classList.add('flex');

            analyzeImageBtn.removeAttribute('disabled');
        }
        reader.readAsDataURL(file);
    }

    removeImageBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // prevent clicking dropzone
        resetUploader();
    });

    function resetUploader() {
        selectedFile = null;
        fileInput.value = '';
        imagePreviewContainer.classList.add('hidden');
        imagePreviewContainer.classList.remove('flex');
        analyzeImageBtn.setAttribute('disabled', 'true');
        toggleState('ocrResultContainer', 'DefaultState');
    }

    analyzeImageBtn.addEventListener('click', async () => {
        if (!selectedFile) return;

        toggleState('ocrResultContainer', 'LoadingState');

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const token = localStorage.getItem('cybershield_token') || '';
            const res = await fetch(`${API_BASE_URL}/api/analyze-screenshot`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` },
                body: formData
            });
            const data = await res.json();

            if (res.status !== 200) {
                alert(data.detail || "Error analyzing image.");
                toggleState('ocrResultContainer', 'DefaultState');
                return;
            }

            // Populate extracted text
            if (extractedTextContent) {
                extractedTextContent.innerText = data.text_extracted || "No text could be extracted.";
            }

            if (data.analysis) {
                renderResult('ocr', data.analysis, 'scam');
            } else {
                if (getEl('ocrAnalysis')) getEl('ocrAnalysis').classList.remove('hidden');
                getEl('ocrResultLabel').innerText = "OCR Failed";
            }

        } catch (err) {
            console.error(err);
            alert("Connection error. Is the backend running?");
            toggleState('ocrResultContainer', 'DefaultState');
        }
    });
}
