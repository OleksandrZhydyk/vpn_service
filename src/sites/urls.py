from django.urls import path, register_converter

from sites.converters import RawConverter
from sites.views import GetStatistics, CreateSiteView, DeleteSiteView, ProxyView


register_converter(RawConverter, 'raw')

urlpatterns = [
    path("", GetStatistics.as_view(), name="get_statistics"),
    path("create_site/", CreateSiteView.as_view(), name="create_site"),
    path("delete_site/<int:pk>/", DeleteSiteView.as_view(), name="delete_site"),
    path("<str:site_name>/<raw:original_link>/", ProxyView.as_view())
]
