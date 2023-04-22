from django.urls import path
from .  import views

urlpatterns = [
   # path('', views.main, name='main'),
    path('frm/',views.employee_form,name ='employee_insert'),
    path('<int:id>/',views.employee_form,name= 'update'),
    path('LogIn/',views.auth_login,name= 'auth_login'),
    path('pupdate/',views.pupdate,name= 'pupdate'),
    path('LogOut/',views.lgout,name= 'lgout'),
    path('Home/',views.home,name= 'home'),
    path('SignUp/',views.signup,name= 'signup'),
    path('fpass/',views.fpass,name= 'fpass'),
    path('list/',views.employee_list,name= 'employee_list'),
    path('li/',views.li,name= 'li'),
    path('uppdf/',views.uppdf,name= 'uppdf'),
    path('pdfview/',views.pdfview,name= 'pdfview'),
    path('delete/<int:id>/',views.employee_delete,name='employee_delete'),
    #path('members/',views.members, name='members'),
    #path('members/details/<int:id>', views.details, name='details'),
]