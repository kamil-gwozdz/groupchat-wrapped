"""Statistics analyzer for Group Chat Wrapped."""

from collections import Counter, defaultdict
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Any
import re

from .parser import Conversation, Message


# Polish stopwords (conjunctions, prepositions, etc.)
POLISH_STOPWORDS = {
    'i', 'a', 'o', 'w', 'z', 'do', 'na', 'to', 'że', 'nie', 'się', 'co', 'jak',
    'ale', 'po', 'tak', 'za', 'od', 'czy', 'już', 'tylko', 'przez', 'jest',
    'są', 'być', 'było', 'będzie', 'ten', 'ta', 'te', 'ty', 'ja', 'on', 'ona',
    'my', 'wy', 'oni', 'one', 'tego', 'tej', 'tym', 'tych', 'tu', 'tam', 'też',
    'może', 'jeszcze', 'kiedy', 'gdzie', 'bo', 'no', 'dla', 'przy', 'jako',
    'sobie', 'który', 'która', 'które', 'którzy', 'mnie', 'ciebie', 'jego',
    'jej', 'ich', 'nas', 'was', 'mi', 'ci', 'mu', 'jej', 'im', 'nam', 'wam',
    'ze', 'we', 'ku', 'nad', 'pod', 'przed', 'między', 'bez', 'u', 'oraz',
    'albo', 'lub', 'więc', 'jednak', 'gdyż', 'ponieważ', 'jeśli', 'jeżeli',
    'gdy', 'ani', 'ni', 'choć', 'chociaż', 'aby', 'żeby', 'by', 'czyli',
    'ok', 'xd', 'xdd', 'xddd', 'haha', 'hehe', 'hihi', 'lol', 'kurwa', 'ja',
    'sie', 'ze', 'juz', 'cos', 'np', 'itd', 'itp', 'etc', 'btw', 'imo',
    'teraz', 'dzisiaj', 'jutro', 'wczoraj', 'rano', 'wieczorem', 'potem',
    'właśnie', 'dobra', 'dobrze', 'dzięki', 'super', 'fajnie', 'okej', 'oki',
    'serio', 'naprawdę', 'chyba', 'raczej', 'bardzo', 'trochę', 'dużo', 'mało',
    'nic', 'coś', 'ktoś', 'nikt', 'wszystko', 'każdy', 'żaden', 'sam', 'sama',
    'cały', 'cała', 'całe', 'inny', 'inna', 'inne', 'taki', 'taka', 'takie',
    'jakiś', 'jakaś', 'jakieś', 'jeden', 'jedna', 'jedno', 'dwa', 'trzy',
    'mój', 'moja', 'moje', 'twój', 'twoja', 'twoje', 'nasz', 'nasza', 'nasze',
    'wasz', 'wasza', 'wasze', 'tam', 'tutaj', 'stąd', 'stamtąd', 'dokąd',
}

ENGLISH_STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
    'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we',
    'they', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why',
    'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
    'too', 'very', 'just', 'also', 'now', 'here', 'there', 'then', 'once',
    'if', 'because', 'as', 'until', 'while', 'although', 'though', 'after',
    'before', 'when', 'where', 'why', 'how', 'again', 'further', 'then',
    'about', 'above', 'below', 'between', 'into', 'through', 'during',
    'out', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'me',
    'my', 'myself', 'your', 'yourself', 'his', 'him', 'himself', 'her',
    'herself', 'its', 'itself', 'our', 'ourselves', 'their', 'them',
    'themselves', 'am', 'up', 'down', 'yes', 'yeah', 'yea', 'nope', 'nah',
    'oh', 'ok', 'okay', 'like', 'lol', 'lmao', 'haha', 'hehe', 'omg', 'wtf',
}

STOPWORDS = POLISH_STOPWORDS | ENGLISH_STOPWORDS


