import toml
from tqdm import tqdm

from nonagon.extractor import Extractor


def calculate_precision_recall(TP, FP, FN):
    precision = TP / (TP + FP) if TP + FP > 0 else 0
    recall = TP / (TP + FN) if TP + FN > 0 else 0
    return precision, recall


if __name__ == "__main__":
    config = toml.load("config.toml")
    classifier = Extractor(**config["OpenAI"])

    test_cases = open("test/synthetic_dataset.txt", "r")
        .read().split("---TEST CASE---\n")
    test_cases += open("test/github_dataset.txt", "r").read().split("---TEST CASE---\n")

    TP = 0
    FP = 0
    FN = 0

    for test_case in tqdm(test_cases):
        conversation, categories = test_case.split("===\n")
        actual_categories = {c for c in categories.strip().split(",") if c != "none"}
        predicted_categories = set(
            c for c, r in classifier.extract(conversation, []).items() if r is not None
        )

        classification = classifier.extract(conversation, [])
        classification = {c for c in classification if not classification[c] is None}

        TP += len(predicted_categories & actual_categories)
        FP += len(predicted_categories - actual_categories)
        FN += len(actual_categories - predicted_categories)

        if predicted_categories != actual_categories:
            tqdm.write(
                f"Found incorrect prediction: expected {actual_categories}, predicted {predicted_categories} for conversation:\n{conversation}"
            )

    precision, recall = calculate_precision_recall(TP, FP, FN)
    print(f"Precision: {precision}, Recall: {recall}")
