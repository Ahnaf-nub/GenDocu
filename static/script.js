const form = document.getElementById('upload-form');
const output = document.getElementById('output');

form.addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(form);
    output.innerHTML = 'Uploading...';

    const response = await fetch('/generate-docs', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    output.innerHTML = '<h3>Generated Documentation:</h3>' + result.documentation;
});