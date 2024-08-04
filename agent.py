from openai import OpenAI
import json
import requests


openai_api_key = "sk-"
google_books_api  = ""


class OpenAIClient:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
def searchBooks(function_call):
    # Google Books API URL
    #filter = "full"
    if 'filter' in function_call and function_call['filter']:
        url = f"https://www.googleapis.com/books/v1/volumes?q={function_call['topic']}&filter={function_call['filter']}&key={google_books_api}"
    else:
        url = f"https://www.googleapis.com/books/v1/volumes?q={function_call['topic']}&key={google_books_api}"
    
    # API'ye istek gönder
    response = requests.get(url)
    
    # Yanıtı JSON formatında al
    data = response.json()
    
    # Kitapların listesini al
    books = data.get('items', [])

    return books

class BookSearchAgent:
    def __init__(self):
        self.api_key = openai_api_key
        self.google_books_api = google_books_api
        self.client = OpenAIClient(api_key=openai_api_key)

    def search_books(self,topic):   
        response = self.client.client.chat.completions.create(
            model="gpt-3.5-turbo",  # gpt-3.5-turbo-0613 deprecated
            messages=[
                {"role":"system","content":"You are a helpful asistan that find books"},
                {"role":"user","content":f"Find me a book about {topic}"}
            ],
            functions = [
                {
                    "name": "findBooks",
                    "description": "Find topic about text",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "A topic about books",
                            }, 
                            "filter": {
                                "type": "string",
                                "description": (
                                    "Choose one of the following options based on the user's needs: "
                                    "'partial' (partially available), 'full' (fully available), "
                                    "'free-ebooks' (free books), 'paid-ebooks' (paid books), "
                                    "'ebooks' (digital books)."),
                                # "description": (
                                #     "Choose one of the following options based on the user's needs: "
                                #     "'partial', 'full','free-ebooks','paid-ebooks','ebooks'"
                                #     ),
                                "enum": ["partial","full","free-ebooks","paid-ebooks","ebooks"],
                                ##"default": "full"
                            }      
                        },
                        "required": ["topic"],
                    },
                }
            ],
            function_call="auto", 
            temperature=0
        )
        response_message = response.choices[0].message
        function_call = json.loads(response_message.function_call.arguments)
        print("calling",function_call)
        books = searchBooks(function_call)

        return books
    
class BookFilterAgent:
    def __init__(self):
        self.client = OpenAIClient(api_key=openai_api_key)

    def detect_language(self, text):
        response = self.client.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a language detection assistant."},
                {"role": "user", "content":  f"Return detected language code (like 'TR', 'EN', 'FR') of this text: {text}"}
            ],
            functions=[
                {
                    "name": "detect_language_code",
                    "description": "Detects the language code of a given text.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "language_code": {
                                "type": "string",
                                "description": "The detected language code."
                            }
                        },
                        "required": ["language_code"]
                    }
                }
            ],
            function_call={"name": "detect_language_code"},
            temperature=0
        )
        response_message = response.choices[0].message
        language_code = json.loads(response_message.function_call.arguments)
        print("language",language_code)
        return language_code

        
    def filter_books(self, books,lang_code):
        filtered_books = [book for book in books if book['saleInfo']['country'] == lang_code['language_code']]
        
        for book in books:
            print(book['saleInfo']['country'])
        return filtered_books
    
class CoordinatorAgent:
    def __init__(self, search_agent, filter_agent):
        self.search_agent = search_agent
        self.filter_agent = filter_agent

    def find_and_filter_books(self, topic):
        books = self.search_agent.search_books(topic)
        #print(books)
        lang_code =  self.filter_agent.detect_language(topic)
        filtered_books = self.filter_agent.filter_books(books,lang_code)
        return filtered_books