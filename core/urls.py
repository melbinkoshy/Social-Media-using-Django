from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index' ),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('signin',views.signout,name='signout'),
    path('settings',views.settings,name='settings')
]