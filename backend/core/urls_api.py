from django.urls import path
from .views import (
    AnalyzeAPIView, HistoryAPIView, SavedIdeaAPIView,
    TrendingAPIView, StatsAPIView,
)

urlpatterns = [
    path('analyze/',     AnalyzeAPIView.as_view(),   name='api_analyze'),
    path('history/',     HistoryAPIView.as_view(),    name='api_history'),
    path('saved-ideas/', SavedIdeaAPIView.as_view(),  name='api_saved_ideas'),
    path('trending/',    TrendingAPIView.as_view(),   name='api_trending'),
    path('stats/',       StatsAPIView.as_view(),      name='api_stats'),
]
