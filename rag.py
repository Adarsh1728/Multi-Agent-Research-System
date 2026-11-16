
from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS

from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_vectorstore(documents, api_key):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        api_key=api_key
    )

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    return vectorstore


def retrieve_documents(
    vectorstore,
    query,
    k=5
):

    if vectorstore is None:
        return []

    results = vectorstore.similarity_search(
        query,
        k=k
    )

    return results
