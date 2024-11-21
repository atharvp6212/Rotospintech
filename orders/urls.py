from django.urls import path
from . import views
from .views import enter_new_order, select_sub_part

urlpatterns = [
    path('enter-new-order/<str:sub_part_ids>/', views.enter_new_order, name='enter_new_order'),  # Accepts comma-separated IDs
    path('generate-reports/', views.generate_reports, name='generate_reports'),
    path('select-sub-part/', select_sub_part, name='select_sub_part'),
    path('review-order/', views.review_order, name='review_order'),
]
