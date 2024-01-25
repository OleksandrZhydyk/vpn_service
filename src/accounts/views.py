from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView

from accounts.forms import LoginForm, RegistrateForm, ProfileForm
from accounts.models import Profile


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def get_success_url(self):
        return reverse_lazy("user_profile", kwargs={"pk": self.request.user.profile.pk})


class LogoutUser(LoginRequiredMixin, LogoutView):
    success_url = reverse_lazy("login")


class RegisterUser(CreateView):
    form_class = RegistrateForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")


class PageNotFoundView(TemplateView):
    template_name = "accounts/404.html"
    extra_context = {"title": "Page not found"}


class UnauthorizedView(TemplateView):
    template_name = "accounts/forbidden.html"
    extra_context = {"title": "Forbidden"}


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "accounts/user_profile.html"
    raise_exception = True
    context_object_name = "profile"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "accounts/update_user_profile.html"
    form_class = ProfileForm
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy("user_profile", kwargs={"pk": self.request.user.profile.pk})

# @login_required
# def update_profile(request, **kwargs):
#     profile = get_object_or_404(Profile, pk=kwargs.get('pk'))
#     if request.method == "POST":
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("index"))
#     else:
#         form = ProfileForm(instance=profile)
#     return render(request, template_name="accounts/profile.html", context={"form": form})
