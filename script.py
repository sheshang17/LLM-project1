from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import sys

DB_FAISS_PATH = "vectorstore/db_faiss"
loader = CSVLoader(file_path="C:/Users/shesh/cis_project/CIS_Amazon_Web_Services_Foundations_Benchmark_v1.3.0.csv", encoding="utf-8", csv_args={'delimiter': ','})
data = loader.load()
print(data)


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
text_chunks = text_splitter.split_documents(data)

print(len(text_chunks))


embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')


docsearch = FAISS.from_documents(text_chunks, embeddings)

docsearch.save_local(DB_FAISS_PATH)


#query = " you can ask question here and answer will be find by the similarity surch"

#docs = docsearch.similarity_search(query, k=3)

#print("Result", docs)

llm = CTransformers(model="llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type="llama",
                    max_new_tokens=512,
                    temperature=0.4)

qa = ConversationalRetrievalChain.from_llm(llm, retriever=docsearch.as_retriever())

while True:
    chat_history = []
    #query = "you can ask question here "
    query = input(f"Input Prompt: ")
    if query == 'exit':
        print('Exiting')
        sys.exit()
    if query == '':
        continue
    result = qa({"question":query, "chat_history":chat_history})
    print("Response: ", result['answer'])