import urllib.request
print("--- Phishing Email Detection Model ---")

# Simple placeholder logic for testing
def detect_phishing(email_text):
    spam_words = ["bank", "verify", "password", "urgent", "login", "click here"]
    for word in spam_words:
        if word in email_text.lower():
            return "⚠️ Warning: Potential Phishing Email Detected!"
    return "✅ Clean Email."

test_email = "Urgent: Please verify your bank account password immediately."
print(f"Testing email: '{test_email}'")
print(detect_phishing(test_email))

