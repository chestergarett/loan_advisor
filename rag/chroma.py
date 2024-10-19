import chromadb

def init_client():
    chroma_client = chromadb.Client()
    return chroma_client

def init_collection(chroma_client,collection_name):
    collection = chroma_client.get_or_create_collection(name=collection_name)
    return collection

def upsert_documents(collection):
    # switch `add` to `upsert` to avoid adding the same documents every time
    collection.upsert(
        documents=[
            "This is a document about pineapple",
            "This is a document about oranges"
        ],
        ids=["id1", "id2"]
    )

    print('Successfully added collection')

def query_collection(collection,query):
    results = collection.query(
        query_texts=[query], 
        n_results=2 # how many results to return
    )

    return results

if __name__=='__main__':
    chroma_client = init_client()
    collection = init_collection(chroma_client,'my_collection')
    results = query_collection(collection,"This is a query document about hawaii")
    print(results)