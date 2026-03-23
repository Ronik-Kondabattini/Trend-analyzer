"""
python manage.py seed  —  Seeds trending topics + demo user.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import TrendingTopic


class Command(BaseCommand):
    help = 'Seed trending topics and create demo user'

    def handle(self, *args, **options):
        # Demo user
        if not User.objects.filter(username='demo@example.com').exists():
            User.objects.create_user('demo@example.com', 'demo@example.com', 'password123')
            self.stdout.write(self.style.SUCCESS('Created demo user: demo@example.com / password123'))
        else:
            self.stdout.write('Demo user already exists.')

        # Trending topics
        topics = [
            {'name':'AI Video Generation','category':'Technology','emoji':'\U0001f916','trend_score':97},
            {'name':'Home Workouts','category':'Fitness','emoji':'\U0001f4aa','trend_score':94},
            {'name':'Budget Cooking','category':'Cooking','emoji':'\U0001f373','trend_score':91},
            {'name':'Passive Income Ideas','category':'Finance','emoji':'\U0001f4b0','trend_score':96},
            {'name':'Indie Game Dev','category':'Gaming','emoji':'\U0001f3ae','trend_score':89},
            {'name':'Productivity Hacks','category':'Technology','emoji':'\u26a1','trend_score':93},
            {'name':'Sourdough Baking','category':'Cooking','emoji':'\U0001f35e','trend_score':85},
            {'name':'Crypto Trading','category':'Finance','emoji':'\U0001f4c8','trend_score':92},
            {'name':'Yoga for Beginners','category':'Fitness','emoji':'\U0001f9d8','trend_score':88},
            {'name':'Web3 Development','category':'Technology','emoji':'\U0001f310','trend_score':90},
            {'name':'Meal Prep Sunday','category':'Cooking','emoji':'\U0001f957','trend_score':87},
            {'name':'Retro Gaming','category':'Gaming','emoji':'\U0001f47e','trend_score':83},
        ]
        created = 0
        for t in topics:
            _, c = TrendingTopic.objects.get_or_create(name=t['name'], defaults=t)
            if c:
                created += 1
        self.stdout.write(self.style.SUCCESS(f'Seeded {created} trending topics.'))
