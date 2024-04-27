# rag

how to use rag with ollama
**Requirements:**

* Python -> see requirements.txt
* current version of ollama ( https://ollama.com )
* chromadb ( https://www.trychroma.com )
* nltk toolkit installed (see import-nltk.py)

and please install Python in a virual inviroment.

**Usage:**

check out frist config.ini. In this file we define the main model and also the embedding model used to create the embeddings.
For instance:
mainmodel=llama3
embedmodel=nomic-embed-text (setting "internal" uses chromadb's embedder.)

use generate.py to produce the embeddings according to sourcedocs-2.txt
cli: python generate.py

use aks.py to retrieve information.
cli: python ask.py "Why is the sky blue?"
