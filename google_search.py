import requests
from config import GOOGLE_API_KEY, GOOGLE_CX, GOOGLE_SEARCH_URL 

def google_search(query):
    try:
        params = {
            "q": query,
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CX,
            "num": 3  # Retrieve top 3 results for better accuracy
        }
        response = requests.get(GOOGLE_SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "items" in data:
            answers = []
            for item in data["items"]:
                title = item.get("title")
                snippet = item.get("snippet")
                link = item.get("link")
                if snippet and len(snippet.split()) > 5:
                    answers.append(f"{title}: {snippet}")
                
                if len(answers) >= 2:
                    break

            if answers:
                return ' '.join(answers) #f"Here is what I found: {' '.join(answers)}"
            else:
                return "I couldn't find a relevant answer. Please try rephrasing your question."
        else:
            return "Sorry, I couldn't find any results for your question."
    
    except Exception as e:
        print(f"Error with Google search API: {e}")
        return "Sorry, I encountered an error while searching. Please try again later."
