# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import PyPDFLoader
# import os
# from pathlib import Path

# class RAG:
#     def __init__(self):
#         self.embeddings = OpenAIEmbeddings()
#         self.vector_store = None
#         self.text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000,
#             chunk_overlap=200,
#         )

#     def load_knowledge_base(self, pdf_path: str):
#         loader = PyPDFLoader(pdf_path)
#         documents = loader.load()
#         texts = self.text_splitter.split_documents(documents)
#         self.vector_store = FAISS.from_documents(texts, self.embeddings)

#     def search_context(self, query: str, k: int = 3):
#         if self.vector_store is None:
#             raise ValueError("Knowledge base not loaded. Call load_knowledge_base first.")
#         docs = self.vector_store.similarity_search(query, k=k)
#         return "\n".join([doc.page_content for doc in docs])





# from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chains import RetrievalQA
# from langchain.llms import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class RAGSystem:
#     def __init__(self):
#         # Load knowledge base
#         self.load_knowledge_base()
#         self.initialize_qa_system()
    
#     def load_knowledge_base(self):
#         # Load PDF document
#         loader = PyPDFLoader("knowledge_base/customer_service.pdf")
#         documents = loader.load()
        
#         # Split documents into chunks
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000,
#             chunk_overlap=200
#         )
#         self.documents = text_splitter.split_documents(documents)
        
#         # Create embeddings and vector store
#         embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
#         self.vectorstore = FAISS.from_documents(self.documents, embeddings)
    
#     def initialize_qa_system(self):
#         self.qa = RetrievalQA.from_chain_type(
#             llm=OpenAI(temperature=0),
#             chain_type="stuff",
#             retriever=self.vectorstore.as_retriever(),
#             return_source_documents=True
#         )
    
#     def query(self, question):
#         result = self.qa({"query": question})
#         return result["result"]
############################## from open ai 




# from langchain_community.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_community.llms import GPT4All
# from langchain_community.chains import RetrievalQA
# import os
# from pathlib import Path

# class RAGSystem:
#     def __init__(self):
#         # Model paths
#         self.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
#         self.llm_path = str(Path.home() / ".cache" / "gpt4all" / "ggml-gpt4all-j-v1.3-groovy.bin")
        
#         # Initialize models
#         self.load_knowledge_base()
#         self.initialize_qa_system()
    
#     def load_knowledge_base(self):
#         try:
#             # Read text file
#             with open("knowledge_base/customer_service.txt", "r") as f:
#                 text = f.read()
            
#             # Split text into chunks
#             text_splitter = RecursiveCharacterTextSplitter(
#                 chunk_size=1000,
#                 chunk_overlap=200
#             )
#             self.documents = text_splitter.create_documents([text])
            
#             # Create embeddings with free model
#             embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
#             self.vectorstore = FAISS.from_documents(self.documents, embeddings)
#         except Exception as e:
#             print(f"Error loading knowledge base: {str(e)}")
#             raise
    
#     def initialize_qa_system(self):
#         # Initialize free LLM
#         llm = GPT4All(
#             model=self.llm_path,
#             max_tokens=1000,
#             temp=0.7
#         )
        
#         self.qa = RetrievalQA.from_chain_type(
#             llm=llm,
#             chain_type="stuff",
#             retriever=self.vectorstore.as_retriever(),
#             return_source_documents=True
#         )
    
#     def query(self, question):
#         result = self.qa({"query": question})
#         return result["result"]





# app/rag.py

from langchain_community.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import GPT4All
from langchain_community.chains import RetrievalQA
from pathlib import Path
import os


class RAGSystem:
    def __init__(self):
        # Model paths
        self.embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
        self.llm_path = str(Path.home() / ".cache" / "gpt4all" / "ggml-gpt4all-j-v1.3-groovy.bin")

        # Load components
        self.load_knowledge_base()
        self.initialize_qa_system()

    def load_knowledge_base(self):
        try:
            # Read text file
            kb_path = "knowledge_base.txt"
            if not os.path.exists(kb_path):
                raise FileNotFoundError(f"Knowledge base not found at {kb_path}")
            
            with open(kb_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            self.documents = text_splitter.create_documents([text])

            # Embeddings
            embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model)
            self.vectorstore = FAISS.from_documents(self.documents, embeddings)

        except Exception as e:
            print(f"Error loading knowledge base: {str(e)}")
            raise

    def initialize_qa_system(self):
        try:
            llm = GPT4All(
                model=self.llm_path,
                max_tokens=1000,
                temperature=0.7
            )

            self.qa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(),
                return_source_documents=True
            )
        except Exception as e:
            print(f"Error initializing QA system: {str(e)}")
            raise

    def query(self, question: str) -> str:
        result = self.qa({"query": question})
        return result["result"]
