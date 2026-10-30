// Get references to the existing HTML Elements
const ticketForm = document.getElementById('ticket-form');
const descriptionInput = document.getElementById('description');
const characterCount = document.getElementById('char-count');
const analyzeButton = document.getElementById('analyze-button')
const clearButton = document.getElementById('clear-button')
const descriptionError = document.getElementById('description-error');
const formInput = document.getElementById('form-input');

const categoryE = document.getElementById('category');
const priorityE = document.getElementById('priority');
const summaryE = document.getElementById('summary');
const explanationE = document.getElementById('explanation');
const solutionsList = document.getElementById('solutions-list');
const analysisSourceE = document.getElementById('analysis-source');

// Toast functionallity
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toast-message');

function showToast(message, backgroundColor) {
    toastMessage.innerHTML = message;
    toast.style.backgroundColor = backgroundColor;
    toast.classList.add("show");

    setTimeout(function () {
        toast.classList.remove("show");
    }, 3000);
}

// Update the character count as the user types.
descriptionInput.addEventListener('input', function () {
    characterCount.textContent = `${descriptionInput.value.length}/2000`;
    
});

// Handle ticket submission
ticketForm.addEventListener('submit', async function (event) {
    // Stop browser from refreshing the page
    event.preventDefault();

    // Get the description and remove surrounding whitespace
    const description = descriptionInput.value.trim();

    // Prevent empty descriptions from being submitted
    if (!description) {
        showToast('<i class="fas fa-exclamation-triangle"></i> Please enter an issue description', '#ff0000')
        formInput.focus()
        return;
    }

    // Prevent repeated submissions while analysis is running
    analyzeButton.disabled = true;
    analyzeButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...'

    try {
        // Send the description to the Flask API

        const response = await fetch('/api/tickets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                description: description
            })
        });

        // Convert the server response from JSON inot Javascript data
        const data = await response.json();

        // Handle errors returned by Flask
        if (!response.ok) {
            // Display error message in toast
            showToast('<i class="fas fa-exclamation-triangle"></i> An error occurred while analyzing the ticket.', '#ff0000');
            // Throw an error to stop further execution
            throw new Error(data.error || 'An error occurred while analyzing the ticket.');
        }

        // Store the analysis returned by the backend
        const analysis = data.analysis

        // Identify which service produced the analysis
        if (data.analysis_source === 'ai') {
            analysisSourceE.textContent = 'Powered by Ollama LLM - qwen3:1.7b'
        } else {
            analysisSourceE.textContent = 'Rule-Based Analysis'
        }

        // Pupulate existing HTMl Elements
        categoryE.textContent = analysis.category;
        priorityE.textContent = analysis.priority;
        summaryE.textContent = analysis.summary;
        explanationE.textContent = `Explanation: ${analysis.explanation}`;

        // Display the troubleshooting steps
        solutionsList.innerHTML = '';

        analysis.troubleshooting_steps.forEach(function (step) {
            const paragraph = document.createElement('p');
            paragraph.textContent = '- ' + step;
            solutionsList.appendChild(paragraph);
        });

        // Display the toast notification
        showToast('<i class="fas fa-check-circle"></i> Ticket analyzed successfully!', '#008000');
        
    } catch (error) {
        // Display the error message in the toast notification
        showToast('<i class="fas fa-exclamation-circle"></i> An error occurred while analyzing the ticket.', '#ff0000')
        console.log(error)
    } finally {
        // Restore the button after the request finishes
        analyzeButton.disabled = false;
        analyzeButton.innerHTML = 'Analyze Ticket <i class="fas fa-arrow-right"></i>';
    }
});

// Clear the ticket form an analysis results
clearButton.addEventListener('click', function () {
    // Clear description
    descriptionInput.value = '';

    // Reste the charcater counter
    characterCount.textContent = '0/2000';

    // Reset the analysis results
    categoryE.textContent = '';
    priorityE.textContent = '';
    summaryE.innerHTML = '<i class="fas fa-circle-info"></i> Your analysis will appear here.';
    explanationE.textContent = '';
    analysisSourceE.textContent = '';

    // Clear troubleshhoting steps.
    solutionsList.innerHTML = '';
    const paragraph2 = document.createElement('p');
    paragraph2.innerHTML = '<i class="fas fa-circle-info"></i> Your troubleshooting steps will appear here.';
    paragraph2.style.color = '#6c757d';
    solutionsList.appendChild(paragraph2);

    // Return focus to the description field
    formInput.focus();
})