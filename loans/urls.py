from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.apply_loan, name='apply_loan'),
    path('my/', views.my_loans, name='my_loans'),
    path('detail/<uuid:pk>/', views.loan_detail, name='loan_detail'),
    path('all/', views.all_loans, name='all_loans'),
    path('review/<uuid:pk>/', views.review_loan, name='review_loan'),
    path('emi-calculator/', views.emi_calculator, name='emi_calculator'),
]
