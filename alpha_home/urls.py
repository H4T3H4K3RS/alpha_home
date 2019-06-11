"""alpha_home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from home import views
from django.views.generic import TemplateView

handler404 = 'home.views.handler404'
handler500 = 'home.views.handler500'
handler403 = 'home.views.handler403'

urlpatterns = [
    # Admin
    url(r'^docs/', include('docs.urls')),
    path('patterns/', TemplateView.as_view(template_name='patterns.html')),
    path('admin/', admin.site.urls, name="admin"),
    path('create_license/', views.create_license, name="create_license"),
    path('signup/set/', views.set_registration, name="set_signup"),
    # END of Admin
    # Landing
    path('', views.index_page, name="main"),
    path('support/', views.ask, name="support"),
    path('help/', views.instruction, name="help"),
    path('products/', views.products, name="products"),
    # END of Landing
    # User auth
    path('login/', views.authorize_page, name="login"),
    path('signup/', views.register_page, name="signup"),
    path('recover/', views.recover, name="recover_email_input"),
    path('recover/confirm/<str:confirm_token_1>/<str:confirm_token_2>/', views.set_password, name="set_password"),
    path('recover/<str:token_1>/<str:token_2>/', views.recover, name="recover_code_input"),
    path('unrecover/', views.recover, name="unrecover"),
    path('unrecover/<str:confirm_token_1>/<str:confirm_token_2>', views.undo_recover, name="unconfirm_recover"),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.logout_page, name="logout"),
    url(r'^accounts/', include('allauth.urls')),
    path('agreement/', views.agreement, name="agreement"),
    # END of user auth
    # Dashboard
    path('panel/<str:panel_type>/', views.panel_page, name="panel_type"),
    path('panel/', views.panel_page, name="panel"),
    path('control_panel/', views.control_panel, name="panel"),
    path('upload_picture/', views.upload_file, name="upload_picture"),
    path('change/house/<int:house_id>', views.change_house, name="change_house"),
    path('add/<int:home>/room/', views.add_room, name="add_room"),
    path('edit/', views.edit_houses, name="edit"),
    path('edit/<int:home>/', views.edit_home, name="edit_home"),
    path('edit/<int:home>/delete/', views.delete_home, name="delete_home"),
    path('edit/room/<int:room>/', views.edit_room, name="edit_room"),
    path('edit/room/<int:room>/delete/', views.delete_room, name="delete_room"),
    path('lamp/room/<int:lamp>/<str:on>/', views.lamp_room, name="lamp_room"),
    path('lamp/house/<str:on>/', views.lamp_house, name="lamp_house"),
    # END of Dashboard
    # Onesignal SDK
    path('manifest.json',
         TemplateView.as_view(template_name='onesignal/manifest.json', content_type='application/json')),
    path('OneSignalSDKWorker.js', TemplateView.as_view(template_name='onesignal/OneSignalSDKWorker.js',
                                                       content_type='application/x-javascript')),
    path('OneSignalSDKUpdaterWorker.js', TemplateView.as_view(template_name='onesignal/OneSignalSDKUpdaterWorker.js',
                                                              content_type='application/x-javascript')),
    # END of Onesignal SDK
]
