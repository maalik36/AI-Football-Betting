from google import genai
from os import environ
import phoenix as px
from dotenv import load_dotenv
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from phoenix.otel import register

load_dotenv()

OPENAI_API_KEY = environ["OPENAI_API_KEY"]
# Only run this block for Gemini Developer API
client = genai.Client(api_key='GEMINI_API_KEY')
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI


# Create an llm object to use for the QueryEngine and the ReActAgent
llm = OpenAI(model="gpt-4")
session = px.launch_app()
tracer_provider = register()
LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
try:
    storage_context = StorageContext.from_defaults(
        persist_dir="./storage/past"
    )
    past_index = load_index_from_storage(storage_context)

    index_loaded = True
except:
    index_loaded = False
if not index_loaded:
    # load data
    past_stats = SimpleDirectoryReader(
        input_files=["SeasonsData.csv"]
    ).load_data()
    
    # build index
    past_index = VectorStoreIndex.from_documents(past_index, show_progress=True)
    
    # persist index
    past_index.storage_context.persist(persist_dir="./storage/past")
    
past_engine = past_index.as_query_engine(similarity_top_k=3, llm=llm)
query_engine_tools = [
    QueryEngineTool(
        query_engine=past_engine,
        metadata=ToolMetadata(
            name="past game data",
            description=(
                "Provides information about past game data from football. "
                
            ),
        ),
    ),
    ]
agent = ReActAgent.from_tools(
    query_engine_tools,
    llm=llm,
    verbose=True,
    max_turns=10,
)