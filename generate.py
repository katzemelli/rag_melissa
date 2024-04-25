#demonstration of how to import a collection of embeddings into a Chroma db collection
#with RAG retrieval augmented generation, the embeddings are used to retrieve relevant documents

import ollama, chromadb, time
from utilities import readtext, getconfig
from mattsollamatools import chunk_text_by_sentences

collectionname="ma-rag-embeddings"
#chroma run --host localhost --port 8000 --path ../vectordb-stores/chromadb
chroma = chromadb.HttpClient(host="localhost", port=8000)
print(chroma.list_collections())
if any(collection.name == collectionname for collection in chroma.list_collections()):
  print('deleting collection')
  chroma.delete_collection(collectionname)
collection = chroma.get_or_create_collection(name=collectionname, metadata={"hnsw:space": "cosine"})

embedmodel = getconfig()["embedmodel"]
starttime = time.time()
with open('sourcedocs-2.txt') as f:
  lines = f.readlines()
  for filename in lines:
    text = readtext(filename)
    if text == "":
      continue
    chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0 )
    print(f"with {len(chunks)} chunks")
    for index, chunk in enumerate(chunks):
      embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
      print(".", end="", flush=True)
      collection.add([filename+str(index)], [embed], documents=[chunk], metadatas={"source": filename})
    
print("--- %s seconds ---" % (time.time() - starttime))

