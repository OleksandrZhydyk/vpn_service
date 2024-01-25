from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView
from django.shortcuts import get_object_or_404
from requests import Response

from requester import Requester
from sites.forms import SiteForm
from sites.models import Site

from sites.url_modifiers import modify_links_in_response, build_full_origin_link
from utils import bytes_to_megabytes


class GetStatistics(LoginRequiredMixin, ListView):
    model = Site
    template_name = "sites/statistics.html"
    context_object_name = "statistics"
    extra_context = {"title": "Sites Statistics"}
    raise_exception = True

    def get_queryset(self):
        return Site.objects.filter(user=self.request.user)


class CreateSiteView(LoginRequiredMixin, CreateView):
    model = Site
    template_name = "sites/create_site.html"
    form_class = SiteForm
    success_url = reverse_lazy("get_statistics")
    raise_exception = True

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteSiteView(LoginRequiredMixin, DeleteView):
    model = Site
    template_name = "sites/delete_site.html"
    success_url = reverse_lazy("get_statistics")
    raise_exception = True
    context_object_name = "site"


class ProxyView(LoginRequiredMixin, View, Requester):

    def get(self, request, site_name, original_link):
        server_domain = f"{request.scheme}://{request.get_host()}"

        site = get_object_or_404(Site, name=site_name, user=request.user)

        original_link = build_full_origin_link(site.url, original_link)

        response = self.get_request(original_link)

        content_type = response.headers.get("content-type")
        received_content_length = int(response.headers.get("Content-Length", 0))
        self._update_site_statistic(site, received_content_length)

        # If response does not have links just proxy it
        if content_type.startswith("image") or content_type in ["application/octet-stream", "application/pdf",
                                                                "application/zip"]:
            return HttpResponse(content=response.content, content_type=content_type)

        modified_content = modify_links_in_response(
            response=response,
            server_domain=server_domain,
            site_name=site_name,
            site_full_domain=site.url
        )
        proxy_response = HttpResponse(content=modified_content, content_type=content_type)
        return self._set_cookie_to_response(response, proxy_response)

    def post(self, request, site_name, original_link):
        server_domain = f"{request.scheme}://{request.get_host()}"

        site = get_object_or_404(Site, name=site_name, user=request.user)

        original_link = build_full_origin_link(site.url, original_link)

        response = self.post_request(original_link, request.body)

        content_type = response.headers.get("content-type")
        received_content_length = int(response.headers.get("Content-Length", 0))
        upload_content_length = request.META.get("CONTENT_LENGTH", 0)
        self._update_site_statistic(site, received_content_length, upload_content_length)

        # If response does not have links just proxy it
        if content_type.startswith("image") or content_type in ["application/octet-stream", "application/pdf",
                                                                "application/zip"]:
            return HttpResponse(content=response.content, content_type=content_type)

        modified_content = modify_links_in_response(
            response=response,
            server_domain=server_domain,
            site_name=site_name,
            site_full_domain=site.url
        )
        proxy_response = HttpResponse(content=modified_content, content_type=content_type)
        return self._set_cookie_to_response(response, proxy_response)

    def _update_site_statistic(self, site: Site, received_content_length: int, upload_content_length: int = 0) -> None:
        site.moves_by_pages += 1
        if upload_content_length:
            total_upload_size = site.upload_data_size + bytes_to_megabytes(upload_content_length)
            site.upload_data_size = round(total_upload_size, 2)
        total_received_size = site.received_data_size + bytes_to_megabytes(received_content_length)
        site.received_data_size = round(total_received_size, 2)
        site.save()

    def _set_cookie_to_response(self, source_response: Response, proxy_response: HttpResponse) -> HttpResponse:
        for cookie in source_response.cookies:
            proxy_response.set_cookie(
                key=cookie.name,
                value=cookie.value,
                expires=cookie.expires,
                path=cookie.path,
                domain=cookie.domain,
                secure=cookie.secure
            )
        return proxy_response
