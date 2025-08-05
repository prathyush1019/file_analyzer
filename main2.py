import os
import shutil
import logging
from tabulate import tabulate

logging.basicConfig(
    filename='file_mover.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)


def filepath():
    file_path = input("Enter the file name: ").strip()
    if file_path.startswith('"') and file_path.endswith('"'):
        file_path = file_path[1:-1]
    elif file_path.startswith('"'):
        file_path = file_path[1:]
    elif file_path.endswith('"'):
        file_path = file_path[:-1]
    return file_path


def check_file(filepath):
    destination_file = r"C:\Users\padma\OneDrive\Desktop\word_count"
    if not os.path.exists(filepath):
        logging.error("Invalid file path.")
        return

    source = os.path.basename(filepath)
    destination = os.path.join(destination_file, source)
    if not os.path.exists(destination):
        try:
            shutil.copy(filepath, destination)
            logging.info("File moved to destination folder")
            return destination
        except Exception as e:
            print("File not found")
            logging.error("File not found")
    else:
        logging.info("File already in the folder")
        return destination


def read_file():
    num_words = 0
    num_lines = 0
    num_spaces = 0
    num_special = 0
    num_digits = 0
    num_upper = 0
    num_lower = 0
    file = filepath()

    output_lines = [] 

    with open(check_file(file), 'r') as f:
        for line in f:
            num_lines += 1
            num_words += len(line.split())
            num_spaces += line.count(' ')
            num_special += len([char for char in line if not char.isalnum() and not char.isspace()])
            num_digits += len([char for char in line if char.isdigit()])
            num_upper += len([char for char in line if char.isupper()])
            num_lower += len([char for char in line if char.islower()])

    summary_table = [
        ["Number of lines", num_lines],
        ["Number of words", num_words],
        ["Number of spaces", num_spaces],
        ["Number of special characters", num_special],
        ["Number of digits", num_digits],
        ["Number of uppercase letters", num_upper],
        ["Number of lowercase letters", num_lower]
    ]

    summary_output = tabulate(summary_table, headers=["Metric", "Count"], tablefmt="grid")
    print(summary_output)
    output_lines.append(summary_output)

    logging.info("Number of lines: %s", num_lines)
    logging.info("Number of words: %s", num_words)
    logging.info("Number of spaces: %s", num_spaces)
    logging.info("Number of special characters: %s", num_special)
    logging.info("Number of digits: %s", num_digits)
    logging.info("Number of uppercase letters: %s", num_upper)
    logging.info("Number of lowercase letters: %s", num_lower)

    with open(check_file(file), 'r') as f:
        text = f.read()
        word_counts = {}

        for word in text.split():
            word_counts[word] = word_counts.get(word, 0) + 1

        not_req = {"to", "To", "the", "The", "and", "And", "or", "Or", "etc", "ETC"}
        unique_words = [word for word, count in word_counts.items() if count == 1 and word not in not_req]

        logging.info("Unique values: %s", unique_words)

        
        word_freq_table = tabulate(word_counts.items(), headers=["Word", "Count"], tablefmt="grid")
        print("\nWord Frequencies:")
        print(word_freq_table)
        output_lines.append("\nWord Frequencies:\n" + word_freq_table)

        
        unique_word_table = tabulate([[word] for word in unique_words], headers=["Unique Word"], tablefmt="grid")
        print("\nUnique Words:")
        print(unique_word_table)
        output_lines.append("\nUnique Words:\n" + unique_word_table)

        
        total_unique_output = tabulate([["Total Unique Words", len(unique_words)]], headers=["Metric", "Count"], tablefmt="grid")
        print(total_unique_output)
        output_lines.append("\n" + total_unique_output)

        
        word_lengths_table = tabulate([[word, len(word)] for word in unique_words], headers=["Word", "Length"], tablefmt="grid")
        print("\nLength of Each Unique Word:")
        print(word_lengths_table)
        output_lines.append("\nLength of Each Unique Word:\n" + word_lengths_table)

        
        if word_counts:
            max_len = max(len(word) for word in word_counts)
            min_len = min(len(word) for word in word_counts)
        else:
            max_len = min_len = 0

        length_extremes_table = tabulate([
            ["Length of Largest Word", max_len],
            ["Length of Smallest Word", min_len]
        ], headers=["Metric", "Length"], tablefmt="grid")
        print(length_extremes_table)
        output_lines.append("\n" + length_extremes_table)

        logging.info("Number of unique values: %s", len(unique_words))

    with open("output_report.txt", "w", encoding="utf-8") as output_file:
        output_file.write("\n".join(output_lines))

    print("\nAll output saved to 'output_report.txt'")


if __name__ == "__main__":
    read_file()
