import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline


# Load documents
def load_documents():
    docs = []
    for file in os.listdir("data"):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join("data", file))
            docs.extend(loader.load())
    return docs


# Vector DB
def create_vector_db(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    return FAISS.from_documents(chunks, embeddings)


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langchain_community.llms import HuggingFacePipeline
import torch


def create_llm():
    model_name = "google/flan-t5-base"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def generate_text(prompt):
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True)

        outputs = model.generate(
            **inputs,
            max_new_tokens=120,
            temperature=0
        )

        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    class CustomLLM:
        def __call__(self, prompt, **kwargs):
            return generate_text(prompt)

    return CustomLLM()


# Added to prevent NameError since it was referenced but not defined in your snippet
def is_broad_query(query):
    return len(query.split()) > 10


def create_qa_chain(db):
    llm = create_llm()
    retriever = db.as_retriever(search_kwargs={"k": 5})

    def qa_function(query):

        # 🔴 CASE 1: Broad question → use MORE context
        if is_broad_query(query):
            docs = retriever.get_relevant_documents(query)

            if not docs:
                return "I am sorry, that information is not in my database."

            # 🔥 combine ALL chunks
            context = "\n".join([doc.page_content for doc in docs])

            prompt = f"""
            You are a university assistant.

            Provide a detailed explanation using ONLY the context.

            Structure your answer clearly.

            Context:
            {context}

            Question:
            {query}

            Detailed Answer:
            """

            return llm(prompt)

        # 🔴 CASE 2: Normal QA
        docs = retriever.get_relevant_documents(query)

        if not docs:
            return "I am sorry, that information is not in my database."

        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
        Answer ONLY using the context below.

        Context:
        {context}

        Question:
        {query}

        Answer:
        """

        return llm(prompt)

    return qa_function






def initialize_chatbot():
    docs = load_documents()
    db = create_vector_db(docs)
    return create_qa_chain(db)


if __name__ == "__main__":
    initialize_chatbot()