from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('index.html', views.index, name = 'index'),
    path('login.html', views.login_html, name = 'login_html'),
    path('no_login.html', views.no_login_html, name = 'no_login_html'),
    path('signup.html', views.signup_html, name = 'signup_html'),
    path('main.html', views.main_html, name = 'main_html'),
    path('aux_get_user_info', views.aux_get_user_info, name = 'aux_get_user_info'),
    path('start.html', views.start_html, name = 'start_html'),
    path('orders.html', views.orders_html, name = 'orders_html'),
    path('orders', views.orders, name = 'orders'),
    path('drive_orders.html', views.drive_orders_html, name = 'drive_orders_html'),
    path('drive_orders', views.drive_orders, name = 'drive_orders'),
    path('driver.html', views.driver_html, name = 'driver_html'),
    path('account.html', views.account_html, name = 'account_html'),
    path('not_a_driver.html', views.not_a_driver_html, name = 'not_a_driver_html'),
    path('request_ride.html', views.request_ride_html, name = 'request_ride_html'),
    path('share_search.html', views.share_search_html, name = 'share_search_html'),
    path('drive_search.html', views.drive_search_html, name = 'drive_search_html'),
    path('driver_register.html', views.driver_register_html, name = 'driver_register_html'),
    path('driver_register_with_special_info/<str:real_name>/<str:licence_number>/<int:car_capacity>/<str:car_type>/<str:special_info>', views.driver_register_with_special_info, name = 'driver_register_with_special_info'),
    path('driver_register/<str:real_name>/<str:licence_number>/<int:car_capacity>/<str:car_type>/', views.driver_register, name = 'driver_register'),
    path('driver_search/<str:destination>/<str:date>', views.drive_search, name = 'drive_search'),
    path('confirm/<int:order_id>', views.confirm, name = 'confirm'),
    path('complete/<int:order_id>', views.complete, name = 'complete'),
    path('share_search.html', views.share_search_html, name = 'share_search_html'),
    path('share_search/<str:destination>/<str:earliest_time>/<str:latest_time>/<int:passenger_num>/<str:car_type>/', views.share_search, name = 'share_search'),
    path('share_search/<str:destination>/<str:earliest_time>/<str:latest_time>/<int:passenger_num>/<str:car_type>/<str:special_info>', views.share_search_with_special_info, name = 'share_search_with_special_info'),
    path('join/<int:order_id>/<int:passenger_num>', views.join, name = 'join'),
    path('logout', views.logout, name = 'logout'),
    path('login/<str:username>/<str:password>', views.login, name = 'login'),
    path('signup/<str:username>/<str:password>/<str:email>', views.signup, name = 'signup'),
    path('request/<str:destination>/<str:arrival_time>/<int:passenger_num>/<str:shared>/<str:car_type>/', views.request, name = 'request'),
    path('request/<str:destination>/<str:arrival_time>/<int:passenger_num>/<str:shared>/<str:car_type>/<str:special_info>', views.request_with_special_info, name = 'request_with_special_info'),
    path('edit/<int:order_id>', views.edit, name = 'edit'),
    path('edit_order.html', views.edit_order_html, name = 'edit_order_html'),
    path('aux_get_order_info', views.aux_get_order_info, name = 'aux_get_order_info'),
    path('aux_get_order_info__view', views.aux_get_order_info__view, name = 'aux_get_order_info__view'),
    path('change_order/<int:order_id>/<str:destination>/<str:arrival_time>/<int:passenger_num>/<str:shared>/<str:car_type>/', views.change_order, name = 'change_order'),
    path('change_order/<int:order_id>/<str:destination>/<str:arrival_time>/<int:passenger_num>/<str:shared>/<str:car_type>/<str:special_info>', views.change_order_with_special_info, name = 'change_order_with_special_info'),
    path('aux_get_driver_info', views.aux_get_driver_info, name = 'aux_get_driver_info'),
    path('change_driver_info_with_special_info/<str:real_name>/<str:licence_number>/<int:car_capacity>/<str:car_type>/<str:special_info>', views.change_driver_info_with_special_info, name = 'change_driver_info_with_special_info'),
    path('change_driver_info/<str:real_name>/<str:licence_number>/<int:car_capacity>/<str:car_type>/', views.change_driver_info, name = 'change_driver_info'),
    path('change_user_info/<str:password>/<str:email>', views.change_user_info, name = 'change_user_info'),
    path('view/<int:order_id>', views.view, name = "view"),
    path('open_order_details.html', views.open_order_details_html, name = 'open_order_details_html'),
    path('confirmed_order_details.html', views.confirmed_order_details_html, name = 'confirmed_order_details_html'),
    path('driver_order_details.html', views.driver_order_details_html, name = 'driver_order_details_html'),
    path('cancel/<int:order_id>', views.cancel, name = "cancel"),
]
