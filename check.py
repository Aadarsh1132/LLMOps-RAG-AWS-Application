import numpy as np
import faiss
import os

dim = 128
xb = np.random.random((100, dim)).astype('float32')
index = faiss.IndexFlatL2(dim)
index.add(xb)

os.makedirs("faiss_index", exist_ok=True)
faiss.write_index(index, "faiss_index/index.faiss")
