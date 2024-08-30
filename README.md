# Code Documentation Generator
### Overview
If you are lazy like me in terms of generating documentation then this tool is for you! This project is a web-based application that generates detailed documentation from uploaded code files. The application is built using FastAPI for the backend, Groq's LLaMA model for generating the documentation, and a simple frontend with HTML, CSS, and JavaScript. 
*(This documentation is also written using this tool!!!)*
## Features

- **Upload Multiple Files**: Users can upload multiple code files simultaneously to generate comprehensive documentation.
- **Documentation Format Options**: Choose between GitHub README format or a general format for the generated documentation.
- **Copy to Clipboard**: Users can easily copy the generated documentation to their clipboard with a single click.

  **Setup Instructions**
   ----------------------### Prerequisites
    * Python 3.8+ * FastAPI * Groq API key
     ### Installation 
     1. Clone the repository: `git clone https://github.com/Ahnaf-nub/Code-Documentation-Generator.git`
     2. Install the required dependencies: `pip install fastapi groq` 
     3. Replace the `api_key` variable in the `groq_client` initialization with your actual Groq API key. 
     ### Running the Application 
     1. Run the application: `uvicorn main:app --host 127.0.0.1 --port 8000`
     2. Open a web browser and navigate to `http://127.0.0.1:8000/`
    **Usage** --------- 
    ### Uploading Code
    1. Navigate to the application's homepage: `http://127.0.0.1:8000/`
    2. Click the "Choose Files" button to select one or more code files to upload.
    3. Select the desired documentation format: GitHub README.md or Normal Text.
    4. Click the "Generate Documentation" button.
    ### Viewing Documentation 
    1. The generated documentation will be displayed ine the box.
    2. The documentation includes an overview, explanations of key components, usage examples, and other relevant information.
    **Key Components**
     ------------------ * `main.py`: The main application file that defines the FastAPI routes and handles user input. *
      `groq_client`: The Groq API client that generates the documentation.
       * `templates/index.html`: The HTML template for the application's homepage.
       *  **Troubleshooting** ------------------ * 
       Ensure that the Groq API key is valid and properly configured.
       * Check the application logs for any error messages. * Verify that the code files are uploaded correctly and in the correct format.
