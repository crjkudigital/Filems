from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django import forms
from django.shortcuts import redirect
from .models import UserProfile
from django.contrib.auth import logout
from django.views import View


User = get_user_model()

# UserProfile Views
class UserProfileCreateView(LoginRequiredMixin, CreateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'email', 'phone_number']
    template_name = 'userprofile_form.html'
    success_url = reverse_lazy('profile-detail')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'userprofile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'email', 'phone_number']
    template_name = 'userprofile_form.html'
    success_url = reverse_lazy('profile-detail')

    def get_object(self):
        return self.request.user.profile

class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserProfile
    template_name = 'userprofile_confirm_delete.html'
    success_url = reverse_lazy('profile-create')

    def get_object(self):
        return self.request.user.profile



# Signup Form
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Signup View
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('profile-create')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

# Login View (using Django built-in LoginView)
class CustomLoginView(LoginView):
    template_name = 'login.html'

# Logout View (optional)
# class CustomLogoutView(LogoutView):
#next_page = reverse_lazy('login')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')  # or wherever you want

# UserProfile Views

class UserProfileCreateView(LoginRequiredMixin, CreateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'email', 'phone_number']
    template_name = 'userprofile_form.html'
    success_url = reverse_lazy('profile-detail')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'userprofile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.profile

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'email', 'phone_number']
    template_name = 'userprofile_form.html'
    success_url = reverse_lazy('profile-detail')

    def get_object(self):
        return self.request.user.profile

class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserProfile
    template_name = 'userprofile_confirm_delete.html'
    success_url = reverse_lazy('profile-create')

    def get_object(self):
        return self.request.user.profile