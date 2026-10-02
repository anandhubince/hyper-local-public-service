from flask import *
from database import select  # Your DB helper
from googletrans import Translator  # pip install googletrans==4.0.0-rc1
from gtts import gTTS  # pip install gtts
import tempfile





from google.genai import Client
from google.genai.types import GenerateContentConfig, Tool, GoogleSearch
import os
from deep_translator import GoogleTranslator

user = Blueprint('user', __name__)
translator = Translator()

# -------------------------------
# Translate text
# -------------------------------# -------------------------------
# Translate text
# -------------------------------
def translate_text(text, target_lang):
    if target_lang == 'en':
        return text
    try:
        return GoogleTranslator(
            source="auto",
            target=target_lang
        ).translate(text)
    except Exception as e:
        print("Translation error:", e)
        return text


# -------------------------------
# User Home Page
# -------------------------------
@user.route('/user_home')
def user_home():
    q = """
        SELECT news.*, agent.fname AS agent_name
        FROM news
        INNER JOIN agent ON news.agent_id = agent.agent_id
        ORDER BY news.news_id DESC
    """
    news_list = select(q)
    return render_template("user_home.html", data={'img': news_list})

# -------------------------------
# Translate News API
# -------------------------------
@user.route('/translate_news', methods=['POST'])
def translate_news():
    news_id = int(request.json.get('news_id'))
    target_lang = request.json.get('lang')

    q = f"""
        SELECT news.*, agent.fname AS agent_name
        FROM news
        INNER JOIN agent ON news.agent_id = agent.agent_id
        WHERE news.news_id = {news_id}
    """
    news_item = select(q)
    if not news_item:
        return jsonify({'error': 'News not found'}), 404
    news_item = news_item[0]

    translated_title = translate_text(news_item['title'], target_lang)
    translated_details = translate_text(news_item['details'], target_lang)

    return jsonify({'title': translated_title, 'details': translated_details})

# -------------------------------
# Read News with TTS
# -------------------------------
@user.route('/read_news', methods=['POST'])
def read_news():
    news_id = int(request.json.get('news_id'))
    lang = request.json.get('lang', 'en')

    q = f"SELECT news.* FROM news WHERE news_id = {news_id}"
    news_item = select(q)
    if not news_item:
        return jsonify({'error': 'News not found'}), 404
    news_item = news_item[0]

    text = f"{news_item['title']}. {news_item['details']}"
    text_translated = translate_text(text, lang)

    lang_map = {'en': 'en', 'hi': 'hi', 'ta': 'ta', 'ml': 'ml'}
    tts_lang = lang_map.get(lang, 'en')

    tts = gTTS(text=text_translated, lang=tts_lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)

    return send_file(temp_file.name, mimetype="audio/mpeg", as_attachment=False)






# NOTE: The API key below is a placeholder provided by the user.
# In a real deployment, please use a secure method to load your actual API key.
# For demonstration purposes, we use the user-provided placeholder value here.
# api_key = 'AIzaSyB1FCp7vt_vwpkZ2ebTi7IdcPsGyBlqU7Y'
# We'll use an environment variable check as a best practice, but default to the placeholder.
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyB1FCp7vt_vwpkZ2ebTi7IdcPsGyBlqU7Y")

