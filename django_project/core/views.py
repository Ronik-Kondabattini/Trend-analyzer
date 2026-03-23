"""
core/views.py — Django Class-Based Views

Page views render templates.
API views return JSON via AJAX.
All authentication uses Django sessions.
"""
import json

from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import LoginForm, SignupForm, AnalyzeForm, SaveIdeaForm
from .models import SearchHistory, SavedIdea, TrendingTopic
from .services import TrendAnalyzerService
from .utils import json_ok, json_err, json_form_errors


# ========================================================
# AUTH VIEWS — render HTML templates, Django session auth
# ========================================================

class UserLoginView(View):
    """GET → render login page.  POST → authenticate & redirect."""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'auth/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        return render(request, 'auth/login.html', {'form': form})


class UserSignupView(View):
    """GET → render signup page.  POST → create account & redirect."""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'auth/signup.html', {'form': SignupForm()})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        return render(request, 'auth/signup.html', {'form': form})


class UserLogoutView(View):
    """GET or POST → logout & redirect to login."""

    def get(self, request):
        logout(request)
        return redirect('login')

    def post(self, request):
        logout(request)
        return redirect('login')


# ========================================================
# DASHBOARD VIEW — server-rendered page with initial data
# ========================================================

class DashboardView(LoginRequiredMixin, View):
    """Main dashboard. Passes server-rendered JSON to the template."""

    def get(self, request):
        trending = list(TrendingTopic.objects.top().values(
            'id', 'name', 'category', 'emoji', 'trend_score'
        ))
        stats = SearchHistory.objects.aggregate_stats(request.user)
        stats['saved_ideas_count'] = SavedIdea.objects.user_count(request.user)
        history = list(SearchHistory.objects.recent(request.user).values(
            'id', 'topic', 'category', 'trend_score', 'search_volume', 'created_at'
        ))
        for h in history:
            h['created_at'] = h['created_at'].isoformat()
        saved = list(SavedIdea.objects.for_user(request.user).values(
            'id', 'topic', 'idea_type', 'idea_title', 'difficulty', 'potential', 'created_at'
        ))
        for s in saved:
            s['created_at'] = s['created_at'].isoformat()

        return render(request, 'dashboard/index.html', {
            'trending_json': json.dumps(trending),
            'stats_json': json.dumps(stats),
            'history_json': json.dumps(history),
            'saved_json': json.dumps(saved),
        })


# ========================================================
# API VIEWS — JSON endpoints called by frontend JS via AJAX
# ========================================================

@method_decorator(csrf_exempt, name='dispatch')
class AnalyzeAPIView(LoginRequiredMixin, View):
    """POST /api/analyze/  — analyze a topic."""

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return json_err('Invalid JSON.')
        form = AnalyzeForm(data)
        if not form.is_valid():
            return json_form_errors(form.errors)
        result = TrendAnalyzerService.analyze(form.cleaned_data['topic'], request.user)
        return json_ok(result)


@method_decorator(csrf_exempt, name='dispatch')
class HistoryAPIView(LoginRequiredMixin, View):
    """GET /api/history/  — list.  DELETE /api/history/ — remove."""

    def get(self, request):
        qs = SearchHistory.objects.recent(request.user)
        data = list(qs.values('id','topic','category','trend_score','search_volume','created_at'))
        for d in data:
            d['created_at'] = d['created_at'].isoformat()
        return json_ok(data)

    def delete(self, request):
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return json_err('Invalid JSON.')
        pk = body.get('id')
        if not pk:
            return json_err('id is required.')
        SearchHistory.objects.filter(id=pk, user=request.user).delete()
        return json_ok({'ok': True})


@method_decorator(csrf_exempt, name='dispatch')
class SavedIdeaAPIView(LoginRequiredMixin, View):
    """GET → list.  POST → create.  DELETE → remove."""

    def get(self, request):
        qs = SavedIdea.objects.for_user(request.user)
        data = list(qs.values('id','topic','idea_type','idea_title','difficulty','potential','created_at'))
        for d in data:
            d['created_at'] = d['created_at'].isoformat()
        return json_ok(data)

    def post(self, request):
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return json_err('Invalid JSON.')
        form = SaveIdeaForm(body)
        if not form.is_valid():
            return json_form_errors(form.errors)
        idea = SavedIdea.objects.create(user=request.user, **form.cleaned_data)
        return json_ok({'id': idea.id, 'idea_title': idea.idea_title}, status=201)

    def delete(self, request):
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return json_err('Invalid JSON.')
        pk = body.get('id')
        if not pk:
            return json_err('id is required.')
        SavedIdea.objects.filter(id=pk, user=request.user).delete()
        return json_ok({'ok': True})


class TrendingAPIView(View):
    """GET /api/trending/ — public endpoint."""

    def get(self, request):
        data = list(TrendingTopic.objects.top().values('id','name','category','emoji','trend_score'))
        return json_ok(data)


class StatsAPIView(LoginRequiredMixin, View):
    """GET /api/stats/ — user aggregate stats."""

    def get(self, request):
        agg = SearchHistory.objects.aggregate_stats(request.user)
        agg['saved_ideas_count'] = SavedIdea.objects.user_count(request.user)
        return json_ok({
            'total_searches': agg['total_searches'],
            'avg_trend_score': agg['avg_score'],
            'total_search_volume': agg['total_volume'],
            'top_category': agg['top_category'],
            'saved_ideas_count': agg['saved_ideas_count'],
        })
