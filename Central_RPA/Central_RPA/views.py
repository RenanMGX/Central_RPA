from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest #for Typing
from django.contrib.auth.decorators import permission_required, login_required
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User, Permission
from django.http import JsonResponse
from typing import List, Dict

@login_required()
def index(request:WSGIRequest):
    return render(request, 'base.html')