class FakeNewsDetection:
    """Handles interaction with the Gemini API for fake news detection."""
    def __init__(self, api_key):
        # Initialize the Gemini client
        self.client = Client(api_key=api_key)

        # System Instruction for the model: output only REAL or FAKE
        self.system_prompt = """You are an expert fake news detection assistant. 
Analyze the provided news content using Google Search. 
Your job is to determine if the claim is REAL or FAKE.
Output must be ONLY one word: REAL or FAKE.
Use Google Search grounding for factual verification.
Do NOT include explanations or extra text."""

        # Trusted news sites (domains) for filtering sources
        self.trusted_sources = [
            "indiatoday.in", "bbc.com", "cnn.com", "ndtv.com", "thehindu.com",
            "timesofindia.indiatimes.com", "hindustantimes.com", "reuters.com",
            "news18.com", "malayalam.manoramaonline.com", "mathrubhumi.com",
            "onmanorama.com", "theguardian.com", "aljazeera.com", "business-standard.com",
            "economictimes.indiatimes.com", "deccanchronicle.com", "newindianexpress.com"
        ]

    def get_response(self, user_input):
        """Generates content and extracts verification details."""
        try:
            grounding_tool = Tool(google_search=GoogleSearch())
            config = GenerateContentConfig(
                tools=[grounding_tool],
                system_instruction=self.system_prompt
            )

            # Generate content from the model
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_input,
                config=config
            )

            verdict = response.text.strip().upper()

            # --- Extract trusted sources with snippets (links and titles) ---
            news_details = []
            
            # Check for grounding supports (Gemini 2.5)
            if hasattr(response, "grounding") and response.grounding:
                for item in getattr(response.grounding, "supports", []):
                    # In this SDK, supports are often returned as dicts with uri and text
                    url = item.get("uri", "")
                    snippet = item.get("text", "")
                    if url and any(domain in url for domain in self.trusted_sources):
                        news_details.append((snippet, url))
            
            # Check for citations (Older structure or alternative)
            elif hasattr(response, "citations") and response.citations:
                for cite in response.citations:
                    url = cite.get("uri", "")
                    snippet = cite.get("title", "") # Use title as snippet fallback
                    if url and any(domain in url for domain in self.trusted_sources):
                        news_details.append((snippet, url))

            # --- Build final response in Markdown format ---
            if verdict == "REAL":
                message = f"✅ **VERIFIED REAL NEWS**\n\nThe news you submitted has been verified as true:\n\n*\"{user_input}\"*"

                if news_details:
                    message += "\n\n📰 **Reported Details from Trusted Sources:**"
                    for i, (snippet, link) in enumerate(news_details, 1):
                        # Format the output to clearly show the snippet and the full link
                        message += f"\n\n**{i}. Snippet:** {snippet}\n**Source:** {link}"
                else:
                    message += "\n\n(Verification successful, but no direct news details from major trusted outlets were available in the search grounding.)"

                return message

            elif verdict == "FAKE":
                return f"❌ **FAKE NEWS DETECTED**\n\nThe following news appears to be false or misleading:\n\n*\"{user_input}\"*\n\n**Note:** This claim could not be verified by searching major trusted news sources."

            else:
                return f"⚠️ **VERDICT UNCLEAR**\n\nUnable to determine the verdict for the claim:\n\n*\"{user_input}\"*\n\nPlease rephrase or provide more context."

        except Exception as e:
            # Simple exponential backoff retry logic is omitted here but recommended for production
            print(f"Gemini API Error: {e}")
            return f"⚠️ **API ERROR**\n\nGemini API failed to process the request: {str(e)}"
        
        
        
bot = FakeNewsDetection(API_KEY)

@user.route("/chat")
def chat():
    """Renders the HTML template for the chat interface."""
    return render_template("chat.html")

@user.route("/get_response", methods=["POST"])
def get_chat_response():
    """Endpoint to handle news submission and return verification result."""
    user_input = request.json.get("user_input", "").strip()
    if not user_input:
        return jsonify({"response": "Please enter a news item or claim to verify."})

    response_text = bot.get_response(user_input)
    return jsonify({"response": response_text})

# def scrape_news(url):
#     try:
#         response = requests.get(url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         # Try to find the main article text
#         article = soup.find('article')
#         if article:
#             text = article.get_text()
#         else:
#             # Fallback to body text
#             text = soup.body.get_text() if soup.body else soup.get_text()
#         return text.strip()
#     except Exception as e:
#         return f"Error scraping URL: {str(e)}"

# def research_check(news_text):
#     try:
#         lang = detect(news_text)
#     except:
#         lang = 'en'

#     # Extract key phrases or title
#     sentences = re.split(r'[.!?]', news_text)
#     key_phrase = sentences[0].strip() if sentences else news_text[:100]

#     if lang == 'en':
#         # Search on fact-checking sites
#         sites = ['https://www.snopes.com', 'https://www.factcheck.org', 'https://www.politifact.com']
#         for site in sites:
#             try:
#                 search_url = f"{site}/search/?q={requests.utils.quote(key_phrase)}"
#                 response = requests.get(search_url, timeout=10)
#                 if 'false' in response.text.lower() or 'fake' in response.text.lower():
#                     return "This news appears to be Fake based on external research."
#                 elif 'true' in response.text.lower() or 'real' in response.text.lower():
#                     return "This news appears to be Real based on external research."
#             except:
#                 continue
#         return "No conclusive evidence found from external sources. Please verify manually."
#     else:
#         # For non-English, use Google search
#         google_url = f"https://www.google.com/search?q={requests.utils.quote(key_phrase + ' fake news')}"
#         try:
#             response = requests.get(google_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
#             if 'debunked' in response.text.lower() or 'false' in response.text.lower():
#                 return f"This {lang} news appears to be Fake based on external research."
#             elif 'verified' in response.text.lower() or 'true' in response.text.lower():
#                 return f"This {lang} news appears to be Real based on external research."
#         except:
#             pass
#         return f"No conclusive evidence found from external sources for {lang} news. Please verify manually."

# @user.route('/live_check', methods=['GET', 'POST'])
# def live_check():
#     if request.method == 'POST':
#         url = request.form['url']
#         check_type = request.form.get('check_type', 'ai')
#         news_text = scrape_news(url)
#         if news_text.startswith("Error"):
#             return render_template('live_check.html', error=news_text)
#         if check_type == 'ai':
#             out = predict(news_text)
#         elif check_type == 'research':
#             out = research_check(news_text)
#         else:
#             out = "Invalid check type"
#         return redirect(url_for("user.view_res", out=out))
#     return render_template('live_check.html')





@user.route('/places_finder')
def places_finder():
    return render_template("places_finder.html")