from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    ServiceContext,
    Settings,
    load_index_from_storage
)
import os
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.groq import Groq

import warnings
warnings.filterwarnings('ignore')

def retriever(file_path):
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

    q3 = """ 
    Return to me the company or companies from which the order was received from the given document and nothing else. For your information, following is some advice and instructions:
    Definition: The Order received from refers to the entity or organization that is issuing or awarding the order. This is the company or party that is making the request for goods, services, or other deliverables.
    Key Points to Identify:
    Identify phrases like "Order placed by," "Received from," "Ordered by," "Issued by," or "Client."
    This should clearly be the name of a company or organization (or sometimes an individual if specifically noted) that is distinct from the Receiver Company.
    Ensure this is the entity responsible for the initiation of the transaction or agreement.
    If multiple entities are found, return a list of all identified entities.
    If Not Found: Simply return "Not found."
    Remember, only return the company or companies from which the order was received, and nothing else.
    """
    resp3 = query_engine.query(q3)

    q4 = """ 
    Return to me the order value or values from the given document and nothing else. For your information, following is some advice and instructions:
    Definition: The Order Value is the total monetary amount that has been agreed upon for the completion of the order. This should be explicitly stated in the document, often in currency terms.
    Key Points to Identify:
    Look for terms such as "Total Amount," "Order Value," "Cost," or "Price."
    Ensure that the value is complete and accurate, with no ambiguity (e.g., "100,000").
    If multiple values are found, return a list of all identified values.
    If Not Found: Simply return "Not found."
    Remember, only return the order value or values, and nothing else.
    """
    resp4 = query_engine.query(q4)

    q5 = """ 
    Return to me the execution period or periods from the given document and nothing else. For your information, following is some advice and instructions:
    Definition: The Execution Period refers to the duration or timeframe within which the order must be fulfilled or completed. This is often stated as a specific number of days, weeks, or months.
    Key Points to Identify:
    Look for terms like "Delivery period," "Execution time," "Completion period," or "Timeframe."
    Ensure that the period is precisely defined (e.g., "30 days from the order date").
    If multiple periods are found, return a list of all identified periods.
    If no timeframe is mentioned, explicitly state "Not found."
    Remember, only return the execution period or periods, and nothing else.
    """
    resp5 = query_engine.query(q5)

    return resp3 , resp4 ,resp5



    
