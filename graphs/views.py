# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import Sensor, Point
from django.template import loader



def plot(requests):
    return render(requests, 'graphs/graphs.html')

