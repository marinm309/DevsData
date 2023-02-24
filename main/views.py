from django.shortcuts import render, redirect
from . models import Event, EventUsers
from users.models import Customer
from datetime import datetime
from . serializer import EventSearializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

def home(request):
    if request.user.is_authenticated:
        user = request.user
        customer = Customer.objects.get(user=user)
        events = Event.objects.exclude(id__in=EventUsers.objects.filter(user=customer).values_list('event_id', flat=True))
    else:
        events = Event.objects.all()

    context = {'events': events}
    return render(request, 'main/home.html', context)


def reserve(request, pk):
    user = request.user
    customer = Customer.objects.get(user=user)
    event = Event.objects.get(id=pk)
    event_user = EventUsers.objects.filter(user=customer, event=event)
    
    if not event_user:
        EventUsers.objects.create(user=customer, event=event)
        return redirect('home')
    else:
        ev = EventUsers.objects.get(user=customer, event=event)
        delta1 = ev.event.start_date.date() - datetime.now().date()
        delta2 = ev.created.date() - datetime.now().date()

        if delta1.days < 2 or delta2.days >= 2:
            return redirect('rules')
        
        event_user.delete()

        return redirect('user_reserves')
    

def user_reserves(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    events = Event.objects.filter(id__in=EventUsers.objects.filter(user=customer).values_list('event_id', flat=True))

    context = {'events': events}
    return render(request, 'main/user_reserves.html', context)


def rules(request):
    return render(request, 'main/rules.html')

def api(request):
    return render(request, 'main/api.html')


@api_view(['GET', 'POST'])
def api_events_list(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSearializer(events, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EventSearializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
@api_view(['GET', 'PUT', 'DELETE'])
def api_single_event(request, pk):
    if request.method == 'GET':
        try:
            event = Event.objects.get(id=pk)
        except:
            return Response({})
        serializer = EventSearializer(event)
        return Response(serializer.data)
    elif request.method == 'PUT':
        try:
            event = Event.objects.get(id=pk)
        except:
            return Response({})
        serializer = EventSearializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({})
    elif request.method == 'DELETE':
        try:
            event = Event.objects.get(id=pk)
            event.delete()
        except:
            return Response({})
        return Response({})

