from transformers import BertTokenizer, BertModel
import matplotlib.pyplot as plt
import seaborn as sns
import torch

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased", output_attentions=True)

sentence = "The dog chased the cat."
inputs = tokenizer(sentence, return_tensors="pt")
outputs = model(**inputs)

# First layer, first head attention
attention = outputs.attentions[0][0, 0].detach().numpy()
labels = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

plt.figure(figsize=(10, 8))
sns.heatmap(attention, xticklabels=labels, yticklabels=labels, cmap="viridis", annot=True)
plt.title("Self-Attention Heatmap (Layer 1, Head 1)")
plt.xlabel("Attending To")
plt.ylabel("From Token")
plt.tight_layout()
#plt.show()

plt.savefig("heatmap.png")
print("Plot saved as heatmap.png")
