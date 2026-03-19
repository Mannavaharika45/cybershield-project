import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
FAKE_NEWS_MODEL_PATH = os.path.join(MODEL_DIR, 'fake_news_model.pkl')
SCAM_MSG_MODEL_PATH = os.path.join(MODEL_DIR, 'scam_msg_model.pkl')

# ─────────────────────────────────────────────────────────────────────────────
# TRAINING DATA — FAKE NEWS DETECTOR
# Label 1 = Fake/Misleading,   Label 0 = Real/Credible
# ─────────────────────────────────────────────────────────────────────────────
FAKE_NEWS_DATA = [
    # --- FAKE / MISLEADING ---
    ("Breaking: Aliens landed in New York and are handing out free gold!", 1),
    ("Government secretly tracking citizens through microchips injected in COVID vaccines.", 1),
    ("Scientists confirm drinking bleach cures cancer immediately.", 1),
    ("SHOCKING: 5G towers are spreading the coronavirus on purpose!", 1),
    ("Obama was born in Kenya, documents leaked by anonymous source prove.", 1),
    ("Bill Gates planning to use vaccines to implant mind-control devices.", 1),
    ("The moon landing was completely faked in a Hollywood studio.", 1),
    ("Chemtrails are secret government mind-control experiments!", 1),
    ("Eat this one weird fruit every morning to cure diabetes overnight.", 1),
    ("URGENT: The deep state is hiding a cure for all diseases from the public.", 1),
    ("Scientists reveal that Earth is actually flat and NASA has been lying!", 1),
    ("EXPOSED: The COVID virus was created in a lab by billionaires to reduce world population.", 1),
    ("Drinking hot water with lemon kills the coronavirus 100% guaranteed.", 1),
    ("Doctors do NOT want you to know about this miracle cure that reverses aging.", 1),
    ("BREAKING: Massive voter fraud uncovered in all 50 states — election stolen!", 1),
    ("Secret documents reveal lizard people run global governments.", 1),
    ("FBI whistleblower reveals the moon is a hollow alien spacecraft.", 1),
    ("George Soros single-handedly controls every world election using Dominion machines.", 1),
    ("MIRACLE: Man cured stage-4 cancer overnight using apple cider vinegar.", 1),
    ("Anonymous hacker leaks proof that Hollywood celebrities are cannibals.", 1),
    ("The real reason doctors push vaccines is to make you sick and keep you coming back.", 1),
    ("NASA scientists admit they've been hiding alien life on Mars for 40 years.", 1),
    ("New study PROVES that Wi-Fi causes autism in children under 5.", 1),
    ("Globalists plan to eliminate 90% of Earth's population by 2030!", 1),
    ("BOMBSHELL: IRS never legally authorized to collect income tax — don't pay!", 1),
    ("Man heals blindness in neighbor's dog by rubbing special oil on its eyes.", 1),
    ("Bigfoot captured in rural Montana — government suppressing story.", 1),
    ("Facebook and CIA are the same organization — leaked memo proves it.", 1),
    ("Scientists bought by Big Pharma to hide link between sugar and all disease.", 1),
    ("This simple trick revealed by a grandma eliminates belly fat in 3 days!", 1),
    ("ALERT: Water fluoridation is a chemical weapon deployed by globalists.", 1),
    ("Anonymous insider: World leaders meet secretly to plan next pandemic.", 1),
    ("WARNING: New law lets government seize your bank account without notice.", 1),
    ("Military sources confirm: US has been at war with underground aliens since 1947.", 1),
    ("The Vatican is hoarding a library of books that would destroy Christianity.", 1),
    ("COVID-19 vaccines cause 5G signal transmission in your blood.", 1),
    ("BREAKING NEWS: Elvis Presley spotted alive working at a gas station in Memphis.", 1),
    ("Exposed: Major supermarkets putting addictive chemicals in food to control consumers.", 1),
    ("Doctors admit prescription drugs kill more people than all illegal drugs combined — suppressed study.", 1),
    ("Insider reveals the true purpose of airport scanners: DNA harvesting.", 1),
    ("BOMBSHELL: Every US president since 1963 has been a CIA puppet — documents revealed.", 1),
    ("New research shows sunscreen causes cancer more than sun exposure.", 1),
    ("URGENT: New 5G rollout killing birds and insects — media blackout in place.", 1),
    ("Secret society of Freemasons controls every major financial institution on Earth.", 1),
    ("PROOF: Time travel used by elites to manipulate historical events.", 1),
    ("Government mind-control program revealed: TV is transmitting subliminal orders.", 1),
    ("Health experts unanimously agree: vegetables are harmful to your kidneys.", 1),
    ("Bombshell leak: Major airline adding sedatives to recirculated cabin air.", 1),
    ("Politician caught on camera admitting vaccines are a depopulation tool.", 1),
    ("Scientists silenced for proving that autism is caused by GMO corn.", 1),

    # --- REAL / CREDIBLE ---
    ("The Federal Reserve raised interest rates by 25 basis points at today's meeting.", 0),
    ("Scientists have discovered a new species of deep-sea fish near the Mariana Trench.", 0),
    ("The President signed a bipartisan infrastructure bill into law on Friday.", 0),
    ("A local football team won the national championship after a comeback victory.", 0),
    ("Researchers at Johns Hopkins have published a peer-reviewed study on Alzheimer's progression.", 0),
    ("Stock market closed higher on Friday driven by strong earnings from tech companies.", 0),
    ("The World Health Organization released new guidelines on childhood vaccination schedules.", 0),
    ("A 7.2 magnitude earthquake struck southern Turkey on Thursday.", 0),
    ("NASA's James Webb Space Telescope captured the deepest infrared image of the universe.", 0),
    ("Apple reported record quarterly earnings of $90 billion in revenue.", 0),
    ("The United Nations Security Council met to discuss the humanitarian crisis in Sudan.", 0),
    ("Scientists have achieved a new breakthrough in nuclear fusion energy output.", 0),
    ("The European Central Bank held interest rates steady at its July meeting.", 0),
    ("Local government announces a $500 million investment in public transportation.", 0),
    ("A new COVID-19 variant has been detected in several countries — scientists studying its severity.", 0),
    ("The Supreme Court issued a ruling on free speech rights in digital media.", 0),
    ("Global temperatures in 2023 were the highest recorded in 174 years of observation.", 0),
    ("A bipartisan group of senators introduced a bill to strengthen cybersecurity infrastructure.", 0),
    ("General Motors announced plans to produce 400,000 electric vehicles by 2025.", 0),
    ("The unemployment rate fell to 3.7% last month, according to the Bureau of Labor Statistics.", 0),
    ("Scientists sequenced the complete genome of the honey bee for the first time.", 0),
    ("A Harvard study finds regular exercise reduces risk of heart disease by 35%.", 0),
    ("The Olympic committee voted to add breakdancing as an official sport.", 0),
    ("Floods in Pakistan displaced more than 30 million people this year.", 0),
    ("Pfizer announced positive Phase 3 trial results for its RSV vaccine.", 0),
    ("The International Monetary Fund revised global growth forecast downward to 2.9%.", 0),
    ("A new archaeological dig in Egypt uncovered a 3,000-year-old burial site.", 0),
    ("Twitter was acquired by Elon Musk for approximately $44 billion.", 0),
    ("Surgeons performed the first ever full-eye transplant on a human patient.", 0),
    ("The Bank of England raised rates for the 10th consecutive time to combat inflation.", 0),
    ("Scientists map the neural pathways of a mouse brain in complete detail.", 0),
    ("The Hubble Space Telescope celebrates its 33rd year of continuous operation.", 0),
    ("Amazon reported stronger than expected Q4 results driven by AWS cloud growth.", 0),
    ("The Senate confirmed a new member to the Federal Reserve board.", 0),
    ("A new study in The Lancet links ultra-processed food consumption to premature death.", 0),
    ("SpaceX successfully launched 60 Starlink satellites into low Earth orbit.", 0),
    ("The CDC updated mask guidance for high-risk individuals during respiratory virus season.", 0),
    ("Researchers develop a biodegradable plastic that decomposes within six months.", 0),
    ("UN climate summit reached agreement on phasing out coal power by 2030.", 0),
    ("The World Bank approved a $2 billion loan to help developing nations with energy transition.", 0),
    ("Scientists confirm that the Milky Way has four spiral arms, not two.", 0),
    ("The FDA approved a new drug for treatment-resistant depression.", 0),
    ("Microsoft announced a multi-billion dollar investment in AI infrastructure.", 0),
    ("NASA's Perseverance rover collected its 23rd Martian rock sample.", 0),
    ("The Federal Trade Commission filed an antitrust case against Meta.", 0),
    ("A study published in Nature found microplastics in human heart tissue for the first time.", 0),
    ("Record rainfall caused severe flooding across parts of central Europe.", 0),
    ("The Nobel Prize in Medicine was awarded for discoveries on mRNA vaccine technology.", 0),
    ("Researchers at MIT created a new battery that charges 10x faster than lithium-ion.", 0),
    ("The IMF warned that global debt has reached an all-time high of $235 trillion.", 0),
]

