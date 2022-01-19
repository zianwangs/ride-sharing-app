from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import User, Driver, Ride, Transaction
from django.core import serializers
from datetime import datetime
from django.db.models import Q
def user_has_logged_in(request):
    return 'username' in request.session
def string_to_datetime(string):
    #unsafe
    if len(string) > 16:
        string = string[:-3]
    return datetime.strptime(string, "%Y-%m-%dT%H:%M")
def string_to_date(string):
    return datetime.strptime(string, "%Y-%m-%d")
def index(request):
    if user_has_logged_in(request):
        return redirect("main.html")
    return render(request, 'index.html')
def login_html(request):
    return render(request, 'login.html')
def signup_html(request):
    return render(request, 'signup.html')
def start_html(request):
    return render(request, 'start.html')
def orders_html(request):
    return render(request, "orders.html")
def drive_orders_html(request):
    return render(request, "drive_orders.html")
def driver_html(request):
    return render(request, "driver.html")
def account_html(request):
    return render(request, "account.html")
def aux_get_user_info(request):
    json = serializers.serialize('json', User.objects.filter(username = request.session['username']))
    return HttpResponse(json)

def signup(request, username, password, email):
    q = User.objects.filter(username = username)
    if len(q) != 0:
        return JsonResponse({'status_code': 1})
    new_user = User(username = username, password = password, email = email, is_driver = False)
    new_user.save()
    return HttpResponse(request)

def login(request, username, password):
    q = User.objects.filter(username = username)
    if len(q) == 0:
        return JsonResponse({'status_code' : 1})
    if q[0].password != password:
        return JsonResponse({'status_code' : 2})
    request.session['username'] = username
    return HttpResponse(request)
def no_login_html(request):
    return render(request, "no_login.html")
def request_ride_html(request):
    return render(request, "request_ride.html")
def share_search_html(request):
    return render(request, "share_search.html")
def drive_search_html(request):
    return render(request, "drive_search.html")
def not_a_driver_html(request):
    return render(request, "not_a_driver.html")
def driver_register_html(request):
    return render(request, "driver_register.html")
def main_html(request):
    if not user_has_logged_in(request):
        return redirect("no_login.html")
    return render(request, "main.html")
def logout(request):
    del request.session['username']
    #del request.session['share_search_car_type']
    #del request.session['share_search_special_info']
    return redirect("index.html")
def orders(request):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    transactions = Transaction.objects.filter(user = User.objects.get(username = request.session['username'])).order_by('-request_time')
    # rides = Ride.objects.filter(id__in = [t.ride.id for t in transactions])
    rides = [t.ride for t in transactions if t.ride.status > 0 and t.ride.status <= 4]
    json = serializers.serialize("json", rides)
    return HttpResponse(json)
def drive_search(request, destination, date):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    user = User.objects.get(username = request.session['username'])
    if not user.is_driver:
        return JsonResponse({"status_code":2})
    driver = Driver.objects.get(user_id = user.id)
    day = string_to_date(date)
    orders = Ride.objects.filter(destination = destination).filter(passenger_num__lte = driver.car_capacity).filter(arrival_time__day = day.day).filter(Q(special_info = "") | Q(special_info = driver.special_info)).filter(Q(car_type = "Unspecified") | Q(car_type = driver.car_type)).exclude(status__gt = 3).exclude(status = 0)
    json = serializers.serialize("json", orders)
    return HttpResponse(json)
def join(request, order_id, passenger_num):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    user = User.objects.get(username = request.session['username'])
    ride = Ride.objects.get(pk = order_id)
    transaction = Transaction(user = user, ride = ride, role = True, request_time = datetime.now(), passenger_num = passenger_num)
    ride.status = 2
    ride.passenger_num += passenger_num
    if ride.car_type == 'Unspecified':
        ride.car_type = request.session['share_search_car_type']
    if ride.special_info == "":
        ride.special_info = request.session['share_search_special_info']
    ride.sharer_num += 1
    ride.save()
    transaction.save()
    return HttpResponse()
def confirm(request, order_id):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    user = User.objects.get(username = request.session['username'])
    if not user.is_driver:
        return JsonResponse({"status_code":2})
    driver = Driver.objects.get(user_id = user.id)
    driver.number_of_incomplete_orders += 1
    driver.save()
    ride = Ride.objects.get(pk = order_id)
    ride.status = 4
    ride.driver = driver
    ride.save()
    return HttpResponse()
def complete(request, order_id):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    user = User.objects.get(username = request.session['username'])
    if not user.is_driver:
        return JsonResponse({"status_code":2})
    driver = Driver.objects.get(user = user)
    driver.number_of_incomplete_orders -= 1
    driver.save()
    ride = Ride.objects.get(pk = order_id)
    ride.status = 5
    ride.save()
    return HttpResponse()
def drive_orders(request):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    user = User.objects.get(username = request.session['username'])
    if not user.is_driver:
        return JsonResponse({"status_code":2})
    driver = Driver.objects.get(user_id = user.id)
    ride = Ride.objects.filter(driver = driver)
    json = serializers.serialize("json", ride)
    return HttpResponse(json)

