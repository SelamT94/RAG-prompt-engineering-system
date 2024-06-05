import os
import time
from datasets import load_dataset
from pinecone import Pinecone, ServerlessSpec
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone as LangChainPinecone
from tqdm.auto import tqdm
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Load the dataset
def load_data():
    dataset = load_dataset("jamescalam/llama-2-arxiv-papers-chunked", split="train")
    return dataset

# Initialize Pinecone
def init_pinecone(api_key):
    pc = Pinecone(api_key=api_key)
    spec = ServerlessSpec(cloud="aws", region="us-east-1")
    return pc, spec

# Create Pinecone index
def create_index(pc, spec, index_name="llama-2-rag"):
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    if index_name not in existing_indexes:
        pc.create_index(index_name, dimension=1536, metric='dotproduct', spec=spec)
        while not pc.describe_index(index_name).status['ready']:
            time.sleep(1)
    index = pc.Index(index_name)
    return index

# Embed and index data
def embed_and_index_data(embed_model, index, data):
    batch_size = 100
    for i in tqdm(range(0, len(data), batch_size)):
        i_end = min(len(data), i + batch_size)
        batch = data.iloc[i:i_end]
        ids = [f"{x['doi']}-{x['chunk-id']}" for i, x in batch.iterrows()]
        texts = [x['chunk'] for _, x in batch.iterrows()]
        embeds = embed_model.embed_documents(texts)
        metadata = [{'text': x['chunk'], 'source': x['source'], 'title': x['title']} for i, x in batch.iterrows()]
        index.upsert(vectors=zip(ids, embeds, metadata))

# Main workflow
def main():
    # Load dataset
    dataset = load_data()
    data = dataset.to_pandas()
    
    # Initialize Pinecone
    api_key = os.getenv("PINECONE_API_KEY") or "YOUR_API_KEY"
    pc, spec = init_pinecone(api_key)
    
    # Create index
    index = create_index(pc, spec)
    
    # Initialize embedding model
    embed_model = OpenAIEmbeddings(model="text-embedding-ada-002")
    
    # Embed and index data
    embed_and_index_data(embed_model, index, data)
    
    # Initialize vectorstore
    text_field = "text"
    vectorstore = LangChainPinecone(index, embed_model.embed_query, text_field)
    
    # Chat model setup
    chat = ChatOpenAI(model="gpt-3.5-turbo")
    
    # Query and augment prompt
    query = "What is so special about Llama 2?"
    def augment_prompt(query):
        results = vectorstore.similarity_search(query, k=3)
        source_knowledge = "\n".join([x.page_content for x in results])
        augmented_prompt = f"""Using the contexts below, answer the query.
        
        Contexts:
        {source_knowledge}
        
        Query: {query}"""
        return augmented_prompt

    # Generate response
    prompt = HumanMessage(content=augment_prompt(query))
    messages = [prompt]
    res = chat(messages)
    print(res.content)

    # Clean up
    pc.delete_index(index.name)

if __name__ == "__main__":
    main()
