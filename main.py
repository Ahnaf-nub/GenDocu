from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from groq import Groq

# Initialize FastAPI and Groq client
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the Groq client
groq_client = Groq(api_key="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")  # Replace with your actual API key

@app.get("/", response_class=HTMLResponse)
async def upload_page():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/generate-docs")
async def generate_docs(files: list[UploadFile] = File(...)):
    code_documents = []
    for file in files:
        content = await file.read()
        code_documents.append(content.decode('utf-8'))

    # Combine code into a single string
    combined_code = "\n".join(code_documents)

    # Create the prompt for Groq's LLaMA model
    prompt = f"Please generate github documentation with details for the following code:\n\n{combined_code}\n\nDocumentation:"

    # Call Groq's API to generate documentation
    try:
        response = groq_client.completions.create(
            model="llama-3.1-70b-versatile",
            prompt=prompt,
            max_tokens=2048
        )
        documentation = response.choices[0].text.strip()
    except Exception as e:
        documentation = f"Error: {str(e)}"

    return JSONResponse(content={"documentation": documentation})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