# ─────────────────────────────────────────────────────────────────────────────
# TRAINING DATA — SCAM MESSAGE DETECTOR
# Label 1 = Scam,   Label 0 = Legitimate
# ─────────────────────────────────────────────────────────────────────────────
SCAM_MSG_DATA = [
    # --- SCAM ---
    ("URGENT: Your bank account has been suspended. Click here immediately to verify your identity.", 1),
    ("Congratulations! You've won a $1000 Amazon gift card. Reply with your SSN to claim.", 1),
    ("I am a Nigerian prince and I need your help to transfer $10 million out of the country.", 1),
    ("Your package delivery has failed. Pay a $2.99 customs fee now or it will be returned.", 1),
    ("Your Apple ID has been hacked! Click this link to restore access immediately.", 1),
    ("WINNER: You have been selected for a free iPhone 15. Provide your address to receive it.", 1),
    ("Dear customer, your Netflix account will be closed in 24 hours. Update billing here.", 1),
    ("We have noticed unusual activity on your PayPal account. Verify now to avoid suspension.", 1),
    ("Claim your $750 Cash App reward! You have been pre-selected. Limited time offer.", 1),
    ("Your Social Security number has been suspended due to suspicious activity. Call now.", 1),
    ("IRS ALERT: You owe $3,245 in unpaid taxes. Failure to pay will result in immediate arrest.", 1),
    ("Your computer is infected with 5 viruses! Call Microsoft support now: 1-800-xxx.", 1),
    ("You've been approved for a $50,000 loan! No credit check needed. Click to claim.", 1),
    ("Dear valued member, your account has been flagged. Confirm identity to avoid closure.", 1),
    ("Free trial winner! Enter your credit card for shipping only — $0 subscription for life.", 1),
    ("SOS: Hello I am stranded in London and have lost my wallet. Please send $500 urgent.", 1),
    ("Exclusive investment opportunity — guaranteed 30% monthly returns. Act now, limited spots.", 1),
    ("Your WhatsApp account will expire in 24 hours unless you upgrade for free here.", 1),
    ("WARNING: Your device has been compromised. Download our security app immediately.", 1),
    ("FINAL NOTICE: Pay your overdue electric bill of $197 now or service will be cut off today.", 1),
    ("Congratulations, your survey is complete! Claim your $500 Walmart voucher here.", 1),
    ("Your Google Account has been hacked from an unknown device. Verify now to secure it.", 1),
    ("Bitcoin giveaway: Send 0.1 BTC and we will send back 0.5 BTC. Limited time offer!", 1),
    ("Hi [Name], it's your bank. We need you to verify your PIN for a security update.", 1),
    ("LAST WARNING: Your phone number has been selected for $1000 cashback. Claim before midnight!", 1),
    ("Weight loss secret doctors don't want you to know — lost 30 lbs in 2 weeks. Buy now.", 1),
    ("New government stimulus check of $1400 unclaimed in your name. Verify SSN to receive.", 1),
    ("Your email won our monthly lottery. To receive £850,000 send processing fee of £50.", 1),
    ("URGENT: Wire $4,500 immediately using Google Play gift cards. This is your boss.", 1),
    ("Earn $3,000/week working from home — no experience needed! Sign up fee only $49.", 1),
    ("Hello dear, I am soldier deployed overseas with gold bars. Please help me transfer them safely.", 1),
    ("Charity donation — please help feed starving children in Africa. Send money via Western Union.", 1),
    ("Your car warranty is about to expire. Press 1 to speak with an agent immediately.", 1),
    ("We found your resume online. You are hired! Pay $150 training fee to begin Monday.", 1),
    ("CRYPTO ALERT: Elon Musk is giving away 10,000 BTC. Send 0.01 to confirm address.", 1),
    ("You owe unpaid tolls. Pay $2.85 immediately to avoid $75 late fee.", 1),
    ("Free $1000 VISA gift card — fill out this one-minute survey, no strings attached!", 1),
    ("Technical Support: Your Windows license has expired. Call now or your data will be deleted.", 1),
    ("You have been chosen as our lucky customer. Reply YES to claim your cash prize.", 1),
    ("Click the link below to unsubscribe or your account will be charged $29.99 monthly fee automatically.", 1),
    ("Investment tip: This penny stock will 10x next week. Buy now before it hits mainstream.", 1),
    ("I saw your photo and fell in love. I am a model overseas — please help me with visa money.", 1),
    ("Your mortgage refinance was approved at 1.9% APR! No documents needed, just a small fee.", 1),
    ("RARE URGENT: A large sum in your deceased relative's name. Contact me to claim inheritance.", 1),
    ("Your streaming service subscription failed. Update payment to keep access uninterrupted.", 1),
    ("Act now! Only 5 spots left in our crypto investment club — guaranteed 200% weekly profits.", 1),
    ("Free government phone! You qualify. Just pay $5 shipping and handling today.", 1),
    ("You have an unclaimed tax refund of $1,240. Submit your bank details to receive it.", 1),
    ("Hello I need someone trustworthy to help safeguard $22 million from corrupt officials.", 1),
    ("Virus detected on your device! Install our FREE antivirus immediately. Tap the link below.", 1),

    # --- LEGITIMATE ---
    ("Hey! Are we still meeting for lunch tomorrow at noon?", 0),
    ("Please review the attached project proposal and provide your feedback by Friday.", 0),
    ("Happy birthday! Hope you have a wonderful day filled with joy.", 0),
    ("The team meeting has been moved to 3 PM in Conference Room B.", 0),
    ("Just wanted to check in – how are you feeling after the procedure?", 0),
    ("Your order #45821 has been shipped and is expected to arrive Thursday.", 0),
    ("Hi, I'm following up on the interview we had last week. Do you have any updates?", 0),
    ("The quarterly sales report is attached. Please review before tomorrow's presentation.", 0),
    ("Reminder: Your dentist appointment is scheduled for Monday at 10:00 AM.", 0),
    ("Can you pick up some milk on your way home? We're out.", 0),
    ("The kids are at soccer practice until 5 PM. I'll meet you at the restaurant.", 0),
    ("I looked at the code you pushed — there's a small bug in the auth module, let's discuss.", 0),
    ("Your flight to London is confirmed! Check-in opens 24 hours before departure.", 0),
    ("Thanks for dinner last night — it was so great catching up with everyone!", 0),
    ("The library book you placed on hold is now available for pickup.", 0),
    ("Just a friendly reminder your rent is due on the 1st of next month.", 0),
    ("We wanted to share the agenda for next week's company all-hands meeting.", 0),
    ("Congratulations on your promotion! You truly deserved it.", 0),
    ("Is the design mockup ready? The client is asking for an update.", 0),
    ("Your refund of $34.99 has been processed and will appear in 3-5 business days.", 0),
    ("Hi Mom, I landed safely — will call tonight when I'm settled in.", 0),
    ("Please RSVP by Friday if you plan to attend the networking event.", 0),
    ("Your prescription from Dr. Smith is ready for pickup at the pharmacy.", 0),
    ("The power will be out in your area from 9 AM to 12 PM tomorrow for maintenance.", 0),
    ("We've reviewed your application and would like to schedule a technical interview.", 0),
    ("Hey, can we reschedule our call to Thursday? Something came up.", 0),
    ("Your monthly bank statement is ready to view in your online banking portal.", 0),
    ("We'll be at the park this weekend — you're all welcome to join us!", 0),
    ("The annual report has been filed with the SEC as required.", 0),
    ("Just texting to say I'm running 10 minutes late. Sorry!", 0),
    ("The gym is closed for renovations but will reopen on the 15th.", 0),
    ("Final reminder: city council meeting tonight at 7 PM.", 0),
    ("Your Amazon order was delivered to your front door at 2:34 PM.", 0),
    ("The professor uploaded the lecture slides to the course portal.", 0),
    ("We'd love for you to come to our housewarming party this Saturday.", 0),
    ("Your insurance claim has been approved — a check will be mailed within 10 days.", 0),
    ("The new employee onboarding documents are attached. Please complete by Monday.", 0),
    ("Sales are up 12% this quarter — great work by the whole team!", 0),
    ("Did you catch the game last night? Incredible comeback in the third quarter.", 0),
    ("The recycling center will not accept electronics this weekend.", 0),
    ("Your test results from the lab came back normal — no concerns.", 0),
    ("Joining you a bit late today — stuck in traffic near downtown.", 0),
    ("Customer satisfaction survey: How was your experience with us today?", 0),
    ("We've decided to go with another candidate, but we appreciate your interest.", 0),
    ("The annual subscription auto-renews next month — no action needed if you wish to continue.", 0),
    ("Reminder: submit your timesheet by 5 PM every Friday.", 0),
    ("Your bus pass has been loaded with $50. Have a great commute!", 0),
    ("Happy holidays from our entire team! Looking forward to a great new year.", 0),
    ("The contract review is complete. You can sign electronically via DocuSign.", 0),
    ("I finished reading the book you recommended — absolutely loved it, thanks!", 0),
]


