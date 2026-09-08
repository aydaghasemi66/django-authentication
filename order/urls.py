from django.urls import path
from .views import (
    OrderListView, OrderDetailView, AddItemView,
    CheckoutView, MyEnrollmentsView,
)

urlpatterns = [
    path("", OrderListView.as_view(), name="order-list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("add-item/", AddItemView.as_view(), name="order-add-item"),
    path("<int:pk>/checkout/", CheckoutView.as_view(), name="order-checkout"),
    path("my-enrollments/", MyEnrollmentsView.as_view(), name="my-enrollments"),
]