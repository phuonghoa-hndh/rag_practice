from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_cohere import CohereEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings()


def ask_chatbot(prompt):
    """
    Sends a prompt to the AI model and returns the response content.
    Args:
        prompt (str): The prompt to send to the model

    Returns:
        str: The response content from the model.
    """
    response = llm.invoke(prompt)
    return response.content


def rag_with_url(target_url, prompt):
    """
    Retrieves relevant documents from a target URL and generates an AI response based on the prompt.
    """
    loader = WebBaseLoader(target_url)
    raw_document = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=0, length_function=len
    )

    splited_document = text_splitter.split_documents(raw_document)

    vector_store = FAISS.from_documents(splited_document, embeddings)

    retriever = vector_store.as_retriever()

    relevant_documents = retriever.get_relevant_documents(prompt)

    final_prompt = (
        prompt + " " + " ".join([doc.page_content for doc in relevant_documents])
    )

    response = llm.invoke(final_prompt)

    return response.content
