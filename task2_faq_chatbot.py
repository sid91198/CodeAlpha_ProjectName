
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

for pkg in ["punkt", "punkt_tab", "stopwords", "wordnet"]:
    nltk.download(pkg, quiet=True)


FAQS = {
    "How can I track my order?": "Go to 'My Orders' and click 'Track'. You will also get a tracking link by email/SMS.",
    "What is your return policy?": "You can return products within 7 days of delivery if they are unused and in original packaging.",
    "How long does delivery take?": "Delivery usually takes 3-5 business days depending on your location.",
    "What payment methods do you accept?": "We accept UPI, credit/debit cards, net banking and cash on delivery.",
    "How do I cancel my order?": "Open 'My Orders', select the order and click 'Cancel' before it is shipped.",
    "How can I contact customer support?": "Email support@example.com or call 1800-123-456 (9 AM - 6 PM).",
    "Do you offer refunds?": "Yes, refunds are processed to the original payment method within 5-7 working days.",
}

lemmatizer = WordNetLemmatizer()
STOP = set(stopwords.words("english"))



def preprocess(text: str) -> str:
    text = text.lower().translate(str.maketrans("", "", string.punctuation))
    tokens = [lemmatizer.lemmatize(w) for w in word_tokenize(text) if w not in STOP]
    return " ".join(tokens)


questions = list(FAQS.keys())
vectorizer = TfidfVectorizer()
faq_matrix = vectorizer.fit_transform([preprocess(q) for q in questions])



GREETINGS = {"hi", "hy", "hii", "hello", "hey", "namaste", "hola"}
SMALL_TALK = ["how are you", "kya haal", "ky hall", "kaise ho", "kese ho", "whats up", "what's up"]
THANKS = {"thanks", "thank", "thankyou", "shukriya", "dhanyawad"}


def get_answer(user_q: str, threshold: float = 0.2) -> str:
    low = user_q.lower().strip()
    words = set(low.translate(str.maketrans("", "", string.punctuation)).split())

    if words & GREETINGS:
        return "Hello! Main aapki kaise madad kar sakta hoon? Order, delivery, return ya payment ke baare me poochhein."
    if any(p in low for p in SMALL_TALK):
        return "Main theek hoon, shukriya! Aap apna sawal poochhein."
    if words & THANKS:
        return "Aapka swagat hai! Aur kuch poochhna ho to bataiye."

    vec = vectorizer.transform([preprocess(user_q)])
    scores = cosine_similarity(vec, faq_matrix)[0]
    best = scores.argmax()
    if scores[best] < threshold:
        return ("Sorry, mujhe samajh nahi aaya. Aap in topics par poochh sakte hain: "
                "order tracking, return policy, delivery time, payment methods, "
                "cancel order, refund, customer support.")
    return FAQS[questions[best]]



if __name__ == "__main__":
    print("FAQ Bot: Hello! Apna sawal poochhein ('quit' likhkar exit karein).")
    while True:
        q = input("You: ").strip()
        if q.lower() in {"quit", "exit", "bye"}:
            print("FAQ Bot: Goodbye!")
            break
        print("FAQ Bot:", get_answer(q))