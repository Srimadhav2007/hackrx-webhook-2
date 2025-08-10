let queryCounter = 1;

function updateProgress() {
    const totalFields = document.querySelectorAll('input[required]').length;
    const filledFields = Array.from(document.querySelectorAll('input[required]'))
        .filter(input => input.value.trim() !== '').length;
    const progress = (filledFields / totalFields) * 100;
    document.getElementById('progressBar').style.width = progress + '%';
}

function addQueryInput() {
    queryCounter++;
    const queryContainer = document.getElementById('queryContainer');
    const queryGroup = document.createElement('div');
    queryGroup.className = 'query-group';
    queryGroup.setAttribute('data-query-index', queryCounter);
    queryGroup.innerHTML = `
        <div class="d-flex align-items-center gap-3">
            <div class="query-counter">
                <span>${queryCounter}</span>
            </div>
            <div class="floating-label flex-grow-1 mb-0">
                <input 
                    type="text" 
                    name="questions" 
                    placeholder=" " 
                    required
                >
                <label>Enter your query <span class="text-danger">*</span></label>
                <i class="bi bi-chat-square-text input-icon"></i>
            </div>
            <button type="button" class="btn-morphing btn-add" onclick="addQueryInput()">
                <i class="bi bi-plus-lg"></i>
            </button>
            <button type="button" class="btn-morphing btn-remove" onclick="removeQueryInput(this)">
                <i class="bi bi-dash-lg"></i>
            </button>
        </div>
    `;
    queryContainer.appendChild(queryGroup);

    // Add entrance animation
    queryGroup.style.opacity = '0';
    queryGroup.style.transform = 'translateY(-30px) scale(0.8)';
    setTimeout(() => {
        queryGroup.style.transition = 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
        queryGroup.style.opacity = '1';
        queryGroup.style.transform = 'translateY(0) scale(1)';
    }, 10);

    queryGroup.querySelector('input').addEventListener('input', updateProgress);
    updateProgress();
}

function removeQueryInput(button) {
    const queryGroup = button.closest('.query-group');
    const queryContainer = document.getElementById('queryContainer');
    
    if (queryContainer.children.length <= 1) {
        queryGroup.style.animation = 'shake 0.5s ease-in-out';
        setTimeout(() => {
            queryGroup.style.animation = '';
        }, 500);
        return;
    }

    queryGroup.style.transition = 'all 0.4s ease';
    queryGroup.style.opacity = '0';
    queryGroup.style.transform = 'translateX(-100%) scale(0.8)';
    
    setTimeout(() => {
        queryGroup.remove();
        updateQueryCounters();
        updateProgress();
    }, 400);
}

function updateQueryCounters() {
    const queryGroups = document.querySelectorAll('.query-group');
    queryGroups.forEach((group, index) => {
        const counter = group.querySelector('.query-counter span');
        counter.textContent = index + 1;
        group.setAttribute('data-query-index', index + 1);
    });
    queryCounter = queryGroups.length;
}

// Add shake animation
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);

// SINGLE Form submission event listener
document.getElementById('queryForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const form = this;
    const submitBtn = form.querySelector('.btn-submit');
    const loadingDots = document.getElementById('loadingDots');
    const submitText = document.getElementById('submitText');
    const successCheckmark = document.getElementById('successCheckmark');

    // Validation
    const urlInput = document.getElementById('urlInput');
    const queryInputs = document.querySelectorAll('input[name="queries[]"]');
    let isValid = true;

    if (!urlInput.value.trim()) {
        urlInput.style.animation = 'shake 0.5s ease-in-out';
        isValid = false;
    }

    queryInputs.forEach(input => {
        if (!input.value.trim()) {
            input.closest('.query-group').style.animation = 'shake 0.5s ease-in-out';
            isValid = false;
        }
    });

    if (!isValid) return;

    // Clear previous answers
    document.querySelectorAll('.answers').forEach(answer => answer.remove());

    // Loading state
    submitText.style.display = 'none';
    loadingDots.style.display = 'inline-flex';
    submitBtn.disabled = true;

    try {
        const formdata = new FormData(this);
         const jsonData = JSON.stringify(Object.fromEntries(formdata.entries()));
         console.log(jsonData);
        const response = await fetch('/hackrx/run', {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: jsonData
        });

        const data = await response.json();

        // Success animation
        loadingDots.style.display = 'none';
        submitText.innerHTML = '<i class="bi bi-check-lg me-2"></i>Success!';
        submitText.style.display = 'inline';
        submitBtn.style.background = 'var(--success-gradient)';
        successCheckmark.style.display = 'block';

        // Display answers with effects
        data.answers.forEach((element, index) => {
            setTimeout(() => {
                const answer = document.createElement('div');
                answer.className = 'answers';
                answer.innerHTML = `
                    <div class="answer-header">
                        <i class="bi bi-lightbulb-fill"></i>
                        <span>Answer ${index + 1}</span>
                    </div>
                    <div class="answer-content">${element}</div>
                `;
                document.querySelector('.container').appendChild(answer);
                
                // Trigger entrance animation
                setTimeout(() => {
                    answer.classList.add('show');
                }, 50);
            }, index * 300); // Stagger animations
        });

        setTimeout(() => {
            submitBtn.disabled = false;
            submitText.innerHTML = '<i class="bi bi-rocket-takeoff me-2"></i>Launch Query';
            submitBtn.style.background = 'var(--primary-gradient)';
            successCheckmark.style.display = 'none';
        }, 3000);

    } catch (error) {
        console.error("Fetch failed: ", error);
        loadingDots.style.display = 'none';
        submitText.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>Try Again';
        submitText.style.display = 'inline';
        submitBtn.style.background = 'var(--secondary-gradient)';
        submitBtn.disabled = false;
        alert("Something went wrong: " + error.message);
    }
});

// Progress tracking
document.addEventListener('input', function(e) {
    if (e.target.matches('input[required]')) {
        updateProgress();
    }
});

// Initialize progress
updateProgress();