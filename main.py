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
    prompt = (
        f"The following code is provided:\n\n{combined_code}\n\n"
        f"Please generate well-structured, clear, and detailed documentation in Markdown format. "
        f"The documentation should include an overview, explanations of key components, "
        f"usage examples, and any other relevant information that would help a general audience "
        f"understand and use the code. Ensure the documentation is formatted for readability."
    )

    # Call Groq's API to generate documentation
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt
                }
            ],
            model="llama-3.1-70b-versatile",    
        )
        documentation = response.choices[0].message.content
    except Exception as e:
        documentation = f"Error: {str(e)}"

    return JSONResponse(content={"documentation": documentation})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