@dataclass
class CategoryResult:
    """Result for a single category/slide."""
    category_id: str
    title: str
    subtitle: str
    icon: str
    winner: str | None = None
    winners: list[tuple[str, Any]] | None = None  # For top 5 categories
    value: Any = None
    extra_info: str | None = None
    fun_fact: str | None = None


@dataclass
class AnalysisResult:
    """Complete analysis result for the conversation."""
    conversation_title: str
    total_messages: int
    total_participants: int
    date_range: tuple[datetime, datetime]
    categories: list[CategoryResult] = field(default_factory=list)


def is_night_hour(hour: int) -> bool:
    """Check if hour is considered night time (0-5)."""
    return 0 <= hour <= 5


def get_words(text: str) -> list[str]:
    """Extract words from text, filtering stopwords."""
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Extract words
    words = re.findall(r'\b[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]{3,}\b', text.lower())
    return [w for w in words if w not in STOPWORDS]


# Polish noun suffixes (common endings)
POLISH_NOUN_SUFFIXES = (
    # Abstract nouns
    'ość', 'ość', 'anie', 'enie', 'cie', 'stwo', 'ctwo',
    # Person nouns
    'nik', 'arz', 'acz', 'ista', 'owiec', 'anin', 'ak',
    # Feminine nouns  
    'ka', 'arka', 'ica', 'ość', 'izna', 'yna',
    # Diminutives
    'ek', 'ko', 'eczko', 'ątko',
    # Other common
    'acja', 'cja', 'sja', 'zja', 'ura', 'ment', 'ent',
)

# Common Polish nouns (whitelist of frequently used nouns)
COMMON_POLISH_NOUNS = {
    # Places
    'dom', 'miasto', 'miejsce', 'ulica', 'sklep', 'szkoła', 'praca', 'biuro', 'pokój',
    'kuchnia', 'łazienka', 'ogród', 'park', 'las', 'góry', 'morze', 'plaża', 'rzeka',
    # People
    'człowiek', 'ludzie', 'koleżanka', 'kolega', 'przyjaciel', 'znajomy', 'rodzina',
    'mama', 'tata', 'brat', 'siostra', 'dziecko', 'dzieci', 'facet', 'gość', 'babka',
    'dziewczyna', 'chłopak', 'kobieta', 'mężczyzna', 'osoba', 'typ', 'ziomek', 'bro',
    # Things
    'rzecz', 'telefon', 'komputer', 'samochód', 'auto', 'rower', 'pociąg', 'autobus',
    'piwo', 'wino', 'wódka', 'kawa', 'herbata', 'jedzenie', 'obiad', 'śniadanie',
    'kolacja', 'pizza', 'kebab', 'burger', 'pieniądze', 'kasa', 'hajs', 'forsa',
    # Abstract
    'czas', 'dzień', 'noc', 'tydzień', 'miesiąc', 'rok', 'godzina', 'minuta',
    'problem', 'pytanie', 'odpowiedź', 'pomysł', 'plan', 'sprawa', 'temat', 'rzecz',
    'życie', 'praca', 'zabawa', 'impreza', 'imba', 'party', 'mecz', 'film', 'serial',
    'gra', 'muzyka', 'piosenka', 'historia', 'wiadomość', 'info', 'news',
    # Tech/internet
    'link', 'zdjęcie', 'foto', 'pic', 'meme', 'mem', 'gif', 'video', 'filmik',
    'post', 'komentarz', 'lajk', 'reakcja', 'wiadomość', 'czat', 'grupa',
    # Emotions/states
    'miłość', 'radość', 'smutek', 'strach', 'stres', 'spokój', 'energia',
    # Weather
    'pogoda', 'deszcz', 'słońce', 'śnieg', 'wiatr',
    # Body
    'głowa', 'ręka', 'noga', 'oko', 'twarz', 'serce', 'dupa',
    # Polish slang nouns
    'spoko', 'git', 'luzik', 'nara', 'hajs', 'sztos', 'bajka', 'akcja',
}


