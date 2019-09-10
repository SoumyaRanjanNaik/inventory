from django.urls import path

from inventory import views

app_name = "inventory"


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path("restock/", views.restock_page, name="restock"),
    path("sale/", views.sale_page, name="sale"),
    path("bill/", views.sale, name="bill"),
    path('inv/', views.manager, name='inv'),
    path("new/", views.newproduct, name="new"),
    path('add/', views.newproductadd, name='add'),
    path("viewstock/", views.stockview, name="viewstock"),
    path('reportrequest/', views.report_req, name='report_req'),
]
