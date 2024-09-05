const form = document.getElementById('upload-form');
const output = document.getElementById('output');
const copyButton = document.getElementById('copy-button');
const viewReadmeButton = document.getElementById('view-readme-button');

let documentationText = "";  // Store the generated documentation for multiple uses
let isMarkdownRendered = false; // Track the state of the output

form.addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(form);
    output.innerHTML = 'Cooking...';

    const response = await fetch('/generate-docs', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    documentationText = result.documentation; // Save the documentation for later use

    // Display the documentation in <pre> format for multiline display
    output.innerHTML = '<h3>Generated Documentation:</h3><pre>' + documentationText + '</pre>';
    isMarkdownRendered = false; // Reset the state of the output
});

copyButton.addEventListener('click', function () {
    const textToCopy = output.innerText;
    navigator.clipboard.writeText(textToCopy).then(() => {
        alert('Documentation copied to clipboard!');
    }).catch(err => {
        alert('Failed to copy text: ', err);
    });
});

viewReadmeButton.addEventListener('click', function () {
    if (isMarkdownRendered) {
        // Display the raw text output
        output.innerHTML = '<h3>Generated Documentation:</h3><pre>' + documentationText + '</pre>';
        isMarkdownRendered = false; // Update the state of the output
    } else {
        // Render the Markdown content using the marked.js library
        output.innerHTML = '<h3>GitHub README.md Preview:</h3>' + marked.parse(documentationText);
        isMarkdownRendered = true; // Update the state of the output
    }
});