def is_polish_noun(word: str) -> bool:
    """Check if a word is likely a Polish noun using heuristics."""
    word_lower = word.lower()
    
    # Check whitelist first
    if word_lower in COMMON_POLISH_NOUNS:
        return True
    
    # Check common noun suffixes
    for suffix in POLISH_NOUN_SUFFIXES:
        if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 1:
            return True
    
    return False


def get_nouns(text: str) -> list[str]:
    """Extract nouns from text using heuristics."""
    words = get_words(text)
    return [w for w in words if is_polish_noun(w)]


def calculate_streak(messages: list[Message], sender: str) -> int:
    """Calculate the longest streak of consecutive messages by sender."""
    max_streak = 0
    current_streak = 0
    
    for msg in messages:
        if msg.sender == sender:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    
    return max_streak


def find_longest_absence(messages: list[Message], sender: str) -> tuple[int, datetime | None]:
    """Find the longest period of inactivity for a sender (in days)."""
    sender_messages = [m for m in messages if m.sender == sender]
    
    if len(sender_messages) < 2:
        return 0, None
    
    max_gap = timedelta(0)
    return_date = None
    
    for i in range(1, len(sender_messages)):
        gap = sender_messages[i].timestamp - sender_messages[i-1].timestamp
        if gap > max_gap:
            max_gap = gap
            return_date = sender_messages[i].timestamp
    
    return max_gap.days, return_date


def is_conversation_starter(messages: list[Message], idx: int, gap_hours: int = 4) -> bool:
    """Check if message at idx starts a new conversation (after gap)."""
    if idx == 0:
        return True
    
    time_diff = messages[idx].timestamp - messages[idx-1].timestamp
    return time_diff > timedelta(hours=gap_hours)


def is_conversation_ender(messages: list[Message], idx: int, gap_hours: int = 4) -> bool:
    """Check if message at idx ends a conversation (before gap)."""
    if idx == len(messages) - 1:
        return True
    
    time_diff = messages[idx+1].timestamp - messages[idx].timestamp
    return time_diff > timedelta(hours=gap_hours)


