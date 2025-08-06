from transformers import AutoTokenizer, AutoModel
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import torch

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")

sentence = "King and queen are royalty."
inputs = tokenizer(sentence, return_tensors="pt")
outputs = model(**inputs)

embeddings = outputs.last_hidden_state.squeeze(0).detach().numpy()
labels = tokenizer.convert_ids_to_tokens(inputs["input_ids"].squeeze(0))

pca = PCA(n_components=2)
reduced = pca.fit_transform(embeddings)

plt.figure(figsize=(10, 6))
plt.scatter(reduced[:, 0], reduced[:, 1])

for i, label in enumerate(labels):
    plt.annotate(label, (reduced[i, 0], reduced[i, 1]))

plt.title("2D Token Embeddings via PCA")
plt.grid(True)
# plt.show()
plt.savefig("embedding_plot.png")
print("Plot saved as embedding_plot.png")
