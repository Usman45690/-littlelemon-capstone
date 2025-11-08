from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from .models import Menu, Booking
import json

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    return render(request, 'book.html')

def reservations(request):
    return render(request, 'reservations.html')

def menu(request):
    items = Menu.objects.all().order_by('name')
    return render(request, 'menu.html', {'items': items})

def menu_item(request, pk):
    item = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu_item.html', {'item': item})

def bookings(request):
    if request.method == 'GET':
        date = request.GET.get('date', '')
        if date:
            bookings = Booking.objects.filter(reservation_date=date)
        else:
            bookings = Booking.objects.all()
        
        booking_data = []
        for booking in bookings:
            booking_data.append({
                'first_name': booking.first_name,
                'reservation_date': booking.reservation_date.strftime('%Y-%m-%d'),
                'reservation_slot': booking.reservation_slot
            })
        
        return JsonResponse(booking_data, safe=False)

@csrf_exempt
def submit_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            reservation_date = data.get('reservation_date')
            reservation_slot = data.get('reservation_slot')
            
            # Check if booking already exists for this date and slot
            existing_booking = Booking.objects.filter(
                reservation_date=reservation_date,
                reservation_slot=reservation_slot
            ).first()
            
            if existing_booking:
                return JsonResponse({'error': 'This time slot is already booked'}, status=400)
            
            # Create new booking
            booking = Booking.objects.create(
                first_name=first_name,
                reservation_date=reservation_date,
                reservation_slot=reservation_slot
            )
            
            return JsonResponse({
                'message': 'Booking successful',
                'booking': {
                    'first_name': booking.first_name,
                    'reservation_date': booking.reservation_date.strftime('%Y-%m-%d'),
                    'reservation_slot': booking.reservation_slot
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def available_slots(request):
    if request.method == 'GET':
        date = request.GET.get('date', '')
        if date:
            # Get all booked slots for the date
            booked_slots = Booking.objects.filter(reservation_date=date).values_list('reservation_slot', flat=True)
            # Available slots are 10-22 (10am-10pm) excluding booked slots
            all_slots = list(range(10, 23))
            available_slots = [slot for slot in all_slots if slot not in booked_slots]
            return JsonResponse({'available_slots': available_slots})
        else:
            return JsonResponse({'error': 'Date parameter is required'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)