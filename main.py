from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain import PromptTemplate, LLMChain
from langchain.chains import SimpleSequentialChain
from groq import Groq

# Initialize FastAPI and Groq LLM
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

groq_llm = Groq(api_key="")  # Replace with your API key

# Define a simple prompt template
prompt_template = PromptTemplate(
    input_variables=["code_snippet"],
    template="Please generate documentation for the following code:\n\n{code_snippet}\n\nDocumentation:"
)

# Set up the LangChain pipeline
llm_chain = LLMChain(prompt=prompt_template, llm=groq_llm)
chain = SimpleSequentialChain(chains=[llm_chain])

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

    # Generate documentation using the LangChain pipeline
    try:
        documentation = chain.run(combined_code)
    except Exception as e:
        documentation = f"Error: {str(e)}"

    return JSONResponse(content={"documentation": documentation})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

