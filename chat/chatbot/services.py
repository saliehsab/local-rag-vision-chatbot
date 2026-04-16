import os
import ollama
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

CHROMA_DIR = "./chroma_db"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
LLM_MODEL = "qwen2.5:7b"
#EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# LLM_MODEL = "qwen"

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
llm = Ollama(model=LLM_MODEL, temperature=0.1)

def process_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=250, separators=["\n\n", "\n", ".", " "])
    documents = loader.load()

    chunks = splitter.split_documents(documents)
    
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=CHROMA_DIR)
    return vectorstore


def analyze_image_with_vlm(image_path):
    try:
        response = ollama.generate(
            model='qwen2.5vl:3b', 
            prompt="Transcribe all the text you see in this image. Write only the text found.",
            images=[image_path]
        )
        transcription = response['response'].strip()
        
        if not transcription or "blurry" in transcription.lower():
             return "Erreur : L'image n'a pas pu être lue correctement."

        # print(f"--- OCR MOONDREAM ---\n{transcription}\n-------------------")
        return transcription
    except Exception as e:
        print(f"Erreur : {e}")
        return ""


def process_image_as_document(image_path):
    transcription = analyze_image_with_vlm(image_path)
    from langchain_core.documents import Document
    doc = Document(
        page_content=transcription,
        metadata={"source": os.path.basename(image_path), "type": "image_doc"}
    )
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents([doc])
    
    vectorstore = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory=CHROMA_DIR
    )
    print(transcription)
    return vectorstore


def ask_question(question, short_history=""):
    vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

    system_prompt = (
    "Tu es un assistant de support STRICT. Ton unique source de vérité est le CONTEXTE fourni ci-dessous. "
    "1. Si le contexte contient des informations sur une intégration en entreprise, utilise EXCLUSIVEMENT ces mots. "
    "2. Ne donne JAMAIS de conseils généraux en économie ou management si ce n'est pas écrit dans le texte. "
    "3. Si le contexte est vide ou hors-sujet, dis simplement : 'Désolé, l'image/le document indexé ne contient pas cette information.'\n\n"
    "CONTEXTE :\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    doc_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, doc_chain)

    result = rag_chain.invoke({
        "input": question,
        "chat_history": short_history if short_history else "Aucun historique disponible."
    })
    return result.get("answer")