"""
core/services.py — Business Logic Layer

Usage:
    from core.services import TrendAnalyzerService
    result = TrendAnalyzerService.analyze('AI tools', request.user)
"""
import random
from urllib.parse import quote_plus
from .models import SearchHistory

CATEGORY_KEYWORDS = {
    'technology': ['tech','ai','programming','software','coding','computer','app','saas','startup','machine learning','web','developer','api','cloud','devops'],
    'fitness':    ['fitness','gym','workout','exercise','health','muscle','weight','diet','nutrition','yoga','running','cardio','crossfit'],
    'cooking':    ['cook','food','recipe','meal','baking','kitchen','restaurant','chef','cuisine','eat','dinner','lunch','breakfast'],
    'finance':    ['finance','money','invest','stock','crypto','budget','saving','wealth','income','bank','trading','forex','real estate'],
    'gaming':     ['game','gaming','esport','playstation','xbox','nintendo','steam','twitch','streamer','fps','rpg'],
    'travel':     ['travel','trip','flight','hotel','backpack','nomad','vacation','destination','tourism','adventure'],
    'education':  ['learn','study','education','course','school','university','teach','skill','tutorial','knowledge','exam'],
}

VIDEO_DB = {
    'technology': [
        {'title':'10 AI Tools That Will Change Your Life in 2025','views':'2.4M','channel':'TechVision','thumbnail':'tech','duration':'12:34','trend_score':95},
        {'title':'Building a SaaS in 48 Hours — Full Process','views':'890K','channel':'IndieHacker','thumbnail':'saas','duration':'28:15','trend_score':88},
        {'title':'Why Everyone is Switching to This Framework','views':'1.1M','channel':'CodeCraft','thumbnail':'framework','duration':'15:42','trend_score':92},
        {'title':'Quantum Computing Explained Simply','views':'3.2M','channel':'ScienceHub','thumbnail':'quantum','duration':'18:20','trend_score':85},
        {'title':'Top 5 Programming Languages in 2025','views':'1.8M','channel':'DevMaster','thumbnail':'programming','duration':'10:05','trend_score':90},
    ],
    'fitness': [
        {'title':'30-Day Body Transformation Challenge','views':'5.1M','channel':'FitLife','thumbnail':'fitness','duration':'22:10','trend_score':97},
        {'title':'Morning Routine That Changed Everything','views':'3.8M','channel':'WellnessGuru','thumbnail':'morning','duration':'14:30','trend_score':93},
        {'title':'Science-Based Workout for Maximum Results','views':'2.1M','channel':'GymScience','thumbnail':'workout','duration':'19:45','trend_score':89},
        {'title':'Meal Prep Like a Pro — Full Week Guide','views':'4.2M','channel':'NutriFit','thumbnail':'meal','duration':'25:00','trend_score':91},
        {'title':'Home Workout No Equipment Needed','views':'6.3M','channel':'BodyWeight','thumbnail':'home','duration':'30:00','trend_score':96},
    ],
    'cooking': [
        {'title':'5 Viral TikTok Recipes Actually Worth Making','views':'4.5M','channel':'FoodieVibes','thumbnail':'cooking','duration':'16:20','trend_score':94},
        {'title':'Restaurant-Quality Meals Under $10','views':'2.9M','channel':'BudgetChef','thumbnail':'budget','duration':'20:15','trend_score':90},
        {'title':'The Secret to Perfect Sourdough Bread','views':'1.7M','channel':'BakeHouse','thumbnail':'bread','duration':'24:30','trend_score':86},
        {'title':'One-Pot Wonders: 10 Easy Dinner Ideas','views':'3.3M','channel':'QuickMeals','thumbnail':'onepot','duration':'18:45','trend_score':92},
        {'title':'Street Food From Around the World at Home','views':'5.8M','channel':'GlobalEats','thumbnail':'street','duration':'22:00','trend_score':95},
    ],
    'finance': [
        {'title':'How I Built 7 Streams of Income by 25','views':'6.7M','channel':'MoneyMoves','thumbnail':'income','duration':'18:30','trend_score':96},
        {'title':'Investing for Beginners: Complete 2025 Guide','views':'3.4M','channel':'WealthPath','thumbnail':'invest','duration':'32:00','trend_score':91},
        {'title':'Side Hustles That Actually Pay Well','views':'4.1M','channel':'HustleHub','thumbnail':'hustle','duration':'14:20','trend_score':93},
        {'title':'Crypto vs Stocks: Where to Put Your Money','views':'2.8M','channel':'FinanceFlow','thumbnail':'crypto','duration':'21:15','trend_score':88},
        {'title':'Budget Like a Millionaire','views':'1.9M','channel':'SmartMoney','thumbnail':'budget','duration':'16:40','trend_score':85},
    ],
    'gaming': [
        {'title':'The Most Anticipated Games of 2025','views':'7.2M','channel':'GameZone','thumbnail':'gaming','duration':'20:00','trend_score':98},
        {'title':'How This Indie Game Became a Phenomenon','views':'3.6M','channel':'IndieSpot','thumbnail':'indie','duration':'15:30','trend_score':90},
        {'title':'Pro Tips to Instantly Improve Your Gameplay','views':'4.8M','channel':'ProGamer','thumbnail':'tips','duration':'12:45','trend_score':94},
        {'title':'Building a Gaming Setup Under $500','views':'2.5M','channel':'SetupKing','thumbnail':'setup','duration':'18:20','trend_score':87},
        {'title':'The Evolution of Open World Games','views':'5.1M','channel':'GameHistory','thumbnail':'openworld','duration':'25:10','trend_score':92},
    ],
    'travel': [
        {'title':'How to Travel the World for $50/Day','views':'8.1M','channel':'BudgetNomad','thumbnail':'travel','duration':'19:30','trend_score':96},
        {'title':'Hidden Gems: Places Tourists Never Visit','views':'4.3M','channel':'OffTheMap','thumbnail':'hidden','duration':'22:15','trend_score':93},
        {'title':'Solo Travel Safety Tips You Must Know','views':'2.7M','channel':'SafeTraveler','thumbnail':'solo','duration':'14:00','trend_score':89},
        {'title':'Best Travel Credit Cards Ranked','views':'3.1M','channel':'PointsGuru','thumbnail':'cards','duration':'16:45','trend_score':87},
        {'title':'Van Life: Full Conversion Guide','views':'5.5M','channel':'VanDreams','thumbnail':'van','duration':'35:00','trend_score':94},
    ],
    'education': [
        {'title':'How to Learn Anything 10x Faster','views':'9.2M','channel':'BrainHacks','thumbnail':'learn','duration':'18:20','trend_score':97},
        {'title':'Free Online Courses Actually Worth It','views':'5.6M','channel':'EduPicks','thumbnail':'courses','duration':'20:00','trend_score':94},
        {'title':'Study Techniques Backed by Science','views':'3.8M','channel':'SciStudy','thumbnail':'study','duration':'15:30','trend_score':91},
        {'title':'Building a Second Brain: Complete System','views':'4.1M','channel':'NoteGenius','thumbnail':'brain','duration':'25:00','trend_score':90},
        {'title':'The Best Note-Taking Method for Students','views':'2.9M','channel':'StudyPro','thumbnail':'notes','duration':'12:15','trend_score':88},
    ],
    'default': [
        {'title':'How to Go Viral: Content Strategy Secrets','views':'3.2M','channel':'CreatorLab','thumbnail':'viral','duration':'16:45','trend_score':93},
        {'title':'The Psychology Behind Trending Topics','views':'1.8M','channel':'MindMatters','thumbnail':'psychology','duration':'20:30','trend_score':87},
        {'title':"Complete Beginner's Guide to [Topic]",'views':'2.5M','channel':'LearnFast','thumbnail':'beginner','duration':'24:00','trend_score':90},
        {'title':'10 Things Nobody Tells You About This','views':'4.1M','channel':'TruthBomb','thumbnail':'truth','duration':'14:15','trend_score':92},
        {'title':'Expert Roundtable: Deep Dive Discussion','views':'890K','channel':'DeepDive','thumbnail':'expert','duration':'45:00','trend_score':85},
    ],
}

