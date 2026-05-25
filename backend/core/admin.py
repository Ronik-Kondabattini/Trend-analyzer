from django.contrib import admin
from .models import SearchHistory, SavedIdea, TrendingTopic


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('topic', 'category', 'trend_score', 'user', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('topic',)


@admin.register(SavedIdea)
class SavedIdeaAdmin(admin.ModelAdmin):
    list_display = ('idea_title', 'idea_type', 'difficulty', 'user', 'created_at')
    list_filter = ('idea_type', 'difficulty')
    search_fields = ('idea_title',)


@admin.register(TrendingTopic)
class TrendingTopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'emoji', 'category', 'trend_score')
    list_filter = ('category',)
    search_fields = ('name',)