def train_fake_news_model():
    texts = [item[0] for item in FAKE_NEWS_DATA]
    labels = [item[1] for item in FAKE_NEWS_DATA]

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),      # unigrams + bigrams for richer signal
            max_features=10000,
            sublinear_tf=True,       # log-normalise term frequencies
            min_df=1
        )),
        ('clf', LogisticRegression(
            C=5.0,
            max_iter=1000,
            class_weight='balanced'  # handle any class imbalance
        ))
    ])
    pipeline.fit(texts, labels)

    with open(FAKE_NEWS_MODEL_PATH, 'wb') as f:
        pickle.dump(pipeline, f)
    print(
        f"[ML] Fake news model trained on {
            len(texts)} samples → {FAKE_NEWS_MODEL_PATH}")


def train_scam_msg_model():
    texts = [item[0] for item in SCAM_MSG_DATA]
    labels = [item[1] for item in SCAM_MSG_DATA]

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=10000,
            sublinear_tf=True,
            min_df=1
        )),
        ('clf', LogisticRegression(
            C=5.0,
            max_iter=1000,
            class_weight='balanced'
        ))
    ])
    pipeline.fit(texts, labels)

    with open(SCAM_MSG_MODEL_PATH, 'wb') as f:
        pickle.dump(pipeline, f)
    print(
        f"[ML] Scam model trained on {
            len(texts)} samples → {SCAM_MSG_MODEL_PATH}")