IDEAS_DB = {
    'technology': [
        {'type':'Blog Post','title':'The Complete Guide to AI-Powered Productivity','difficulty':'Medium','potential':'High','icon':'\ud83d\udcdd'},
        {'type':'YouTube Video','title':"I Tested Every AI Tool So You Don't Have To",'difficulty':'Hard','potential':'Very High','icon':'\ud83c\udfac'},
        {'type':'Twitter Thread','title':'15 Underrated Tech Tools That Save Hours','difficulty':'Easy','potential':'High','icon':'\ud83d\udc26'},
        {'type':'Podcast','title':'Interview: Building the Next Big Thing','difficulty':'Medium','potential':'Medium','icon':'\ud83c\udf99\ufe0f'},
        {'type':'Instagram Reel','title':'Day in the Life of a Startup Founder','difficulty':'Easy','potential':'Very High','icon':'\ud83d\udcf1'},
        {'type':'Newsletter','title':'Weekly Tech Trends for Non-Techies','difficulty':'Medium','potential':'High','icon':'\ud83d\udce7'},
    ],
    'fitness': [
        {'type':'YouTube Video','title':'7-Minute Morning Workout That Works','difficulty':'Easy','potential':'Very High','icon':'\ud83c\udfac'},
        {'type':'Instagram Reel','title':'Gym Mistakes 90% of People Make','difficulty':'Easy','potential':'Very High','icon':'\ud83d\udcf1'},
        {'type':'Blog Post','title':'Science-Backed Nutrition for Muscle Growth','difficulty':'Hard','potential':'High','icon':'\ud83d\udcdd'},
        {'type':'TikTok','title':'Healthy Snack Ideas Under 200 Calories','difficulty':'Easy','potential':'Very High','icon':'\ud83c\udfb5'},
        {'type':'Podcast','title':'Debunking Fitness Myths with Science','difficulty':'Medium','potential':'Medium','icon':'\ud83c\udf99\ufe0f'},
        {'type':'E-book','title':'The No-BS Guide to Getting in Shape','difficulty':'Hard','potential':'High','icon':'\ud83d\udcda'},
    ],
    'cooking': [
        {'type':'YouTube Video','title':'Master 5 Sauces That Transform Any Meal','difficulty':'Medium','potential':'Very High','icon':'\ud83c\udfac'},
        {'type':'TikTok','title':'60-Second Recipe: Crispy Garlic Noodles','difficulty':'Easy','potential':'Very High','icon':'\ud83c\udfb5'},
        {'type':'Blog Post','title':'Pantry Staples: 20 Meals from 10 Ingredients','difficulty':'Medium','potential':'High','icon':'\ud83d\udcdd'},
        {'type':'Instagram Reel','title':'Aesthetic Cooking ASMR Compilation','difficulty':'Easy','potential':'High','icon':'\ud83d\udcf1'},
        {'type':'Newsletter','title':'Weekly Meal Plan + Grocery List','difficulty':'Medium','potential':'Medium','icon':'\ud83d\udce7'},
        {'type':'E-book','title':'College Cooking: Gourmet on a Budget','difficulty':'Hard','potential':'High','icon':'\ud83d\udcda'},
    ],
    'finance': [
        {'type':'YouTube Video','title':'How I Save $2000/Month on a Normal Salary','difficulty':'Easy','potential':'Very High','icon':'\ud83c\udfac'},
        {'type':'Twitter Thread','title':'Money Lessons I Wish I Knew at 20','difficulty':'Easy','potential':'Very High','icon':'\ud83d\udc26'},
        {'type':'Blog Post','title':"Beginner's Guide to Index Fund Investing",'difficulty':'Medium','potential':'High','icon':'\ud83d\udcdd'},
        {'type':'Podcast','title':'From Broke to Financial Freedom: Real Stories','difficulty':'Medium','potential':'High','icon':'\ud83c\udf99\ufe0f'},
        {'type':'Instagram Reel','title':'Daily Money Habits of Wealthy People','difficulty':'Easy','potential':'High','icon':'\ud83d\udcf1'},
        {'type':'Newsletter','title':'Weekly Market Insights in Plain English','difficulty':'Hard','potential':'Medium','icon':'\ud83d\udce7'},
    ],
    'gaming': [
        {'type':'YouTube Video','title':'Ranking Every Game Release This Month','difficulty':'Medium','potential':'Very High','icon':'\ud83c\udfac'},
        {'type':'TikTok','title':'Hidden Easter Eggs You Definitely Missed','difficulty':'Easy','potential':'Very High','icon':'\ud83c\udfb5'},
        {'type':'Blog Post','title':'Ultimate Gaming Setup Guide for Every Budget','difficulty':'Medium','potential':'High','icon':'\ud83d\udcdd'},
        {'type':'Twitter Thread','title':'Most Underrated Games of the Decade','difficulty':'Easy','potential':'High','icon':'\ud83d\udc26'},
        {'type':'Podcast','title':'Game Developers Share Their Secrets','difficulty':'Hard','potential':'Medium','icon':'\ud83c\udf99\ufe0f'},
        {'type':'Instagram Reel','title':'Satisfying Gaming Moments Compilation','difficulty':'Easy','potential':'Very High','icon':'\ud83d\udcf1'},
    ],
    'travel': [
        {'type':'YouTube Video','title':'Budget Travel Hacks That Save Thousands','difficulty':'Easy','potential':'Very High','icon':'\ud83c\udfac'},
        {'type':'Blog Post','title':'Ultimate Packing Guide: Carry-On Only','difficulty':'Medium','potential':'High','icon':'\ud83d\udcdd'},
        {'type':'Instagram Reel','title':'Most Instagrammable Spots in Each Country','difficulty':'Easy','potential':'Very High','icon':'\ud83d\udcf1'},
        {'type':'TikTok','title':'Airport Hacks That Actually Work','difficulty':'Easy','potential':'Very High','icon':'\ud83c\udfb5'},
        {'type':'Podcast','title':'Digital Nomad Life: The Real Truth','difficulty':'Medium','potential':'Medium','icon':'\ud83c\udf99\ufe0f'},
        {'type':'Newsletter','title':'Weekly Flight Deals & Hidden Gems','difficulty':'Medium','potential':'High','icon':'\ud83d\udce7'},
    ],
    'education': [
        {'type':'YouTube Video','title':'The Feynman Technique: Learn Anything Fast','difficulty':'Easy','potential':'Very High','icon':'\ud83c\udfac'},
        {'type':'Blog Post','title':'Building a Personal Knowledge System','difficulty':'Hard','potential':'High','icon':'\ud83d\udcdd'},
        {'type':'Twitter Thread','title':'20 Free Resources Better Than Paid Courses','difficulty':'Easy','potential':'Very High','icon':'\ud83d\udc26'},
        {'type':'TikTok','title':'Study With Me: Pomodoro Timer Edition','difficulty':'Easy','potential':'High','icon':'\ud83c\udfb5'},
        {'type':'Podcast','title':'How Top Performers Structure Their Learning','difficulty':'Medium','potential':'Medium','icon':'\ud83c\udf99\ufe0f'},
        {'type':'E-book','title':"The Self-Taught Learner's Handbook",'difficulty':'Hard','potential':'High','icon':'\ud83d\udcda'},
    ],
    'default': [
        {'type':'YouTube Video','title':'Everything You Need to Know About [Topic]','difficulty':'Medium','potential':'High','icon':'\ud83c\udfac'},
        {'type':'Blog Post','title':"The Ultimate Beginner's Guide",'difficulty':'Medium','potential':'High','icon':'\ud83d\udcdd'},
        {'type':'Twitter Thread','title':"10 Surprising Facts Most People Don't Know",'difficulty':'Easy','potential':'Very High','icon':'\ud83d\udc26'},
        {'type':'TikTok','title':'Quick Tips in Under 60 Seconds','difficulty':'Easy','potential':'Very High','icon':'\ud83c\udfb5'},
        {'type':'Podcast','title':'Deep Dive: Expert Interview Series','difficulty':'Hard','potential':'Medium','icon':'\ud83c\udf99\ufe0f'},
        {'type':'Newsletter','title':'Weekly Curated Insights & Updates','difficulty':'Medium','potential':'Medium','icon':'\ud83d\udce7'},
    ],
}

