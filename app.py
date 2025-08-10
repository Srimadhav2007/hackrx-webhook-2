from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from llm_code import query_vertex_ai_rag_engine
import json

PROMPT = """For the given question below, refer to the document url and answer the question in one or two medium to long sentences max. 
                The returned answers must be in json format string, with no other text with it before or after it, with key being "answers", and value being JSON array of answers\n"""

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/hackrx/run")
async def doc_load(request: Request):
    payload = await request.json()
    questions = json.dumps(payload,indent=4)
    url = payload.get('documents')
    queries = payload.get('questions')

    if not url or not queries:
        return JSONResponse(content={"error": "Missing 'documents' or 'questions' in payload"}, status_code=400)

    try:
        returned = query_vertex_ai_rag_engine(user_query=(PROMPT+"\n"+questions))
        print('\n\n\n')
        print(returned)
        return JSONResponse(content=json.loads(returned[returned.find('\n')+1:returned.rfind('\n')]))
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
