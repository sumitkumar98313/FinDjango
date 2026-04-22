from django.urls import path
from . import views

# all url patterns for the tracker app
urlpatterns = [

    # home page
    path('', views.home, name='home'),

    # auth urls
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # transaction urls
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('transactions/<int:tx_id>/delete/', views.delete_transaction, name='delete_transaction'),

    # profile and account
    path('profile/', views.profile, name='profile'),
    path('delete-account/', views.delete_account, name='delete_account'),

    # export and reports
    path('export/', views.export_csv, name='export_csv'),
    path('report/', views.monthly_report, name='monthly_report'),

]

# custom error pages
handler404 = 'tracker.views.error_404'
handler500 = 'tracker.views.error_500'
