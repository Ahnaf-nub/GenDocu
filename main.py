from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI and Groq client
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the Groq client
groq_client = Groq(api_key=os.getenv('API_KEY'))  # Replace with your actual API key

@app.get("/", response_class=HTMLResponse)
async def upload_page():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.post("/generate-docs")
async def generate_docs(
    files: list[UploadFile] = File(...),
    format: str = Form(...),
    context: str = Form(None)  # Make context optional
):
    code_documents = []
    for file in files:
        content = await file.read()
        code_documents.append(content.decode('utf-8'))

    # Combine code into a single string
    combined_code = "\n".join(code_documents)

    # Determine the style based on user selection
    if context:
        prompt = (
            f"The following code is provided:\n\n{combined_code}\n\n"
            f"Context provided by user: {context}\n\n"
        )
    else:
        prompt = (
            f"The following code is provided:\n\n{combined_code}\n\n"
        )

    if format == "github":
        style = "GitHub README.md"
        prompt += (
            f"Please generate well-structured, clear, and detailed documentation in {style} format. "
            f"Structure the documentation with the following sections: "
            f"1. **Overview** - Brief introduction and purpose of the code. "
            f"2. **Installation** - Steps to install any dependencies or set up the environment. "
            f"3. **Usage** - Instructions and examples on how to use the code. "
            f"4. **Code Explanation** - Detailed explanation of key functions, classes, and logic in the code. "
            f"5. **Conclusion** - Any additional notes or considerations. "
            f"Ensure that the documentation is formatted for readability with appropriate headings and code blocks where necessary."
        )
    else:
        style = "Normal Text"
        prompt += (
            f"Please generate well-structured, clear, and detailed documentation including setup instructions in {style} format. "
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
            model = "llama-3.1-70b-versatile",
        )
        documentation = response.choices[0].message.content
        
        if format == "general":
            documentation = documentation.replace("**", "").replace("##", "").replace("###", "").replace("***", "")
            
    except Exception as e:
        documentation = f"Error: {str(e)}"

    return JSONResponse(content={"documentation": documentation})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
