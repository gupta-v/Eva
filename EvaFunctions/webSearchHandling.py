import os
import webbrowser
from sr_tts import say
def webSearch(query):
            # Handle multiple possible search phrases
            if "search" in query.lower():
                search_query = query.lower().replace("search on the web for", "").replace("search on web for", "").replace("web search for","").replace("web search", "").strip()
                
            # Clean up by removing any leading phrase like "Eva"
            search_query = search_query.replace("eva", "").strip()  # Optionally remove "Eva" if it exists
            search_query = search_query.lstrip()  # Strip any leading unwanted words

            if search_query:  # Ensure the search query is not empty
                print("\nSearching on the web for:", search_query, flush=True)
                say(f"Searching on the web for: {search_query}")
                search_url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(search_url)
            else:
                print("\nNo search query found!", flush=True)
                say("I couldn't find any search query. Please try again.")