def load_fake_news_model():
    # Always retrain to pick up latest dataset changes
    train_fake_news_model()
    with open(FAKE_NEWS_MODEL_PATH, 'rb') as f:
        return pickle.load(f)


def load_scam_msg_model():
    train_scam_msg_model()
    with open(SCAM_MSG_MODEL_PATH, 'rb') as f:
        return pickle.load(f)


# Models loaded (and retrained) at startup
fake_news_model = load_fake_news_model()
scam_msg_model = load_scam_msg_model()


def predict_fake_news(text: str) -> dict:
    if not text.strip():
        return {
            "is_fake": False,
            "confidence": 0,
            "label": "No input provided"}

    prediction = fake_news_model.predict([text])[0]
    probabilities = fake_news_model.predict_proba([text])[0]
    is_fake = bool(prediction == 1)
    # Use probability of the predicted class as confidence
    confidence = float(probabilities[1] if is_fake else probabilities[0]) * 100

    return {
        "is_fake": is_fake,
        "confidence": round(confidence, 2),
        "label": "Fake News" if is_fake else "Real News"
    }


def predict_scam_message(text: str) -> dict:
    if not text.strip():
        return {
            "is_scam": False,
            "confidence": 0,
            "label": "No input provided"}

    prediction = scam_msg_model.predict([text])[0]
    probabilities = scam_msg_model.predict_proba([text])[0]
    is_scam = bool(prediction == 1)
    confidence = float(probabilities[1] if is_scam else probabilities[0]) * 100

    return {
        "is_scam": is_scam,
        "confidence": round(confidence, 2),
        "label": "Scam Message" if is_scam else "Safe Message"
    }


if __name__ == "__main__":
    train_fake_news_model()
    train_scam_msg_model()
    print("Models trained successfully.")
