import os

knowledge = []


def load_knowledge():

    global knowledge

    knowledge = []

    folder = "knowledge"

    if not os.path.exists(folder):
        return

    for filename in os.listdir(folder):

        if filename.endswith(".txt"):

            path = os.path.join(folder, filename)

            with open(path, "r", encoding="utf-8") as f:

                knowledge.append(
                    {
                        "source": filename,
                        "content": f.read()
                    }
                )

    print(f"Loaded {len(knowledge)} knowledge files.")


def search_knowledge(query):

    print("\nSearching for:", query)

    query = query.lower()

    stop_words = {
        "what",
        "is",
        "the",
        "a",
        "an",
        "how",
        "can",
        "do",
        "does",
        "tell",
        "me",
        "about",
        "explain",
        "should",
        "i",
        "to",
        "of",
        "on",
        "for",
        "and",
        "in",
        "my",
        "it"
    }

    keywords = [
        word
        for word in query.split()
        if word not in stop_words and len(word) > 2
    ]

    print("Keywords:", keywords)

    best_match = None
    best_score = 0

    for doc in knowledge:
        
        print("Checking:", doc["source"])

        text = doc["content"].lower()
        
        print(text[:150])

        score = 0

        for word in keywords:

            score += text.count(word)

        print(doc["source"], "Score:", score)

        if score > best_score:

            best_score = score
            best_match = doc

    if best_match:

        print("Selected:", best_match["source"])

        return best_match

    print("No relevant knowledge found.")

    return None