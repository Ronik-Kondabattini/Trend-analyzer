"""
core/models.py — Django ORM Models

MySQL tables created by `python manage.py migrate`:

  core_searchhistory   ─ user search logs with trend scores
  core_savedidea       ─ bookmarked content ideas
  core_trendingtopic   ─ pre-seeded hot topics for the homepage
"""
from django.db import models
from django.conf import settings
from django.db.models import Avg, Sum, Count


# ------------------------------------------------------------------ Managers

class SearchHistoryManager(models.Manager):

    def for_user(self, user):
        return self.filter(user=user).order_by('-created_at')

    def recent(self, user, limit=20):
        return self.for_user(user)[:limit]

    def user_count(self, user):
        return self.filter(user=user).count()

    def aggregate_stats(self, user):
        qs = self.filter(user=user)
        agg = qs.aggregate(
            avg_score=Avg('trend_score'),
            total_volume=Sum('search_volume'),
            total_searches=Count('id'),
        )
        top = (
            qs.values('category')
            .annotate(cnt=Count('id'))
            .order_by('-cnt')
            .first()
        )
        return {
            'avg_score': round(agg['avg_score'] or 0),
            'total_volume': agg['total_volume'] or 0,
            'top_category': top['category'] if top else 'N/A',
            'total_searches': agg['total_searches'] or 0,
        }


class SavedIdeaManager(models.Manager):

    def for_user(self, user):
        return self.filter(user=user).order_by('-created_at')

    def user_count(self, user):
        return self.filter(user=user).count()


class TrendingTopicManager(models.Manager):

    def top(self, limit=12):
        return self.order_by('-trend_score')[:limit]


# ------------------------------------------------------------------ Models

class SearchHistory(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='searches')
    topic      = models.CharField(max_length=255)
    category   = models.CharField(max_length=50, blank=True, default='')
    trend_score   = models.IntegerField(default=0)
    search_volume = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = SearchHistoryManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Search histories'
        indexes = [models.Index(fields=['user', '-created_at'])]

    def __str__(self):
        return f'{self.topic} ({self.trend_score}%) — {self.user}'


class SavedIdea(models.Model):
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_ideas')
    topic      = models.CharField(max_length=255, blank=True, default='')
    idea_type  = models.CharField(max_length=100, blank=True, default='')
    idea_title = models.CharField(max_length=500)
    difficulty = models.CharField(max_length=20, blank=True, default='')
    potential  = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SavedIdeaManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Saved ideas'

    def __str__(self):
        return f'{self.idea_title} ({self.idea_type})'


class TrendingTopic(models.Model):
    name        = models.CharField(max_length=255)
    category    = models.CharField(max_length=50, blank=True, default='')
    emoji       = models.CharField(max_length=10, blank=True, default='')
    trend_score = models.IntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    objects = TrendingTopicManager()

    class Meta:
        ordering = ['-trend_score']

    def __str__(self):
        return f'{self.emoji} {self.name} ({self.trend_score}%)'
