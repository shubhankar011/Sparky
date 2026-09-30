from sentence_transformers import SentenceTransformer
import json
import numpy as np
import commands
import sparky_SystemPrompt

# Load model
model = SentenceTransformer("./models/all-MiniLM-L6-v2")
# model.save("")
THRESHOLD = 0.2

# Load command descriptions
with open("commands_desc.json", "r", encoding="utf-8") as file:
    data = json.load(file)

comm = data["commands"]


# Create examples and labels
examples = []
labels = []

for comma, info in comm.items():
    for example in info["examples"]:
        examples.append(example)
        labels.append(comma)


# Convert all examples into embeddings
example_embeddings = model.encode(
    examples,
    normalize_embeddings=True
)


def classify(text):
    # Convert user input into an embedding
    input_embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    # Cosine similarity
    similarities = np.dot(
        example_embeddings,
        input_embedding
    )

    # Find best match
    best_index = np.argmax(similarities)

    command = labels[best_index]
    confidence = similarities[best_index]

    return command, confidence


if __name__ == "__main__":
    while True:
        text = input("\nSparky > ")

        if text.lower() == "exit" or text.lower() == "quit":
            break

        command, confidence = classify(text)

        print("Command:", command)
        print("Confidence:", round(float(confidence), 3))
        if confidence > THRESHOLD:
            print("True")
            commands.execute_command({
                "command": command,
                "parameters": {}
            })
        else:
            print("Unknown command")
