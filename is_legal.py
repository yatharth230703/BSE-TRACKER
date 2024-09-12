from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
    load_index_from_storage
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.groq import Groq

import warnings
warnings.filterwarnings('ignore')
def legality(file_path):
    GROQ_API_KEY = "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"
    
    Settings.llm = Groq(model="llama3-8b-8192", api_key=GROQ_API_KEY)
    Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    Settings.node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=200)

    reader = SimpleDirectoryReader(input_files=[file_path])
    documents = reader.load_data()
    nodes = Settings.node_parser.get_nodes_from_documents(documents, show_progress=True)

    vector_index = VectorStoreIndex.from_documents(documents, node_parser=nodes)
    vector_index.storage_context.persist(persist_dir="storage_mini")
    storage_context = StorageContext.from_defaults(persist_dir="storage_mini")
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    q6 = """ 
    Determine whether the given document contains the words "violation(s)" or "contravention(s)" in any of the tables. Return "YES" if either of these terms is found in any table, and return "NO" if neither term is found. 
    
    If Found: Return "YES."
    If Not Found: Return "NO."
    Remember, only return "YES" or "NO," and nothing else.
    """
    resp6 = query_engine.query(q6)
    return resp6