from django.urls import path
from sales.views import listcustomers
urlpatterns = [
    #    path("admin/", admin.site.urls),
    path('customers/',listcustomers)
]