def analyze_conversation(conversation: Conversation) -> AnalysisResult:
    """Analyze a conversation and generate all category results."""
    messages = conversation.messages
    participants = set(m.sender for m in messages)
    
    if not messages:
        return AnalysisResult(
            conversation_title=conversation.title,
            total_messages=0,
            total_participants=0,
            date_range=(datetime.now(), datetime.now()),
            categories=[]
        )
    
    # Initialize counters
    messages_per_person: Counter[str] = Counter()
    night_messages_per_person: Counter[str] = Counter()
    messages_per_day: Counter[str] = Counter()  # date string -> count
    nouns_counter: Counter[str] = Counter()
    message_lengths: dict[str, list[int]] = defaultdict(list)
    reactions_received: Counter[str] = Counter()
    reactions_given: Counter[str] = Counter()
    photos_per_person: Counter[str] = Counter()
    stickers_per_person: Counter[str] = Counter()
    gifs_per_person: Counter[str] = Counter()
    links_per_person: Counter[str] = Counter()
    questions_per_person: Counter[str] = Counter()
    conversation_starters: Counter[str] = Counter()
    conversation_enders: Counter[str] = Counter()
    hour_distribution: Counter[int] = Counter()
    weekday_distribution: Counter[int] = Counter()
    month_distribution: Counter[str] = Counter()
    emojis_per_person: Counter[str] = Counter()
    favorite_emoji_per_person: dict[str, Counter[str]] = defaultdict(Counter)
    most_reacted_message: tuple[Message, int, list[str]] | None = None  # (message, count, reactions)
    
    # Track group name and photo changes
    name_changes: list[tuple[datetime, str, str]] = []  # (timestamp, who, content)
    photo_changes: list[tuple[datetime, str, str]] = []  # (timestamp, who, action)
    
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"
        "]+"
    )
    
    # Analyze each message
    for idx, msg in enumerate(messages):
        sender = msg.sender
        messages_per_person[sender] += 1
        
        # Night messages (0-5 AM)
        if is_night_hour(msg.timestamp.hour):
            night_messages_per_person[sender] += 1
        
        # Messages per day
        day_key = msg.timestamp.strftime("%Y-%m-%d")
        messages_per_day[day_key] += 1
        
        # Time distributions
        hour_distribution[msg.timestamp.hour] += 1
        weekday_distribution[msg.timestamp.weekday()] += 1
        month_distribution[msg.timestamp.strftime("%Y-%m")] += 1
        
        # Text analysis
        if msg.message_type == "text" and msg.content:
            # Nouns for Słownik Grupy
            nouns = get_nouns(msg.content)
            nouns_counter.update(nouns)
            
            # Message length
            message_lengths[sender].append(len(msg.content))
            
            # Questions
            if '?' in msg.content:
                questions_per_person[sender] += 1
            
            # Links
            if 'http' in msg.content.lower():
                links_per_person[sender] += 1
            
            # Emojis
            emojis = emoji_pattern.findall(msg.content)
            emojis_per_person[sender] += len(emojis)
            for emoji in emojis:
                favorite_emoji_per_person[sender][emoji] += 1
        
        # Media types
        if msg.message_type == "photo":
            photos_per_person[sender] += 1
        elif msg.message_type == "sticker":
            stickers_per_person[sender] += 1
        elif msg.message_type == "gif":
            gifs_per_person[sender] += 1
        elif msg.message_type == "name_change":
            name_changes.append((msg.timestamp, sender, msg.content))
        elif msg.message_type == "photo_change":
            photo_changes.append((msg.timestamp, sender, msg.content))
        
        # Reactions
        msg_reactions = []
        for reaction in msg.reactions:
            actor = reaction.get("actor", "")
            if actor:
                try:
                    actor = actor.encode('latin-1').decode('utf-8', errors='ignore')
                except (UnicodeEncodeError, UnicodeDecodeError):
                    pass  # Keep original actor name if encoding fails
                reactions_given[actor] += 1
            reactions_received[sender] += 1
            # Decode reaction emoji
            reaction_emoji = reaction.get("reaction", "")
            try:
                reaction_emoji = reaction_emoji.encode('latin-1').decode('utf-8', errors='ignore')
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
            msg_reactions.append(reaction_emoji)
        
        # Track most reacted message
        if len(msg.reactions) > 0:
            if most_reacted_message is None or len(msg.reactions) > most_reacted_message[1]:
                most_reacted_message = (msg, len(msg.reactions), msg_reactions)
        
        # Conversation starters/enders
        if is_conversation_starter(messages, idx):
            conversation_starters[sender] += 1
        if is_conversation_ender(messages, idx):
            conversation_enders[sender] += 1
    
    # Calculate additional stats
    longest_streaks = {p: calculate_streak(messages, p) for p in participants}
    longest_absences = {p: find_longest_absence(messages, p) for p in participants}
    
    # Average message length per person
    avg_message_lengths = {
        p: sum(lengths) / len(lengths) if lengths else 0
        for p, lengths in message_lengths.items()
    }
    
    # Find longest single message
    longest_message = max(
        (m for m in messages if m.message_type == "text"),
        key=lambda m: len(m.content),
        default=None
    )
    
    # Build category results
    categories = []
    
    # 1. Nocny Marek - Night Owl
    if night_messages_per_person:
        top_night = night_messages_per_person.most_common(3)
        total_night = sum(night_messages_per_person.values())
        night_percent = total_night * 100 // len(messages) if messages else 0
        categories.append(CategoryResult(
            category_id="night_owl",
            title="🦉 Nocny Marek",
            subtitle="Najwięcej wiadomości w nocy (00:00 - 05:00)",
            icon="🌙",
            winner=top_night[0][0] if top_night else None,
            winners=[(name, f"{count} wiadomości") for name, count in top_night],
            value=top_night[0][1] if top_night else 0,
            extra_info="Kiedy inni śpią, oni piszą!",
            fun_fact=f"Łącznie wysłano {total_night} nocnych wiadomości ({night_percent}% wszystkich)"
        ))
    
    # 2. Najbardziej intensywny dzień
    if messages_per_day:
        busiest_day = messages_per_day.most_common(1)[0]
        day_date = datetime.strptime(busiest_day[0], "%Y-%m-%d")
        polish_months = ['', 'stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca',
                         'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia']
        day_formatted = f"{day_date.day} {polish_months[day_date.month]} {day_date.year}"
        seconds_per_msg = 86400 // busiest_day[1] if busiest_day[1] > 0 else 0  # 86400 seconds in a day
        categories.append(CategoryResult(
            category_id="busiest_day",
            title="🔥 Dzień Apokalipsy",
            subtitle="Najbardziej intensywny dzień w historii grupy",
            icon="📅",
            winner=day_formatted,
            value=busiest_day[1],
            extra_info=f"{busiest_day[1]} wiadomości w jeden dzień!",
            fun_fact=f"To średnio 1 wiadomość co {seconds_per_msg} sekund!"
        ))
    
    # 3. Syn Marnotrawny - Longest absence
    polish_months = ['', 'stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca',
                     'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia']
    
    if longest_absences:
        prodigal = max(longest_absences.items(), key=lambda x: x[1][0])
        return_date = prodigal[1][1]
        if return_date:
            return_date_str = f"{return_date.day} {polish_months[return_date.month]} {return_date.year}"
        else:
            return_date_str = "kiedyś"
        categories.append(CategoryResult(
            category_id="prodigal_son",
            title="🚪 Syn Marnotrawny",
            subtitle="Powrót po najdłuższej przerwie",
            icon="👋",
            winner=prodigal[0],
            value=prodigal[1][0],
            extra_info=f"Zniknął na {prodigal[1][0]} dni!",
            fun_fact=f"Wrócił {return_date_str}"
        ))
    
    # 4. Król Spamu - Most messages overall
    if messages_per_person:
        top_spammers = messages_per_person.most_common(5)
        total = sum(messages_per_person.values())
        categories.append(CategoryResult(
            category_id="spam_king",
            title="👑 Król Spamu",
            subtitle="Najwięcej wiadomości ogółem",
            icon="💬",
            winner=top_spammers[0][0],
            winners=[(name, f"{count} ({count*100//total}%)") for name, count in top_spammers],
            value=top_spammers[0][1],
            extra_info=f"{top_spammers[0][1]} wiadomości!",
            fun_fact=f"To {top_spammers[0][1] * 100 // total}% wszystkich wiadomości"
        ))
    
    # 5. Maszyna do pisania - Longest streak
    if longest_streaks:
        streak_winner = max(longest_streaks.items(), key=lambda x: x[1])
        categories.append(CategoryResult(
            category_id="typing_machine",
            title="⌨️ Maszyna do Pisania",
            subtitle="Najdłuższy ciąg wiadomości pod rząd",
            icon="🔄",
            winner=streak_winner[0],
            value=streak_winner[1],
            extra_info=f"{streak_winner[1]} wiadomości pod rząd!",
            fun_fact="Rozmowa z samym sobą level: ekspert"
        ))
    
    # 6. Poeta - Longest message
    if longest_message:
        categories.append(CategoryResult(
            category_id="poet",
            title="📜 Poeta",
            subtitle="Najdłuższa pojedyncza wiadomość",
            icon="✍️",
            winner=longest_message.sender,
            value=len(longest_message.content),
            extra_info=f"{len(longest_message.content)} znaków!",
            fun_fact=f"Fragment: \"{longest_message.content[:100]}...\""
        ))
    
    # 7. Słownik - Most used nouns
    if nouns_counter:
        top_nouns = nouns_counter.most_common(10)
        categories.append(CategoryResult(
            category_id="dictionary",
            title="📚 Słownik Grupy",
            subtitle="Najczęściej używane rzeczowniki",
            icon="🔤",
            winner=top_nouns[0][0],
            winners=[(noun, f"{count}x") for noun, count in top_nouns],
            value=top_nouns[0][1],
            extra_info=f"\"{top_nouns[0][0]}\" - {top_nouns[0][1]} razy!",
            fun_fact="📊 Algorytm: filtrujemy tylko rzeczowniki (po końcówkach i słowniku)"
        ))
    
    # 8. Duch - Least active
    if messages_per_person:
        ghosts = messages_per_person.most_common()
        ghosts.reverse()
        least_active = ghosts[:3]
        categories.append(CategoryResult(
            category_id="ghost",
            title="👻 Duch",
            subtitle="Najmniej aktywny uczestnik",
            icon="🔇",
            winner=least_active[0][0] if least_active else None,
            winners=[(name, f"{count} wiadomości") for name, count in least_active],
            value=least_active[0][1] if least_active else 0,
            extra_info="Cisza to też odpowiedź!",
        ))
    
    # 9. Starter - Conversation starter
    if conversation_starters:
        top_starters = conversation_starters.most_common(3)
        categories.append(CategoryResult(
            category_id="starter",
            title="🎬 Reżyser",
            subtitle="Najczęściej zaczyna rozmowy",
            icon="▶️",
            winner=top_starters[0][0],
            winners=[(name, f"{count}x") for name, count in top_starters],
            value=top_starters[0][1],
            extra_info="Zawsze ma temat do rozmowy!",
            fun_fact="📊 Algorytm: pierwsza wiadomość po 4+ godzinach ciszy = nowa rozmowa"
        ))
    
    # 10. Zamykacz - Conversation ender
    if conversation_enders:
        top_enders = conversation_enders.most_common(3)
        categories.append(CategoryResult(
            category_id="closer",
            title="🚪 Zamykacz",
            subtitle="Najczęściej kończy rozmowy",
            icon="⏹️",
            winner=top_enders[0][0],
            winners=[(name, f"{count}x") for name, count in top_enders],
            value=top_enders[0][1],
            extra_info="Ostatnie słowo zawsze należy do niego!",
            fun_fact="📊 Algorytm: ostatnia wiadomość przed 4+ godzinami ciszy = koniec rozmowy"
        ))
    
    # 11. Reakcjonista - Most reactions given
    if reactions_given:
        top_reactors = reactions_given.most_common(5)
        categories.append(CategoryResult(
            category_id="reactor",
            title="❤️ Reakcjonista",
            subtitle="Rozdał najwięcej reakcji",
            icon="👍",
            winner=top_reactors[0][0],
            winners=[(name, f"{count} reakcji") for name, count in top_reactors],
            value=top_reactors[0][1],
            extra_info="Serce grupy!",
        ))
    
    # 12. Celebryta - Most reactions received
    if reactions_received:
        top_celebrities = reactions_received.most_common(5)
        categories.append(CategoryResult(
            category_id="celebrity",
            title="⭐ Celebryta",
            subtitle="Otrzymał najwięcej reakcji",
            icon="🌟",
            winner=top_celebrities[0][0],
            winners=[(name, f"{count} reakcji") for name, count in top_celebrities],
            value=top_celebrities[0][1],
            extra_info="Gwiazda grupy!",
            fun_fact="📊 Algorytm: suma wszystkich reakcji otrzymanych na wiadomości"
        ))
    
    # 12b. Wiadomość z największą ilością reakcji
    if most_reacted_message:
        msg, count, reactions = most_reacted_message
        reactions_str = " ".join(reactions)
        msg_preview = msg.content[:150] + "..." if len(msg.content) > 150 else msg.content
        categories.append(CategoryResult(
            category_id="viral_message",
            title="💥 Viral",
            subtitle="Wiadomość z największą ilością reakcji",
            icon="🙌",
            winner=msg.sender,
            value=count,
            extra_info=f'"{msg_preview}"',
            fun_fact=f"Reakcje: {reactions_str}",
        ))
    
    # 13. Galernik - Most photos/images
    if photos_per_person:
        top_photographers = photos_per_person.most_common(3)
        categories.append(CategoryResult(
            category_id="paparazzo",
            title="🖼️ Galernik",
            subtitle="Wysłał najwięcej obrazków",
            icon="📁",
            winner=top_photographers[0][0],
            winners=[(name, f"{count} obrazków") for name, count in top_photographers],
            value=top_photographers[0][1],
            extra_info="Memy, zdjęcia, screenshoty - wszystko się liczy!",
        ))
    
    # 14. Śmieszek - Most GIFs/Stickers
    if gifs_per_person or stickers_per_person:
        fun_content = Counter()
        fun_content.update(gifs_per_person)
        fun_content.update(stickers_per_person)
        top_funny = fun_content.most_common(3)
        if top_funny:
            categories.append(CategoryResult(
                category_id="comedian",
                title="🤡 Śmieszek",
                subtitle="Wysłał najwięcej GIFów i naklejek",
                icon="😂",
                winner=top_funny[0][0],
                winners=[(name, f"{count}") for name, count in top_funny],
                value=top_funny[0][1],
                extra_info="GIF wart więcej niż 1000 słów!",
            ))
    
    # 15. Detektyw - Most questions
    if questions_per_person:
        top_questioners = questions_per_person.most_common(3)
        categories.append(CategoryResult(
            category_id="detective",
            title="🔍 Detektyw",
            subtitle="Zadał najwięcej pytań",
            icon="❓",
            winner=top_questioners[0][0],
            winners=[(name, f"{count} pytań") for name, count in top_questioners],
            value=top_questioners[0][1],
            extra_info="Ciekawość to pierwszy stopień do piekła... wiedzy!",
            fun_fact="📊 Algorytm: zliczamy wiadomości zawierające znak zapytania (?)"
        ))
    
    # 16. Linkomaniak - Most links
    if links_per_person:
        top_linkers = links_per_person.most_common(3)
        categories.append(CategoryResult(
            category_id="link_maniac",
            title="🔗 Linkomaniak",
            subtitle="Udostępnił najwięcej linków",
            icon="🌐",
            winner=top_linkers[0][0],
            winners=[(name, f"{count} linków") for name, count in top_linkers],
            value=top_linkers[0][1],
            extra_info="Internet w pigułce!",
        ))
    
    # 17. Emoji Królem - Most emojis
    if emojis_per_person:
        top_emoji = emojis_per_person.most_common(3)
        winner_name = top_emoji[0][0]
        # Find favorite emoji for the winner
        favorite_emoji = ""
        if winner_name in favorite_emoji_per_person:
            fav = favorite_emoji_per_person[winner_name].most_common(3)
            favorite_emoji = " ".join([f"{e}({c}x)" for e, c in fav])
        categories.append(CategoryResult(
            category_id="emoji_king",
            title="😎 Emoji Master",
            subtitle="Używa najwięcej emoji",
            icon="🎭",
            winner=winner_name,
            winners=[(name, f"{count} emoji") for name, count in top_emoji],
            value=top_emoji[0][1],
            extra_info="Obrazek wart więcej niż słowa!",
            fun_fact=f"Ulubione emoji: {favorite_emoji}" if favorite_emoji else None,
        ))
    
    # 18. Pisarz - Longest average message
    if avg_message_lengths:
        writers = sorted(avg_message_lengths.items(), key=lambda x: x[1], reverse=True)[:3]
        categories.append(CategoryResult(
            category_id="writer",
            title="📝 Pisarz",
            subtitle="Najdłuższe średnie wiadomości",
            icon="📖",
            winner=writers[0][0],
            winners=[(name, f"śr. {int(length)} znaków") for name, length in writers],
            value=int(writers[0][1]),
            extra_info="Jakość ponad ilość!",
        ))
    
    # 19. Najbardziej aktywna godzina
    if hour_distribution:
        peak_hour = hour_distribution.most_common(1)[0]
        categories.append(CategoryResult(
            category_id="peak_hour",
            title="⏰ Godzina Szczytu",
            subtitle="Najbardziej aktywna pora dnia",
            icon="🕐",
            winner=f"{peak_hour[0]}:00 - {peak_hour[0]+1}:00",
            value=peak_hour[1],
            extra_info=f"{peak_hour[1]} wiadomości o tej porze!",
        ))
    
    # 20. Historia nazw i obrazków grupy
    if name_changes or photo_changes:
        # Sort name changes by timestamp and calculate durations
        name_changes_sorted = sorted(name_changes, key=lambda x: x[0])
        
        polish_months_short = ['', 'sty', 'lut', 'mar', 'kwi', 'maj', 'cze',
                               'lip', 'sie', 'wrz', 'paź', 'lis', 'gru']
        
        # Calculate timeline for names with durations
        timeline_entries = []
        total_span = (messages[-1].timestamp - messages[0].timestamp).days if messages else 1
        if total_span < 1:
            total_span = 1
        
        for i, (ts, who, content) in enumerate(name_changes_sorted):
            # Extract the new name from content
            new_name = content
            if ' na ' in content.lower():
                new_name = content.split(' na ', 1)[-1].strip('".')
            elif 'named the group' in content.lower():
                parts = content.split('named the group', 1)
                if len(parts) > 1:
                    new_name = parts[1].strip(' .')
            
            # Calculate duration until next change or end
            if i + 1 < len(name_changes_sorted):
                end_ts = name_changes_sorted[i + 1][0]
            else:
                end_ts = messages[-1].timestamp
            
            duration_days = (end_ts - ts).days
            if duration_days < 1:
                duration_days = 1
            
            # Calculate percentage of total timeline
            percentage = (duration_days / total_span) * 100
            if percentage < 5:
                percentage = 5  # Minimum width for visibility
            
            date_str = f"{ts.day} {polish_months_short[ts.month]}"
            timeline_entries.append({
                'name': new_name,
                'who': who,
                'date': date_str,
                'days': duration_days,
                'percentage': percentage,
                'start_ts': ts,
            })
        
        # Count photo changes
        photo_count = len(photo_changes)
        
        categories.append(CategoryResult(
            category_id="group_identity",
            title="🎭 Metamorfozy",
            subtitle="Historia nazw grupy",
            icon="🎨",
            winner=None,
            winners=timeline_entries,  # Special format for horizontal timeline
            value=len(name_changes),
            extra_info=f"{len(name_changes)} zmian nazwy" + (f", {photo_count} zmian zdjęcia" if photo_count else ""),
            fun_fact=f"Najdłuższa nazwa: {max(timeline_entries, key=lambda x: x['days'])['days']} dni" if timeline_entries else None
        ))
    
    # 21. Statystyki ogólne
    total_days = (messages[-1].timestamp - messages[0].timestamp).days + 1
    avg_per_day = len(messages) / total_days if total_days > 0 else 0
    
    categories.append(CategoryResult(
        category_id="summary",
        title="📊 Podsumowanie",
        subtitle=f"Statystyki grupy {conversation.title}",
        icon="📈",
        winner=None,
        extra_info=f"""
        📨 Łącznie wiadomości: {len(messages):,}
        👥 Uczestników: {len(participants)}
        📅 Dni aktywności: {total_days:,}
        📊 Średnio dziennie: {avg_per_day:.1f}
        """,
        fun_fact=f"Od {messages[0].timestamp.strftime('%d.%m.%Y')} do {messages[-1].timestamp.strftime('%d.%m.%Y')}"
    ))
    
    return AnalysisResult(
        conversation_title=conversation.title,
        total_messages=len(messages),
        total_participants=len(participants),
        date_range=(messages[0].timestamp, messages[-1].timestamp),
        categories=categories
    )
