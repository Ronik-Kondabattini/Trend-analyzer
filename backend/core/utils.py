"""
core/utils.py — Shared helpers
"""
from django.http import JsonResponse


def json_ok(data, status=200):
    return JsonResponse(data, status=status, safe=False)


def json_err(msg, status=400):
    return JsonResponse({'detail': msg}, status=status)


def json_form_errors(errors, status=400):
    return JsonResponse({'errors': errors.get_json_data()}, status=status)
