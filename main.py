#Go to 1156 change budget to real numbers for easier use
import pandas as pd
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import openai
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import datetime

# Page config and styling
st.set_page_config(
    page_title="TravelTunes AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling with Luxair-inspired color scheme
st.markdown("""
<style>
    /* Main color palette - Luxair inspired */
    :root {
        --primary: #003F7D;       /* Luxair Blue */
        --secondary: #97BF0D;     /* Luxair Green */
        --accent1: #FF5000;       /* Luxair Orange */
        --accent2: #707070;       /* Luxair Gray */
        --light-bg: #f6f9fc;
        --text-color: #333;
        --light-text: #6c757d;
    }
    
    /* General styles */
    body {
        background: var(--light-bg);
        color: var(--text-color);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        color: var(--primary);
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: var(--primary);
        margin-bottom: 1rem;
        border-left: 4px solid var(--secondary);
        padding-left: 10px;
        font-weight: 600;
    }
    
    /* Card containers */
    .card {
        padding: 25px;
        border-radius: 8px;
        background-color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
        border-top: 3px solid var(--primary);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.08);
    }
    
    /* Information sections */
    .country-info {
        background-color: var(--light-bg);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid var(--primary);
    }
    
    .travel-tips {
        background-color: var(--light-bg);
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        border-left: 4px solid var(--secondary);
    }
    
    /* Song items styling */
    .song-item {
        padding: 15px;
        background-color: white;
        border-left: 3px solid var(--secondary);
        margin-bottom: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    
    .song-item:hover {
        transform: scale(1.01);
    }
    
    /* Buttons */
    .stButton>button {
        background: var(--primary);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 4px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: var(--accent1);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-right: 5px;
        font-weight: 600;
    }
    
    .badge-primary {
        background-color: var(--primary);
        color: white;
    }
    
    .badge-secondary {
        background-color: var(--secondary);
        color: white;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 30px;
        border-top: 1px solid #eee;
        color: var(--light-text);
    }

    /* Country stats */
    .stat-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        margin-bottom: 15px;
    }
    
    .stat-item {
        background: white;
        border-radius: 8px;
        padding: 15px;
        width: 31%;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stat-value {
        font-size: 1.3rem;
        font-weight: bold;
        color: var(--primary);
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--light-text);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: white;
        border-radius: 5px;
        color: var(--text-color);
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--primary) !important;
        color: white !important;
    }

    /* Travel form styling */
    .travel-form-container {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .form-header {
        color: var(--primary);
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 15px;
        border-bottom: 2px solid var(--secondary);
        padding-bottom: 8px;
    }
    
    /* Luxair-like navigation */
    .luxair-navbar {
        background-color: var(--primary);
        padding: 10px 20px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-radius: 8px;
    }
    
    .luxair-logo {
        font-size: 1.5rem;
        font-weight: bold;
        letter-spacing: 1px;
    }
    
    .nav-links {
        display: flex;
        gap: 20px;
    }
    
    .nav-item {
        color: white;
        text-decoration: none;
        font-weight: 500;
        padding: 5px 10px;
        border-radius: 4px;
        transition: background-color 0.2s;
    }
    
    .nav-item:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .stat-item {
            width: 100%;
            margin-bottom: 10px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Spotify API client
@st.cache_resource
def get_spotify_client():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=st.secrets["SPOTIFY_ID"] , 
        client_secret=st.secrets["SPOTIFY_SECRET"]
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Set up OpenAI API key (for travel guide)
# Note: In a production app, you should use environment variables or secrets management
openai.api_key = st.secrets["OPENAI_KEY"]

sp = get_spotify_client()

# Enhanced country data with more details
countries = { 
    "Luxembourg": {
        "code": "LU", 
        "lat": 49.8153, 
        "lon": 6.1296,
        "capital": "Luxembourg City",
        "languages": ["Luxembourgish", "French", "German"],
        "currency": "Euro (€)",
        "population": "634,730",
        "time_zone": "GMT+1",
        "best_time_to_visit": "May to September"
    },
    "Germany": {
        "code": "DE", 
        "lat": 51.1657, 
        "lon": 10.4515,
        "capital": "Berlin",
        "languages": ["German"],
        "currency": "Euro (€)",
        "population": "83,240,000",
        "time_zone": "GMT+1",
        "best_time_to_visit": "May to September"
    },
    "France": {
        "code": "FR", 
        "lat": 46.6034, 
        "lon": 1.8883,
        "capital": "Paris",
        "languages": ["French"],
        "currency": "Euro (€)",
        "population": "67,390,000",
        "time_zone": "GMT+1",
        "best_time_to_visit": "April to October"
    },
    "Belgium": {
        "code": "BE", 
        "lat": 50.8503, 
        "lon": 4.3517,
        "capital": "Brussels",
        "languages": ["Dutch", "French", "German"],
        "currency": "Euro (€)",
        "population": "11,560,000",
        "time_zone": "GMT+1",
        "best_time_to_visit": "April to October"
    },
    "USA": {
        "code": "US", 
        "lat": 37.0902, 
        "lon": -95.7129,
        "capital": "Washington D.C.",
        "languages": ["English"],
        "currency": "US Dollar ($)",
        "population": "331,900,000",
        "time_zone": "Various (GMT-4 to GMT-10)",
        "best_time_to_visit": "Varies by region"
    },
    "Japan": {
        "code": "JP", 
        "lat": 36.2048, 
        "lon": 138.2529,
        "capital": "Tokyo",
        "languages": ["Japanese"],
        "currency": "Japanese Yen (¥)",
        "population": "125,800,000",
        "time_zone": "GMT+9",
        "best_time_to_visit": "March to May and October to November"
    },
    "Mexico": {
        "code": "MX", 
        "lat": 23.6345, 
        "lon": -102.5528,
        "capital": "Mexico City",
        "languages": ["Spanish"],
        "currency": "Mexican Peso ($)",
        "population": "128,900,000",
        "time_zone": "GMT-6",
        "best_time_to_visit": "December to April"
    },
    "Brazil": {
        "code": "BR", 
        "lat": -14.2350, 
        "lon": -51.9253,
        "capital": "Brasília",
        "languages": ["Portuguese"],
        "currency": "Brazilian Real (R$)",
        "population": "212,600,000",
        "time_zone": "GMT-3",
        "best_time_to_visit": "December to March"
    },
    "India": {
        "code": "IN", 
        "lat": 20.5937, 
        "lon": 78.9629,
        "capital": "New Delhi",
        "languages": ["Hindi", "English"],
        "currency": "Indian Rupee (₹)",
        "population": "1,380,000,000",
        "time_zone": "GMT+5:30",
        "best_time_to_visit": "October to March"
    },
    "South Korea": {
        "code": "KR", 
        "lat": 35.9078, 
        "lon": 127.7669,
        "capital": "Seoul",
        "languages": ["Korean"],
        "currency": "South Korean Won (₩)",
        "population": "51,780,000",
        "time_zone": "GMT+9",
        "best_time_to_visit": "March to May and September to November"
    },
    "UK": {
        "code": "GB", 
        "lat": 55.3781, 
        "lon": -3.4360,
        "capital": "London",
        "languages": ["English"],
        "currency": "Pound Sterling (£)",
        "population": "67,220,000",
        "time_zone": "GMT",
        "best_time_to_visit": "May to September"
    },
    "Argentina": {
        "code": "AR", 
        "lat": -38.4161, 
        "lon": -63.6167,
        "capital": "Buenos Aires",
        "languages": ["Spanish"],
        "currency": "Argentine Peso ($)",
        "population": "45,380,000",
        "time_zone": "GMT-3",
        "best_time_to_visit": "October to April"
    },
}

# Music preferences with descriptions
music_preferences = {
    "Pop": {
        "code": "pop",
        "description": "Chart-topping hits and catchy melodies",
        "icon": "🎵"
    },
    "Rock": {
        "code": "rock",
        "description": "Guitar-driven music with attitude",
        "icon": "🤘"
    },
    "Hip-Hop": {
        "code": "hip hop",
        "description": "Rhythmic beats and powerful lyrics",
        "icon": "🎤"
    },
    "Chill": {
        "code": "chill",
        "description": "Relaxing tunes to unwind and relax",
        "icon": "😌"
    },
    "Classical": {
        "code": "classical",
        "description": "Timeless orchestral and piano compositions",
        "icon": "🎻"
    },
    "Electronic": {
        "code": "electronic", 
        "description": "Synthesized sounds and digital beats",
        "icon": "🎧"
    },
    "Jazz": {
        "code": "jazz",
        "description": "Smooth improvisational melodies",
        "icon": "🎷"
    },
    "Folk": {
        "code": "folk",
        "description": "Traditional acoustic storytelling",
        "icon": "🪕"
    },
    "R&B": {
        "code": "r&b",
        "description": "Soulful rhythms and blues influences",
        "icon": "🎹"
    },
    "Indie": {
        "code": "indie",
        "description": "Independent artists with unique sounds",
        "icon": "🎸"
    },
}

# Travel tips for each country
travel_tips = {
    "Luxembourg": [
        "Public transport is free throughout the entire country",
        "Visit the Bock Casemates - underground tunnels dating from 1644",
        "Try 'Judd mat Gaardebounen' - a local specialty with smoked pork and beans",
        "The country is small enough to explore in just a few days"
    ],
    "Germany": [
        "The train system (Deutsche Bahn) is excellent for getting around",
        "Many museums are free on the first Sunday of each month",
        "Beer gardens are great places to meet locals and enjoy German culture",
        "Cash is preferred in many places; don't rely solely on cards"
    ],
    "France": [
        "Learn a few basic French phrases - locals appreciate the effort",
        "Many museums are free on the first Sunday of each month",
        "Don't rush meals - dining is a leisurely experience in France",
        "Paris Museum Pass can save money if visiting multiple attractions"
    ],
    "Belgium": [
        "Try different Belgian beers - there are more than 1,500 varieties",
        "Don't miss the waffles, fries, and chocolate",
        "Most people speak English, but learning some French or Dutch is appreciated",
        "The train system makes it easy to visit multiple cities"
    ],
    "USA": [
        "Tipping (15-20%) is expected for services like restaurants and taxis",
        "Distances between cities can be vast - plan travel accordingly",
        "Purchase travel insurance as healthcare can be expensive",
        "National Parks require entrance fees but offer annual passes"
    ],
    "Japan": [
        "Get a Japan Rail Pass if planning to travel between cities",
        "Removing shoes is customary when entering homes and some restaurants",
        "Carrying cash is important as many places don't accept cards",
        "Learn basic phrases and respect local customs"
    ],
    "Mexico": [
        "Drink bottled water and be cautious with street food (though it's delicious)",
        "Learn basic Spanish phrases to enhance your experience",
        "Siesta time (2-4 PM) is observed in smaller towns",
        "Bargaining is expected in markets"
    ],
    "Brazil": [
        "Learn some Portuguese basics - English isn't widely spoken",
        "Be vigilant about personal security, especially in major cities",
        "The currency is the Real (R$) - have some cash on hand",
        "Yellow fever vaccination is recommended for some regions"
    ],
    "India": [
        "Dress modestly, especially when visiting religious sites",
        "Try the street food but be cautious - stick to busy stalls",
        "Always drink bottled or filtered water",
        "Haggling is expected in markets"
    ],
    "South Korea": [
        "T-money card is useful for public transportation",
        "Free wifi is widely available in cities",
        "Remove shoes when entering homes and some restaurants",
        "Learn some basic Korean phrases - it's appreciated"
    ],
    "UK": [
        "Look right first when crossing roads - they drive on the left",
        "Museums in London are mostly free",
        "An Oyster card is essential for London transport",
        "Pubs close relatively early (around 11 PM)"
    ],
    "Argentina": [
        "The currency situation can be complex - research before arrival",
        "Dinner is typically eaten late (after 9 PM)",
        "Learn some basic Spanish phrases",
        "Tipping 10% is customary in restaurants"
    ],
}

# Functions
def get_top_songs(country_code, genre, limit=10):
    try:
        # Modified query to focus on top tracks from the country rather than just genre
        # First, try to get country-specific top hits
        country_top_hits = sp.search(q=f"tag:new", type="track", market=country_code, limit=limit)
        
        # If we got results, use those
        if country_top_hits and len(country_top_hits['tracks']['items']) > 0:
            results = country_top_hits
        else:
            # Fallback to genre if country-specific search doesn't yield results
            results = sp.search(q=f"genre:{genre}", type="track", market=country_code, limit=limit)
        
        top_songs = []
        for item in results['tracks']['items']:
            song_name = item['name']
            artist_name = item['artists'][0]['name']
            artist_id = item['artists'][0]['id']
            preview_url = item['preview_url']
            album_image = item['album']['images'][1]['url'] if item['album']['images'] else None
            song_url = item['external_urls']['spotify']
            song_popularity = item['popularity']
            release_date = item['album']['release_date'] if 'release_date' in item['album'] else 'Unknown'
            
            # Get additional artist info
            try:
                artist_info = sp.artist(artist_id)
                artist_genres = artist_info['genres'][:3] if 'genres' in artist_info and artist_info['genres'] else []
                artist_image = artist_info['images'][0]['url'] if 'images' in artist_info and artist_info['images'] else None
            except:
                artist_genres = []
                artist_image = None
            
            top_songs.append({
                "name": song_name,
                "artist": artist_name,
                "artist_image": artist_image,
                "artist_genres": artist_genres,
                "preview_url": preview_url,
                "image": album_image,
                "url": song_url,
                "popularity": song_popularity,
                "release_date": release_date
            })
        
        return top_songs
    except Exception as e:
        st.error(f"Error fetching songs: {e}")
        return []

def get_ai_country_facts(country):
    # Enhanced facts with more detail and style
    facts = {
        "Luxembourg": "Luxembourg is one of Europe's smallest countries, known for its medieval old town perched on dramatic cliffs. As a global financial center, it has the highest GDP per capita in the world. The country is trilingual, with Luxembourgish, French, and German all recognized as official languages. Its fairytale castles and picturesque valleys make it a hidden gem in Europe.",
        "Germany": "Germany is famous for its rich cultural heritage, engineering excellence, and Oktoberfest. It's Europe's largest economy and home to many influential philosophers, composers, and scientists. From the fairy-tale castles of Bavaria to Berlin's vibrant art scene, Germany offers diverse experiences. The country's Autobahn highways famously have no general speed limit in many sections.",
        "France": "France is renowned for its cuisine, fashion, art, and the iconic Eiffel Tower. It's one of the world's most popular tourist destinations, attracting visitors with its charming villages, alpine mountains, Mediterranean beaches, and world-class museums. French wine regions like Bordeaux, Burgundy, and Champagne are celebrated worldwide. The country has a rich literary and philosophical tradition that has significantly influenced Western culture.",
        "Belgium": "Belgium is famous for its chocolate, waffles, beer, and as the headquarters of the European Union. Brussels, its capital, is known as the 'Capital of Europe'. Despite its small size, Belgium has three official languages: Dutch, French, and German. The country has over 1,500 varieties of beer and is home to the world's first beer academy. Its medieval towns like Bruges appear frozen in time with their cobblestone streets and Gothic architecture.",
        "USA": "The United States is known for its cultural influence, entertainment industry in Hollywood, and technological innovation in Silicon Valley. As the world's third-largest country by area, it offers incredibly diverse landscapes from the Grand Canyon and Yellowstone to the beaches of Hawaii and the skyscrapers of New York City. American culture emphasizes freedom, individualism, and innovation, which has led to global contributions in science, technology, arts, and sports.",
        "Japan": "Japan is famous for its unique blend of traditional culture and cutting-edge technology. It's known for sushi, anime, cherry blossoms, and high-tech innovations. The Japanese concept of 'omotenashi' represents their unique approach to hospitality. Japan has the world's oldest monarchy and more than 1,500 earthquakes annually. Tokyo's Shibuya Crossing is the world's busiest pedestrian intersection, with up to 3,000 people crossing at once during peak times.",
        "Mexico": "Mexico has a rich cultural heritage, from ancient Mayan and Aztec ruins to vibrant music, dance, and cuisine that includes tacos and tequila. It's home to 35 UNESCO World Heritage sites, including Chichen Itza and the historic center of Mexico City. Mexican cuisine is so important culturally that it's recognized by UNESCO as an Intangible Cultural Heritage of Humanity. The country's Day of the Dead celebration has become internationally recognized for its colorful and meaningful traditions.",
        "Brazil": "Brazil is known for its Amazon rainforest, vibrant Carnival celebrations, football excellence, and beautiful beaches like Copacabana and Ipanema. It's the largest country in South America, covering nearly half the continent. The Amazon River flowing through Brazil discharges more water than the next seven largest rivers combined. Brazilian culture is a vibrant mix of Portuguese, African, indigenous, and various immigrant influences, creating unique music, dance, and cuisine.",
        "India": "India is famous for its diverse culture, colorful festivals, spicy cuisine, Bollywood films, and ancient monuments like the Taj Mahal. With over 1.3 billion people, it's the world's largest democracy and home to 22 officially recognized languages. Indian cuisine varies dramatically by region, reflecting the country's diverse geography and history. The country gave the world significant innovations including chess, the concept of zero, yoga, and Ayurvedic medicine.",
        "South Korea": "South Korea is known for K-pop music, Korean dramas, technological innovation, and a unique blend of ancient traditions and modern lifestyle. Seoul's sophisticated subway system is considered one of the world's best public transportation networks. Korean cuisine features kimchi, a fermented vegetable dish that has been recognized for its health benefits. The country has one of the world's fastest internet speeds and is a global leader in smartphone and semiconductor production.",
        "UK": "The United Kingdom is famous for its royal family, historic landmarks like Big Ben and Stonehenge, and cultural exports from Shakespeare to The Beatles. London's underground 'Tube' is the world's oldest underground railway network. The UK consists of four countries: England, Scotland, Wales, and Northern Ireland, each with distinct cultures and traditions. British literature, from Chaucer to J.K. Rowling, has shaped global literary traditions for centuries.",
        "Argentina": "Argentina is known for tango dancing, football stars like Messi, delicious steaks, and the beautiful landscapes of Patagonia. It's home to both the highest and lowest points in South America. Argentine beef is world-renowned, and the country has the highest consumption of red meat in the world. The southernmost city in the world, Ushuaia, is located in Argentina and is the gateway to Antarctica. The country has produced five Nobel Prize winners in the sciences, peace, and literature."
    }
    return facts.get(country, "No information available for this country.")

def get_language_flags(languages):
    flags = []
    for language in languages:
        if language == "English":
            flags.append("🇬🇧")
        elif language == "French":
            flags.append("🇫🇷")
        elif language == "German":
            flags.append("🇩🇪")
        elif language == "Dutch":
            flags.append("🇳🇱")
        elif language == "Spanish":
            flags.append("🇪🇸")
        elif language == "Portuguese":
            flags.append("🇵🇹")
        elif language == "Japanese":
            flags.append("🇯🇵")
        elif language == "Korean":
            flags.append("🇰🇷")
        elif language == "Hindi":
            flags.append("🇮🇳")
        elif language == "Luxembourgish":
            flags.append("🇱🇺")
        else:
            flags.append("🏳️")
    return " ".join(flags)

def format_time_difference(country):
    # Calculate time difference between user's local time and destination
    time_zones = {
        "GMT": 0,
        "GMT+1": 1,
        "GMT+5:30": 5.5,
        "GMT+9": 9,
        "GMT-3": -3,
        "GMT-6": -6,
    }
    
    # Simplified calculation (would need proper timezone handling in real app)
    country_tz = countries[country]["time_zone"]
    if "Various" in country_tz:
        return "Various time zones"
    
    base_tz = time_zones.get(country_tz.split(" ")[0], 0)
    now = datetime.datetime.now()
    country_time = now + datetime.timedelta(hours=base_tz)
    
    return f"Local time: approximately {country_time.strftime('%H:%M')}"

def get_accurate_phrases(language):
    """Return accurate and useful phrases in the given language"""
    phrases = {
        "Luxembourgish": [
            "Moien / Gudden Owend - Hello / Good evening",
            "Wann ech glift - Please",
            "Villmools Merci - Thank you very much",
            "Entschëlleg mech - Excuse me",
            "Schwätz du Englesch - Do you speak English?"
        ],
        "French": [
            "Bonjour / Bonsoir - Hello / Good evening",
            "S'il vous plaît - Please",
            "Merci beaucoup - Thank you very much",
            "Excusez-moi - Excuse me",
            "Parlez-vous anglais? - Do you speak English?"
        ],
        "German": [
            "Guten Tag / Guten Abend - Hello / Good evening",
            "Bitte - Please",
            "Danke schön - Thank you very much",
            "Entschuldigung - Excuse me",
            "Sprechen Sie Englisch? - Do you speak English?"
        ],
        "Spanish": [
            "Hola / Buenas noches - Hello / Good evening",
            "Por favor - Please",
            "Muchas gracias - Thank you very much",
            "Disculpe - Excuse me",
            "¿Habla inglés? - Do you speak English?"
        ],
        "Japanese": [
            "Konnichiwa / Konbanwa - Hello / Good evening",
            "Onegaishimasu - Please",
            "Arigatou gozaimasu - Thank you very much",
            "Sumimasen - Excuse me",
            "Eigo wo hanasemasu ka? - Do you speak English?"
        ],
        "Portuguese": [
            "Olá / Boa noite - Hello / Good evening",
            "Por favor - Please",
            "Muito obrigado/a - Thank you very much",
            "Com licença - Excuse me",
            "Fala inglês? - Do you speak English?"
        ],
        "English": [
            "Hello / Good evening",
            "Please",
            "Thank you very much", 
            "Excuse me",
            "Could you speak more slowly, please?"
        ],
        "Korean": [
            "Annyeonghaseyo / Annyeong haseyo - Hello / Good day",
            "Juseyo - Please",
            "Kamsahamnida - Thank you very much",
            "Shillye hamnida - Excuse me",
            "Yeongeo reul hasimnikka? - Do you speak English?"
        ],
        "Hindi": [
            "Namaste / Namaskar - Hello",
            "Kripaya - Please",
            "Dhanyavaad - Thank you very much",
            "Maaf kijiye - Excuse me",
            "Kya aap angrezi bolte hain? - Do you speak English?"
        ]
    }
    return phrases.get(language, phrases["English"])

def get_currency_code(currency_text):
    """Extract currency code from currency text"""
    currency_codes = {
        "Euro (€)": "EUR",
        "US Dollar ($)": "USD",
        "Pound Sterling (£)": "GBP",
        "Japanese Yen (¥)": "JPY",
        "Indian Rupee (₹)": "INR",
        "South Korean Won (₩)": "KRW",
        "Brazilian Real (R$)": "BRL",
        "Mexican Peso ($)": "MXN",
        "Argentine Peso ($)": "ARS"
    }
    return currency_codes.get(currency_text, "EUR")

def generate_travel_guide(country, language_skill, traveler_type, experience_type, food_importance):
    """Generate a personalized travel guide using OpenAI or fallback to pre-defined guides if API limit is reached"""
    try:
        # Create the prompt to send to OpenAI
        prompt = f"""
        I am traveling to {country}. I speak the local language: {language_skill}. 
        I am a {traveler_type}. I am looking for {experience_type} experiences.
        Food is {food_importance} to my experience. 
        
        Based on this, provide a concise travel guide for {country} with:
        - 5 useful phrases in the local language(s) of {country} (adapt based on whether I speak the language or not)
        - A brief manual of etiquette (cultural norms and tips for {country})
        - 5 things to do (activities, cultural spots, or attractions)
        - 3 accommodation options (that match my preferences as a {traveler_type})
        - 5 local food experiences (dishes, restaurants, markets, etc.)
        
        Format each section with clear headers and bullet points.
        """

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        # Extract and return the generated guide
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        # Fallback to pre-defined guides when API limit is reached
        st.warning(f"Using offline guide - OpenAI API limit reached: {str(e)}")
        
        # Get properly translated phrases
        primary_language = countries[country]["languages"][0]
        phrases = get_accurate_phrases(primary_language)
        
        # Generic accommodations by traveler type
        accommodations = {
            "Solo Explorer": [
                "Boutique hostels with private rooms",
                "Centrally located budget hotels",
                "Local guesthouses or B&Bs"
            ],
            "Family Adventurer": [
                "Family-friendly resorts with kids' activities",
                "Apartment rentals with multiple bedrooms",
                "All-inclusive hotels with pool facilities"
            ],
            "Business Professional": [
                "Luxury hotels with business centers",
                "Serviced apartments with good wifi",
                "Executive suites with concierge service"
            ],
            "Couple or Friends": [
                "Romantic boutique hotels",
                "Shared vacation rentals",
                "Cozy bed and breakfasts"
            ]
        }
        
        # Generic activities tailored to experience type
        activities_base = {
            "Adventure & Exploration": [
                f"Hiking in the natural areas around {country}",
                f"Adventure sports activities in {country}",
                "Taking guided tours to off-the-beaten-path locations",
                "Exploring natural wonders and geological formations",
                "Participating in outdoor adventure activities"
            ],
            "Relaxing & Scenic": [
                f"Visiting scenic viewpoints in {country}",
                "Relaxing at spa and wellness centers",
                "Taking leisurely walks through beautiful neighborhoods",
                "Enjoying picnics in local parks",
                "Taking scenic drives or train journeys"
            ],
            "Cultural Immersion": [
                f"Visiting the top museums and historical sites in {country}",
                "Taking cooking classes to learn local cuisine",
                "Participating in cultural festivals or events",
                "Visiting local markets and craft shops",
                "Taking guided cultural tours with local experts"
            ],
            "Luxury & Comfort": [
                f"Fine dining at renowned restaurants in {country}",
                "Shopping at luxury boutiques and designer shops",
                "Booking VIP experiences and exclusive tours",
                "Relaxing at premium spa and wellness centers",
                "Taking chauffeured tours of the highlights"
            ]
        }
        
        # Get specific activities for the country if available, otherwise use generic
        country_specific_activities = {
            "France": [
                "Visit the Louvre Museum in Paris to see the Mona Lisa",
                "Take a wine tasting tour in Bordeaux or Champagne",
                "Explore the historic châteaux of the Loire Valley",
                "Walk along the beautiful Promenade des Anglais in Nice",
                "Visit Mont Saint-Michel, the stunning island commune in Normandy"
            ],
            "Japan": [
                "Visit Senso-ji Temple and explore Asakusa in Tokyo",
                "Experience a traditional tea ceremony in Kyoto",
                "See the iconic Mount Fuji (best viewed from Hakone)",
                "Visit Hiroshima Peace Memorial Park and Museum",
                "Explore the historic temples and shrines in Nara"
            ],
            "Germany": [
                "Visit Neuschwanstein Castle, the inspiration for Disney's castle",
                "Explore Museum Island in Berlin",
                "Take a boat trip on the Rhine River to see medieval castles",
                "Visit the Black Forest and try authentic Black Forest cake",
                "Experience Oktoberfest in Munich (if visiting in September/October)"
            ],
            "Mexico": [
                "Explore the ancient Mayan ruins of Chichen Itza",
                "Visit Frida Kahlo's Blue House museum in Mexico City",
                "Experience the Day of the Dead celebrations (if visiting in November)",
                "Relax on the beaches of Tulum or Cancun",
                "Take a boat trip through the Sumidero Canyon"
            ],
            "Brazil": [
                "Visit Christ the Redeemer statue in Rio de Janeiro",
                "Experience the vibrant atmosphere of Copacabana Beach",
                "Explore the Amazon Rainforest with a guided tour",
                "Visit Iguazu Falls on the border with Argentina",
                "Experience the historic center of Salvador, with its colorful colonial architecture"
            ],
            "India": [
                "Visit the Taj Mahal in Agra",
                "Explore the Golden Temple in Amritsar",
                "Experience a boat ride on the Ganges River in Varanasi",
                "Visit Jaipur's Amber Fort and City Palace",
                "Explore the beaches and Portuguese architecture of Goa"
            ],
            "South Korea": [
                "Explore Gyeongbokgung Palace in Seoul",
                "Hike in Bukhansan National Park",
                "Visit the DMZ (Demilitarized Zone) on a guided tour",
                "Experience a traditional Korean bath house (jjimjilbang)",
                "Explore Jeju Island, known for its natural beauty"
            ]
        }
        
        activities = country_specific_activities.get(country, activities_base[experience_type])
        
        # Food recommendations based on country and importance
        food_experiences = {
            "France": [
                "Try authentic French croissants and pastries at a local boulangerie",
                "Experience a multi-course dinner at a traditional bistro",
                "Visit a local cheese shop and sample regional varieties",
                "Visit a French wine bar for wine tasting with charcuterie",
                "Browse and sample at a local farmers market"
            ],
            "Japan": [
                "Try authentic sushi at a traditional sushi restaurant",
                "Experience a kaiseki (multi-course) dinner",
                "Visit an izakaya (Japanese pub) for casual dining and drinks",
                "Try ramen at a specialized ramen shop",
                "Visit Tsukiji Outer Market for fresh seafood and street food"
            ],
            "Germany": [
                "Try authentic German sausages at a local Biergarten",
                "Experience traditional German dishes like Schnitzel and Sauerbraten",
                "Visit a German bakery for fresh pretzels and bread",
                "Try regional specialties like Currywurst in Berlin or Käsespätzle in Bavaria",
                "Visit a traditional German brewery"
            ],
            "Mexico": [
                "Try authentic street tacos from local vendors",
                "Experience mole dishes in Oaxaca or Puebla",
                "Visit a local market to try fresh tropical fruits",
                "Try traditional Mexican breakfast dishes like chilaquiles",
                "Experience authentic Mexican seafood dishes on the coast"
            ],
            "Brazil": [
                "Try churrasco (Brazilian barbecue) at a churrascaria",
                "Experience feijoada, Brazil's national dish, on a Wednesday or Saturday",
                "Try açaí bowls for breakfast or as a snack",
                "Visit a local market to try exotic Amazonian fruits",
                "Try pastels (fried pastries with fillings) at a feira (street market)"
            ],
            "India": [
                "Try a traditional thali with various dishes representing local cuisine",
                "Experience street food like chaat, pani puri, or vada pav",
                "Visit a local sweet shop for desserts like jalebi or gulab jamun",
                "Try regional specialties like masala dosa in South India or butter chicken in North India",
                "Visit a spice market for an authentic sensory experience"
            ],
            "South Korea": [
                "Try Korean BBQ where you grill meat at your table",
                "Experience traditional street food at markets like Gwangjang Market",
                "Try bibimbap, a colorful rice bowl with vegetables and meat",
                "Visit a traditional tea house for Korean teas and rice cakes",
                "Try Korean fried chicken with beer (chimaek)"
            ]
        }
        
        food_section = food_experiences.get(country, [
            f"Try the local specialties in {country}",
            "Visit local markets for fresh ingredients and street food",
            "Experience fine dining at renowned restaurants",
            "Take a cooking class to learn about local ingredients",
            "Join a food tour to sample multiple dishes"
        ])
        
        # Cultural etiquette tips by country
        etiquette = {
            "France": [
                "Always greet with 'Bonjour' before starting a conversation",
                "Maintain eye contact during conversations",
                "Keep hands on the table, not in your lap, during meals",
                "Punctuality is appreciated but not strictly expected",
                "Dress well - casual but neat attire is appropriate for most situations"
            ],
            "Japan": [
                "Bow when greeting people - the deeper the bow, the more respect shown",
                "Remove shoes before entering homes and certain restaurants",
                "Don't tip - it's not customary and can be considered rude",
                "Avoid eating while walking on the street",
                "Be quiet on public transportation"
            ],
            "Germany": [
                "Punctuality is extremely important - arrive on time or slightly early",
                "Maintain direct eye contact during conversations",
                "Wait for the host to say 'Guten Appetit' before eating",
                "Always keep your hands visible during meals (not in your lap)",
                "Recycling and environmental consciousness are taken seriously"
            ],
            "Mexico": [
                "Greetings are important - handshakes and sometimes kisses on the cheek",
                "Be patient with a more relaxed sense of time (especially outside business settings)",
                "Don't discuss sensitive political topics",
                "Dress conservatively when visiting religious sites",
                "Personal space is smaller than in some Western countries"
            ],
            "Brazil": [
                "Brazilians are tactile - expect kisses on the cheek and frequent touching",
                "Be patient with a more relaxed sense of time",
                "The 'OK' hand gesture is considered offensive",
                "Dress casually but neatly - appearance is important",
                "Don't refuse food or drink when offered - it's considered impolite"
            ],
            "India": [
                "Greet with 'Namaste' with hands pressed together",
                "Use your right hand for eating and giving/receiving objects",
                "Remove shoes before entering temples and homes",
                "Dress modestly, especially at religious sites",
                "Ask permission before taking photos of people"
            ],
            "South Korea": [
                "Bow when greeting, especially to older people",
                "Use both hands when giving or receiving items",
                "Remove shoes when entering homes",
                "The eldest person should be served first at meals",
                "Don't write names in red ink - it symbolizes death"
            ],
            "UK": [
                "Queueing (lining up) is taken very seriously - never cut in line",
                "Maintain an 'arm's length' of personal space",
                "Punctuality is important",
                "Avoid loud conversations in public places",
                "Saying 'please' and 'thank you' is extremely important"
            ]
        }
        
        country_etiquette = etiquette.get(country, [
            "Greet people appropriately according to local customs",
            "Respect personal space and local communication styles",
            "Dress appropriately for the occasion and location",
            "Learn basic phrases in the local language",
            "Be aware of local dining etiquette"
        ])
        
        # Build formatted guide
        guide = f"""
# 📖 Personalized Travel Guide for {country}
*Based on your preferences as a {traveler_type} looking for {experience_type} experiences*

## 🗣️ Useful Phrases in {primary_language}

"""
        for phrase in phrases:
            guide += f"* {phrase}\n"
        
        guide += f"""
## 🤝 Cultural Etiquette in {country}

"""
        for tip in country_etiquette:
            guide += f"* {tip}\n"
        
        guide += f"""
## 🏆 Top 5 Things to Do in {country}

"""
        for activity in activities:
            guide += f"* {activity}\n"
        
        guide += f"""
## 🏨 Accommodation Recommendations for {traveler_type}s

"""
        for accommodation in accommodations[traveler_type]:
            guide += f"* {accommodation}\n"
        
        guide += f"""
## 🍽️ Food Experiences in {country}

"""
        for food in food_section:
            guide += f"* {food}\n"
        
        guide += f"""
---
*Note: This guide was generated offline. For more detailed information, please check online travel resources.*
"""
        
        return guide

# Banner image or header with Luxair-styled navbar
st.markdown("""
<div class="luxair-navbar">
    <div class="luxair-logo">✈️ TravelTunes</div>
    <div class="nav-links">
        <a href="#" class="nav-item">Book</a>
        <a href="#" class="nav-item">Destinations</a>
        <a href="#" class="nav-item">Services</a>
        <a href="#" class="nav-item">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Your Travel Companion</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.1rem; margin-bottom: 30px;'>Discover destinations with curated music and personalized travel guides</p>", unsafe_allow_html=True)

# Add a branded watermark for Daphne & OR
st.markdown("""
<div style="position: absolute; top: 10px; right: 10px; background: var(--primary); padding: 5px 10px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <span style="color: white; font-weight: bold; font-size: 0.8rem;">Daphne & OR</span>
</div>
""", unsafe_allow_html=True)

# Add interactive progress bar - removing the snowflakes animation that user didn't like
progress_bar = st.progress(0)
for percent_complete in range(100):
    progress_bar.progress(percent_complete + 1)
progress_bar.empty()  # Clear the progress bar after completion

# Create layout with columns
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Plan Your Journey</h2>", unsafe_allow_html=True)
    
    # Country selection with flags - styled like an airline booking form
    st.markdown("<div class='form-header'>Select Your Destination</div>", unsafe_allow_html=True)
    selected_country = st.selectbox(
        "Where would you like to go?",
        list(countries.keys()),
        index=None,
        placeholder="Choose a country..."
    )
    
    # Music preference selection with icons
    if selected_country:
        st.markdown("<div class='form-header'>Travel Preferences</div>", unsafe_allow_html=True)
        music_preference = st.selectbox(
            "What kind of music do you enjoy?",
            options=list(music_preferences.keys()),
            format_func=lambda x: f"{music_preferences[x]['icon']} {x}",
            index=None,
            placeholder="Select your music taste..."
        )
        
        # Travel date with calendar picker
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            travel_date = st.date_input("Departure date", datetime.datetime.now() + datetime.timedelta(days=30))
        with col_date2:
            return_date = st.date_input("Return date", datetime.datetime.now() + datetime.timedelta(days=37))
        
        days_until_trip = (travel_date - datetime.datetime.now().date()).days
        if days_until_trip > 0:
            st.info(f"🗓️ Your trip is in {days_until_trip} days!")
        
        # Flight details
        flight_number = st.text_input("Luxair flight number (optional)", placeholder="LG1234")
        
        # Travel guide options - collapsible section
        with st.expander("Customize Your Trip"):
            language_skill = st.radio("Do you speak the local language?", 
                                ["Yes, fluently", "Yes, a little", "No, not at all"])
            
            traveler_type = st.radio("What kind of traveler are you?", 
                                ["Solo Explorer", "Family Adventurer", "Business Professional", "Couple or Friends"])
            
            experience_type = st.radio("What kind of experiences are you looking for?", 
                                ["Adventure & Exploration", "Relaxing & Scenic", "Cultural Immersion", "Luxury & Comfort"])
            
            food_importance = st.radio("How important is food to your travel experience?", 
                                ["Very Important", "Somewhat Important", "Not Important"])
            
            # Add a budget slider
            budget_level = st.slider("What's your budget level?", 1, 5, 3, 
                                    help="1 = Budget traveler, 5 = Luxury traveler")
            budget_labels = {1: "Budget", 2: "Economy", 3: "Mid-range", 4: "Premium", 5: "Luxury"}
            st.write(f"Selected budget: {budget_labels[budget_level]} 💰" + "💰" * (budget_level-1))
        
        # Search button styled like a flight booking button
        if st.button("Generate My Trip Plan", type="primary"):
            if not music_preference:
                st.warning("Please select a music preference")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Recommendations based on viewing history - styled like featured destinations
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Featured Destinations</h2>", unsafe_allow_html=True)
    
    # Sample recommended destinations with interactive elements
    for dest in ["France", "Japan", "Germany"]:
        if dest != selected_country:
            st.markdown(f"""
            <div style="padding: 15px; margin-bottom: 15px; background: linear-gradient(90deg, white 0%, var(--light-bg) 100%); 
                        border-radius: 8px; cursor: pointer; transition: transform 0.3s ease, box-shadow 0.3s ease; border-left: 3px solid var(--secondary);"
                 onmouseover="this.style.transform='scale(1.02)';this.style.boxShadow='0 8px 15px rgba(0,0,0,0.08)';" 
                 onmouseout="this.style.transform='scale(1)';this.style.boxShadow='none';">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 1.1rem; font-weight: 500; color: var(--primary);">{dest}</span>
                    <span>{get_language_flags(countries[dest]['languages'])}</span>
                </div>
                <div style="margin-top: 8px; font-size: 0.9rem; color: var(--light-text);">
                    🏛️ {countries[dest]['capital']}
                </div>
                <div style="margin-top: 5px; font-size: 0.8rem; color: var(--accent1); font-weight: 500;">
                    FROM €299
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
with col2:
    if selected_country:
        # Create tabs for different content sections
        tab1, tab2, tab3 = st.tabs(["📍 Destination", "🎵 Music", "📒 Travel Guide"])
        
        with tab1:
            # Country information card with enhanced styling
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            # Country title with flag
            country_flag_emoji = get_language_flags(countries[selected_country]['languages']).split()[0]
            st.markdown(f"<h2 class='sub-header'>{country_flag_emoji} {selected_country}</h2>", unsafe_allow_html=True)
            
            # Country stats in a nice layout
            st.markdown("<div class='stat-container'>", unsafe_allow_html=True)
            
            # Population stat
            st.markdown(f"""
            <div class='stat-item'>
                <div class='stat-value'>👥 {countries[selected_country]['population']}</div>
                <div class='stat-label'>Population</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Capital stat
            st.markdown(f"""
            <div class='stat-item'>
                <div class='stat-value'>🏛️ {countries[selected_country]['capital']}</div>
                <div class='stat-label'>Capital</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Currency stat
            st.markdown(f"""
            <div class='stat-item'>
                <div class='stat-value'>💱 {countries[selected_country]['currency']}</div>
                <div class='stat-label'>Currency</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Map showing the selected country with customized appearance
            st.markdown("<p style='margin: 25px 0 15px 0; font-weight: 600; color: var(--primary);'>📍 Location</p>", unsafe_allow_html=True)
            map_data = pd.DataFrame({
                'latitude': [countries[selected_country]['lat']],
                'longitude': [countries[selected_country]['lon']]
            })
            st.map(map_data, zoom=4)
            
            # Country details in a more structured layout
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                # Languages with flags
                languages = countries[selected_country]['languages']
                language_flags = get_language_flags(languages)
                st.markdown(f"<p><strong>🗣️ Languages:</strong> {', '.join(languages)}</p>", unsafe_allow_html=True)
                
                # Time zone information with clock icon
                st.markdown(f"<p><strong>🕒 Time Zone:</strong> {countries[selected_country]['time_zone']}</p>", unsafe_allow_html=True)
            
            with col_info2:
                # Best time to visit with calendar icon
                st.markdown(f"<p><strong>📅 Best Time to Visit:</strong> {countries[selected_country]['best_time_to_visit']}</p>", unsafe_allow_html=True)
                
                # Visa information (simplified)
                visa_info = {
                    "USA": "Tourist visa (ESTA) required for most visitors",
                    "Japan": "Tourist visa required for many countries, visa waiver for others",
                    "UK": "Standard Visitor visa required for many countries",
                    "France": "Schengen visa for non-EU visitors",
                    "Germany": "Schengen visa for non-EU visitors",
                    "Mexico": "Tourist Card (FMM) required",
                    "Brazil": "Tourist visa required for some countries",
                    "India": "e-Visa available for most tourists",
                    "South Korea": "Visa-free for many countries for up to 90 days",
                    "Argentina": "Visa-free for many tourists for up to 90 days",
                    "Luxembourg": "Schengen visa for non-EU visitors",
                    "Belgium": "Schengen visa for non-EU visitors"
                }
                
                visa_text = visa_info.get(selected_country, "Please check visa requirements before traveling")
                st.markdown(f"<p><strong>🛂 Visa:</strong> {visa_text}</p>", unsafe_allow_html=True)
            
            # Currency exchange calculator (improved version)
            st.markdown("<div style='background-color: var(--light-bg); padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 3px solid var(--primary);'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 1.1rem; margin-bottom: 10px; color: var(--primary);'>💱 Currency Converter</h3>", unsafe_allow_html=True)
            
            currency_name = countries[selected_country]['currency']
            currency_code = get_currency_code(currency_name)
            
            exchange_rates = {
                "EUR": 1.0,
                "USD": 1.08,
                "GBP": 0.85,
                "JPY": 162.5,
                "INR": 90.3,
                "KRW": 1470.0,
                "BRL": 5.5,
                "MXN": 18.2,
                "ARS": 945.0
            }
            
            amount = st.number_input("Amount (EUR)", value=100.0, step=10.0)
            
            if currency_code in exchange_rates:
                converted = amount * exchange_rates[currency_code]
                
                # Get the currency symbol from the name
                currency_symbol = "€"
                if "$" in currency_name:
                    currency_symbol = "$"
                elif "£" in currency_name:
                    currency_symbol = "£"
                elif "¥" in currency_name:
                    currency_symbol = "¥"
                elif "₹" in currency_name:
                    currency_symbol = "₹"
                elif "₩" in currency_name:
                    currency_symbol = "₩"
                elif "R$" in currency_name:
                    currency_symbol = "R$"
                
                st.metric("Value", f"{currency_symbol} {converted:.2f}")
                
                # Show the exchange rate
                st.write(f"Exchange rate: 1 EUR = {exchange_rates[currency_code]} {currency_code}")
            else:
                st.metric("Value", f"{currency_name} (rate unavailable)")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # AI-generated country facts
            country_facts = get_ai_country_facts(selected_country)
            st.markdown("<div class='country-info'>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight: 600; color: var(--primary); margin-bottom: 10px;'>About {selected_country}</p>", unsafe_allow_html=True)
            st.markdown(f"{country_facts}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Travel tips section with improved styling
            st.markdown("<div class='travel-tips'>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight: 600; color: var(--primary); margin-bottom: 10px;'>Luxair Travel Tips for {selected_country}</p>", unsafe_allow_html=True)
            for tip in travel_tips[selected_country]:
                st.markdown(f"<div style='display: flex; align-items: flex-start; margin-bottom: 8px;'><div style='margin-right: 10px; color: var(--secondary);'>•</div><div>{tip}</div></div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            # Music recommendations section with enhanced layout
            if music_preference:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<h2 class='sub-header'>{music_preferences[music_preference]['icon']} {selected_country} Playlist</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: var(--light-text); margin-bottom: 20px;'>Top local hits to enjoy during your trip</p>", unsafe_allow_html=True)
                
                country_code = countries[selected_country]['code']
                genre_code = music_preferences[music_preference]['code']
                
                with st.spinner(f"Creating your {selected_country} playlist..."):
                    songs = get_top_songs(country_code, genre_code)
                
                if songs:
                    # Sort songs by popularity for better recommendations
                    songs.sort(key=lambda x: x['popularity'], reverse=True)
                    
                    # Add a filter option in a more styled way
                    st.markdown("<div style='background: var(--light-bg); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>", unsafe_allow_html=True)
                    filter_col1, filter_col2 = st.columns(2)
                    with filter_col1:
                        sort_by = st.selectbox("Sort by:", ["Popularity", "Release Date"])
                    with filter_col2:
                        min_popularity = st.slider("Minimum popularity:", 0, 100, 30)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Apply filters
                    if sort_by == "Release Date":
                        # Sort by release date (newest first)
                        songs.sort(key=lambda x: x['release_date'] if x['release_date'] != 'Unknown' else '1900-01-01', reverse=True)
                    
                    # Filter by popularity
                    songs = [song for song in songs if song['popularity'] >= min_popularity]
                    
                    if songs:
                        # Display songs in a grid with enhanced styling
                        for i, song in enumerate(songs):
                            st.markdown(f"""
                            <div style="padding: 15px; background: white; border-radius: 8px; margin-bottom: 15px; 
                                        box-shadow: 0 2px 4px rgba(0,0,0,0.05); border-left: 3px solid var(--secondary);">
                                <div style="display: flex; align-items: center;">
                                    <div style="flex: 0 0 50px; text-align: center;">
                                        <span style="font-size: 1.2rem; font-weight: 600; color: var(--accent2);">#{i+1}</span>
                                    </div>
                                    <div style="flex: 1;">
                                        <div style="font-weight: 600; color: var(--primary); font-size: 1.1rem;">{song['name']}</div>
                                        <div style="color: var(--accent2); margin-bottom: 5px;">{song['artist']}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Additional song details
                            if song["image"]:
                                with st.container():
                                    song_detail1, song_detail2 = st.columns([1, 4])
                                    with song_detail1:
                                        st.image(song["image"], width=100)
                                    with song_detail2:
                                        # Popularity meter
                                        pop = song["popularity"]
                                        pop_color = "var(--secondary)" if pop > 70 else "var(--primary)" if pop > 50 else "var(--accent1)"
                                        st.markdown(f"""
                                        <div style='margin: 5px 0;'>
                                            <div style='display:flex;align-items:center;'>
                                                <div style='width:80px;font-size:0.8rem;'>Popularity:</div>
                                                <div style='flex-grow:1;background:#eee;height:6px;border-radius:3px;'>
                                                    <div style='width:{pop}%;background:{pop_color};height:6px;border-radius:3px;'></div>
                                                </div>
                                                <div style='width:40px;text-align:right;font-size:0.8rem;'>{pop}%</div>
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        # Release date
                                        if song["release_date"] and song["release_date"] != "Unknown":
                                            st.markdown(f"<span style='font-size:0.8rem;color:var(--light-text);'>Released: {song['release_date']}</span>", unsafe_allow_html=True)
                            
                            # Audio player
                            if song["preview_url"]:
                                st.audio(song["preview_url"])
                            else:
                                st.info("No audio preview available for this track")
                            
                            # Spotify link - without nesting columns
                            st.markdown(f"<a href='{song['url']}' target='_blank' style='text-decoration: none;'><div style='background: var(--primary); color: white; padding: 8px 15px; border-radius: 4px; text-align: center; display: inline-block; margin-top: 10px;'>Listen on Spotify</div></a>", unsafe_allow_html=True)
                            
                            st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.warning("No songs match your filter criteria. Try adjusting the filters.")
                else:
                    st.warning("No songs found for this country. Try a different music preference or country.")
                
                # Flight playlist info with enhanced styling
                if 'flight_number' in locals() and flight_number:
                    st.markdown(f"""
                    <div style='background: var(--light-bg); padding: 20px; border-radius: 8px; margin-top: 30px; border-left: 3px solid var(--primary);'>
                        <p style='font-weight: 600; color: var(--primary); margin-bottom: 10px;'>✈️ Luxair Flight {flight_number}</p>
                        <p style='margin-bottom: 15px;'>Your personalized playlist will be available on your flight's entertainment system.</p>
                        <a href='#' style='text-decoration:none;'>
                            <div style='display:inline-block;background:var(--primary);color:white;padding:8px 15px;border-radius:4px;'>
                                <span style='margin-right:5px;'>📥</span> Download Playlist
                            </div>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Please select your music preferences to get a personalized playlist for your trip.")
        
        with tab3:
            # Personalized Travel Guide section
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 class='sub-header'>📖 {selected_country} Travel Guide</h2>", unsafe_allow_html=True)
            
            # Check if all preferences are selected
            all_preferences_selected = (
                'language_skill' in locals() and 
                'traveler_type' in locals() and 
                'experience_type' in locals() and 
                'food_importance' in locals()
            )
            
            if all_preferences_selected:
                with st.spinner(f"Creating your personalized {selected_country} guide..."):
                    travel_guide = generate_travel_guide(
                        selected_country, 
                        language_skill, 
                        traveler_type, 
                        experience_type, 
                        food_importance
                    )
                    
                    # Display the guide with enhanced styling - more like a travel brochure
                    st.markdown(f"""
                    <div style="background: white; border-radius: 8px; padding: 25px; border-top: 3px solid var(--secondary);">
                        {travel_guide}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Interactive sharing options
                    st.markdown("<div style='display: flex; gap: 10px; margin-top: 20px;'>", unsafe_allow_html=True)
                    
                    # Email button
                    st.markdown("""
                    <a href='#' style='text-decoration:none; flex: 1;'>
                        <div style='background:var(--light-bg);padding:10px;border-radius:4px;text-align:center;'>
                            <span style='margin-right:5px;'>📧</span> Email Guide
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
                    
                    # Save to phone button
                    st.markdown("""
                    <a href='#' style='text-decoration:none; flex: 1;'>
                        <div style='background:var(--light-bg);padding:10px;border-radius:4px;text-align:center;'>
                            <span style='margin-right:5px;'>📱</span> Save to Phone
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
                    
                    # Download button
                    st.markdown("""
                    <a href='#' style='text-decoration:none; flex: 1;'>
                        <div style='background:var(--primary);color:white;padding:10px;border-radius:4px;text-align:center;'>
                            <span style='margin-right:5px;'>📥</span> Download PDF
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Actually include the download functionality with streamlit
                    st.download_button(
                        label="",  # Hidden label since we have the HTML button above
                        data=travel_guide,
                        file_name=f"{selected_country}_Travel_Guide.txt",
                        mime="text/plain",
                        key="download_guide",
                        help="Download your personalized travel guide"
                    )
            else:
                st.info("Complete your travel preferences and click 'Generate My Trip Plan' to create your personalized guide.")
            
            # st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Show a welcome message when no country is selected
        st.markdown("""
        <div class="card" style="text-align: center; padding: 40px 20px;">
            <img src="https://www.luxair.lu/sites/default/files/styles/luxair_list_top_image_article/public/media/image/2021/hero_1920_1080_4.jpg?itok=hcB7W6pC" style="max-width: 100%; border-radius: 8px; margin-bottom: 20px;">
            <h2 style="color: var(--primary); margin-bottom: 15px;">Welcome to TravelTunes</h2>
            <p style="margin-bottom: 25px; font-size: 1.1rem;">Select a destination to begin planning your perfect trip with music that matches your journey.</p>
            <div style="padding: 10px; background: var(--light-bg); border-radius: 8px; font-style: italic; color: var(--accent2);">
                "Music is the soundtrack of your life" - Dick Clark
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer with Luxair-style links and improved styling
st.markdown("""
<div style="background: var(--primary); color: white; padding: 30px 20px; border-radius: 8px; margin-top: 40px;">
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; margin-bottom: 20px;">
        <div style="flex: 1; min-width: 200px; margin-bottom: 15px;">
            <h3 style="font-size: 1.2rem; margin-bottom: 15px;">About TravelTunes</h3>
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li style="margin-bottom: 8px;"><a href="#" style="color: white; text-decoration: none;">About Us</a></li>
                <li style="margin-bottom: 8px;"><a href="#" style="color: white; text-decoration: none;">Careers</a></li>
                <li style="margin-bottom: 8px;"><a href="#" style="color: white; text-decoration: none;">Press</a></li>
            </ul>
        </div>
        <div style="flex: 1; min-width: 200px; margin-bottom: 15px;">
            <h3 style="font-size: 1.2rem; margin-bottom: 15px;">Help</h3>
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li style="margin-bottom: 8px;"><a href="#" style="color: white; text-decoration: none;">Contact Us</a></li>
                <li style="margin-bottom: 8px;"><a href="#" style="color: white; text-decoration: none;">FAQs</a></li>
                <li style="margin-bottom: 8px;"><a href="#" style="color: white; text-decoration: none;">Terms & Conditions</a></li>
            </ul>
        </div>
        <div style="flex: 1; min-width: 200px; margin-bottom: 15px;">
            <h3 style="font-size: 1.2rem; margin-bottom: 15px;">Follow Us</h3>
            <div style="display: flex; gap: 15px;">
                <a href="#" style="color: white; font-size: 1.5rem;">📱</a>
                <a href="#" style="color: white; font-size: 1.5rem;">📷</a>
                <a href="#" style="color: white; font-size: 1.5rem;">📨</a>
            </div>
        </div>
    </div>
    <div style="text-align: center; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.2);">
        TravelTunes • Created by Daphne & OR • © 2025 All Rights Reserved
    </div>
</div>
""", unsafe_allow_html=True)
