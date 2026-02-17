from text import text
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken

# Inicializar tokenizer
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

# Configuración equivalente a llm-chunk de Node.js
splitter = RecursiveCharacterTextSplitter(
    chunk_size=120,         # maxLength
    chunk_overlap=40,       # overlap
    length_function=lambda text: len(tokenizer.encode(text)),  # contar tokens
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    tokens = len(tokenizer.encode(chunk))
    print(f"CHUNK {i+1} ({tokens} tokens): {chunk}\n")