RELATED_TOPICS = {
    'technology': ['Artificial Intelligence','Web Development','Cloud Computing','Cybersecurity','Blockchain'],
    'fitness':    ['Nutrition','Mental Health','Yoga','CrossFit','Marathon Training'],
    'cooking':    ['Baking','Meal Prep','Vegan Recipes','Kitchen Gadgets','Food Photography'],
    'finance':    ['Real Estate','Cryptocurrency','Passive Income','Tax Planning','Retirement'],
    'gaming':     ['Game Development','Esports','VR Gaming','Retro Gaming','Game Reviews'],
    'travel':     ['Digital Nomad','Budget Travel','Luxury Resorts','Adventure Sports','Cultural Experiences'],
    'education':  ['Online Courses','Speed Reading','Memory Techniques','Language Learning','Study Hacks'],
    'default':    ['Content Creation','Social Media','Marketing','Personal Brand','Storytelling'],
}


class TrendAnalyzerService:
    """Pure Python business logic. Zero JS."""

    @staticmethod
    def classify_topic(topic: str) -> str:
        t = topic.lower()
        for cat, kws in CATEGORY_KEYWORDS.items():
            if any(kw in t for kw in kws):
                return cat
        return 'default'

    @staticmethod
    def get_video_suggestions(category: str, topic: str) -> list:
        vids = VIDEO_DB.get(category, VIDEO_DB['default'])
        out = []
        for v in vids:
            title = v['title'].replace('[Topic]', topic)
            out.append({**v, 'title': title,
                        'youtube_url': f'https://www.youtube.com/results?search_query={quote_plus(title)}'})
        return out

    @staticmethod
    def get_content_ideas(category: str, topic: str) -> list:
        ideas = IDEAS_DB.get(category, IDEAS_DB['default'])
        return [{**i, 'title': i['title'].replace('[Topic]', topic)} for i in ideas]

    @staticmethod
    def get_related_topics(category: str, topic: str) -> list:
        return [t for t in RELATED_TOPICS.get(category, RELATED_TOPICS['default'])
                if t.lower() != topic.lower()]

    @staticmethod
    def generate_metrics() -> dict:
        return {
            'trend_score': random.randint(70, 99),
            'search_volume': random.randint(50000, 550000),
            'competition': random.choice(['Low', 'Medium', 'High']),
            'growth_percentage': random.randint(10, 210),
        }

    @classmethod
    def analyze(cls, topic: str, user=None) -> dict:
        category = cls.classify_topic(topic)
        metrics  = cls.generate_metrics()
        if user and user.is_authenticated:
            SearchHistory.objects.create(
                user=user, topic=topic, category=category,
                trend_score=metrics['trend_score'],
                search_volume=metrics['search_volume'],
            )
        return {
            'topic': topic, 'category': category, **metrics,
            'videos': cls.get_video_suggestions(category, topic),
            'content_ideas': cls.get_content_ideas(category, topic),
            'related_topics': cls.get_related_topics(category, topic),
        }
