const form = document.getElementById('upload-form');
const output = document.getElementById('output');
const copyButton = document.getElementById('copy-button');

form.addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(form);
    output.innerHTML = 'Cooking...';

    const response = await fetch('/generate-docs', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    output.innerHTML = '<h3>Generated Documentation:</h3>' + result.documentation;
});

copyButton.addEventListener('click', function () {
    const textToCopy = output.innerText;
    navigator.clipboard.writeText(textToCopy).then(() => {
        alert('Documentation copied to clipboard!');
    }).catch(err => {
        alert('Failed to copy text: ', err);
    });
});