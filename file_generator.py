import os
import random

def generate_files(num_files, num_words, keywords, path="text_files"):
    os.makedirs(path, exist_ok=True)
    words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"]  # звичайні слова
    
    for i in range(num_files):
        file_path = os.path.join(path, f"file_{i+1}.txt")
        with open(file_path, 'w') as file:
            file_content = []
            for _ in range(num_words):
                if random.random() < 0.05:  # ймовірність вибору ключового слова
                    file_content.append(random.choice(keywords))
                else:
                    file_content.append(random.choice(words))
            file.write(' '.join(file_content))
        print(f"Generated {file_path}")

# Приклад використання
keywords = ["urgent", "confidential", "important"]  # ключові слова
generate_files(10, 100, keywords)
