import math
from collections import defaultdict

print("--- Standalone ML Phishing Detection Model ---")

# 1. Training Dataset (1 = Phishing, 0 = Safe)
train_corpus = [
    ("Urgent: Your account is locked. Click here to verify your password immediately.", 1),
    ("Congratulations! You won a $1000 Amazon gift card. Claim your prize now.", 1),
    ("Dear user, suspicious login activity detected on your bank profile. Secure it here.", 1),
    ("Hey, are we still meeting for lunch at 1 PM today near the office?", 0),
    ("Please find attached the monthly financial report spreadsheet for your review.", 0),
    ("Don't forget to submit your project assignment before midnight tonight.", 0)
]

# 2. Tokenizer (Preprocesses text)
def tokenize(text):
    return text.lower().replace('.', '').replace(':', '').split()

# 3. Calculate Term Frequencies (TF-IDF & Naive Bayes Logic)
class NaiveBayesPhishingClassifier:
    def __init__(self):
        self.word_counts = {0: defaultdict(int), 1: defaultdict(int)}
        self.class_counts = {0: 0, 1: 0}
        self.vocab = set()

    def fit(self, data):
        for text, label in data:
            self.class_counts[label] += 1
            words = tokenize(text)
            for word in words:
                self.word_counts[label][word] += 1
                self.vocab.add(word)

    def predict(self, text):
        words = tokenize(text)
        total_docs = sum(self.class_counts.values())
        
        log_prob_safe = math.log(self.class_counts[0] / total_docs)
        log_prob_phish = math.log(self.class_counts[1] / total_docs)
        
        vocab_size = len(self.vocab)
        
        for word in words:
            prob_word_given_safe = (self.word_counts[0][word] + 1) / (sum(self.word_counts[0].values()) + vocab_size)
            prob_word_given_phish = (self.word_counts[1][word] + 1) / (sum(self.word_counts[1].values()) + vocab_size)
            
            log_prob_safe += math.log(prob_word_given_safe)
            log_prob_phish += math.log(prob_word_given_phish)
            
        max_log = max(log_prob_safe, log_prob_phish)
        exp_safe = math.exp(log_prob_safe - max_log)
        exp_phish = math.exp(log_prob_phish - max_log)
        confidence = (exp_phish / (exp_safe + exp_phish)) * 100
        
        if log_prob_phish > log_prob_safe:
            return 1, confidence
        return 0, 100 - confidence

# 4. Train the Classifier Instantly
classifier = NaiveBayesPhishingClassifier()
classifier.fit(train_corpus)
print("Pure Machine Learning Engine trained successfully!\n")

# 5. Interactive UI
print("=== Test the Model ===")
user_input = input("Paste an email text to analyze: ")

prediction, confidence = classifier.predict(user_input)

if prediction == 1:
    print(f"\n⚠️ Decision: PHISHING EMAIL (Model Confidence: {confidence:.2f}%)")
else:
    print(f"\n✅ Decision: SAFE EMAIL (Model Confidence: {confidence:.2f}%)")



# ==========================================
# 6. MODEL EVALUATION & STATISTICS PROFILE
# ==========================================
print("\n=== Generating Project Performance Metrics ===")

# Test Data for evaluation (Text, True Label)
validation_set = [
    ("Verify your banking info now.", 1),
    ("Winner of the lottery prize!", 1),
    ("Are you coming to the party later?", 0),
    ("The report document is attached.", 0)
]

true_positives = 0
false_positives = 0
true_negatives = 0
false_negatives = 0

for text, true_label in validation_set:
    pred_label, _ = classifier.predict(text)
    if pred_label == 1 and true_label == 1:
        true_positives += 1
    elif pred_label == 1 and true_label == 0:
        false_positives += 1
    elif pred_label == 0 and true_label == 0:
        true_negatives += 1
    elif pred_label == 0 and true_label == 1:
        false_negatives += 1

# Calculate Machine Learning Matrix Equations
total_tests = len(validation_set)
accuracy = ((true_positives + true_negatives) / total_tests) * 100

precision = (true_positives / (true_positives + false_positives) * 100) if (true_positives + false_positives) > 0 else 100
recall = (true_positives / (true_positives + false_negatives) * 100) if (true_positives + false_negatives) > 0 else 100
f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

print(f"📊 Model Global Accuracy : {accuracy:.2f}%")
print(f"🎯 Detection Precision  : {precision:.2f}%")
print(f"🔍 Sensitivity (Recall)  : {recall:.2f}%")
print(f"🧪 Balanced F1-Score     : {f1_score:.2f}%")
print("==============================================")