def driver_register_with_special_info(request, real_name, licence_number, car_capacity, car_type, special_info):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    user = User.objects.get(username = request.session['username'])
    if user.is_driver:
        return JsonResponse({"status_code":2})
    user.is_driver = True
    driver = Driver(user = user, car_type = car_type, car_capacity = car_capacity, real_name = real_name, licence_number = licence_number, special_info = special_info)
    driver.save()
    user.save()
    return HttpResponse()
def driver_register(request, real_name, licence_number, car_capacity, car_type):
    return driver_register_with_special_info(request, real_name, licence_number, car_capacity, car_type, "")
def share_search_with_special_info(request, destination, earliest_time, latest_time, passenger_num, car_type, special_info):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    request.session['share_search_car_type'] = car_type
    request.session['share_search_special_info'] = special_info
    user = User.objects.get(username = request.session['username'])
    earliest_datetime = string_to_datetime(earliest_time)
    latest_datetime = string_to_datetime(latest_time)
    orders = Ride.objects.filter(destination = destination).filter(is_exclusive = False).filter(arrival_time__gte = earliest_datetime).filter(arrival_time__lte = latest_datetime).exclude(status__gt = 2).exclude(status = 0)
    if special_info != "":
        orders = orders.filter(Q(special_info = "") | Q(special_info = special_info))
    if car_type != "Unspecified":
        orders = orders.filter(Q(car_type = "Unspecified") | Q(car_type = car_type))
    self_transactions = Transaction.objects.filter(user = user)
    self_orders = [t.ride for t in self_transactions]
    orders = [o for o in orders if o not in self_orders]
    json = serializers.serialize('json', orders)

    return HttpResponse(json)
def share_search(request, destination, earliest_time, latest_time, passenger_num, car_type):
    return share_search_with_special_info(request, destination, earliest_time, latest_time, passenger_num, car_type, "")
def request_with_special_info(request, destination, arrival_time, passenger_num, shared, car_type, special_info):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    user = User.objects.get(username = request.session['username'])
    ride = Ride(status = 1, passenger_num = passenger_num, destination = destination, arrival_time = string_to_datetime(arrival_time), is_exclusive = (shared == "No"), sharer_num = 0, special_info = special_info, car_type = car_type)
    transaction = Transaction(user = user, ride = ride, role = False, request_time = datetime.now(), passenger_num = passenger_num)
    ride.save()
    transaction.save()
    return JsonResponse({"status_code":0})
def edit(request, order_id):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    request.session['order_to_be_edited'] = order_id
    return HttpResponse()
def edit_order_html(request):
    if not user_has_logged_in(request):
        return redirect("login.html")
    return render(request, "edit_order.html")
def request(request, destination, arrival_time, passenger_num, shared, car_type):
    return request_with_special_info(request, destination, arrival_time, passenger_num, shared, car_type, "")
def aux_get_order_info(request):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    user = User.objects.get(username = request.session['username'])
    order_id = request.session['order_to_be_edited']
    order = Ride.objects.get(pk = order_id)
    order.passenger_num = Transaction.objects.get(ride = order, user = user).passenger_num
    json = serializers.serialize('json', [order,])
    return HttpResponse(json)
def change_order_with_special_info(request, order_id, destination, arrival_time, passenger_num, shared, car_type, special_info):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    print(len(arrival_time))
    user = User.objects.get(username = request.session['username'])
    order = Ride.objects.get(pk = order_id)
    transaction = Transaction.objects.get(user = user, ride = order)
    order.destination = destination
    order.arrival_time = string_to_datetime(arrival_time)
    order.passenger_num += passenger_num - transaction.passenger_num
    order.car_type = car_type
    order.is_exclusive = shared == "No"
    order.special_info = special_info
    transaction.passenger_num = passenger_num
    order.save()
    transaction.save()
    return JsonResponse({"status_code":0})

def change_order(request, order_id, destination, arrival_time, passenger_num, shared, car_type):
    return change_order_with_special_info(request, order_id, destination, arrival_time, passenger_num, shared, car_type, "")

def aux_get_driver_info(request):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    user = User.objects.get(username = request.session['username'])
    if not user.is_driver:
        return JsonResponse({"status_code":2})
    driver = Driver.objects.get(user_id = user.id)
    json = serializers.serialize('json', [driver,])
    return HttpResponse(json)
def change_driver_info_with_special_info(request, real_name, licence_number, car_capacity, car_type, special_info):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    user = User.objects.get(username = request.session['username'])
    if not user.is_driver:
        return JsonResponse({"status_code":2})
    driver = Driver.objects.get(user = user)
    driver.real_name = real_name
    driver.licence_number = licence_number
    driver.car_capacity = car_capacity
    driver.car_type = car_type
    driver.special_info = special_info
    driver.save()
    return HttpResponse()
def change_driver_info(request, real_name, licence_number, car_capacity, car_type):
    return change_driver_info_with_special_info(request, real_name, licence_number, car_capacity, car_type, "")
def change_user_info(request, password, email):
    if not user_has_logged_in(request):
        return JsonResponse({"status_code":1})
    user = User.objects.get(username = request.session['username'])
    user.password = password
    user.email = email
    user.save()
    return HttpResponse()
# Create your views here.
