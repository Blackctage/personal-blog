from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import SignUpForm, ProfileUpdateForm, UserForm, UserUpdateForm
from .models import Profile


class SignUpView(generic.View):
    form_class = SignUpForm
    success_url = ''
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('home')

        return render(request, 'accounts/signup.html', {'form': form})


class UserAndProfileView(generic.UpdateView, LoginRequiredMixin):
    form_class = ProfileUpdateForm
    user_form_class = UserUpdateForm
    template_name = 'accounts/profile_update.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserAndProfileView, self).get_context_data(*args, **kwargs)
        context['form'] = self.form_class(self.request.POST)

        context['form2'] = self.user_form_class(self.request.POST)

        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get(self, request, *args, **kwargs):
        context = {}

        context['form'] = self.form_class(initial={'bio': self.request.user.profile.bio,
                                                       'website': self.request.user.profile.website,
                                                       'phone_number': self.request.user.profile.phone_number,
                                                         })

        context['form2'] = self.user_form_class(initial={'username': self.request.user.username,
                                                             'email': self.request.user.email,
                                                             'first_name': self.request.user.first_name,
                                                             'last_name': self.request.user.last_name
                                                             })
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        # get the user instance
        self.object = self.get_object()

        # determine which form is being submitted
        # uses the name of the form's submit button
        if 'form' in request.POST:

            # get the primary form
            form_class = self.get_form_class()
            form_name = 'form'

        else:

            # get the secondary form
            form_class = self.user_form_class
            form_name = 'form2'

        # get the form
        form = self.get_form(form_class)
        u_form = self.user_form_class(request.POST, instance=self.request.user)
        p_form = self.form_class(request.POST, request.FILES, instance=self.request.user.profile)

        # validate
        if form.is_valid() and p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})

    def get_success_url(self):
        return reverse_lazy('profile-detail', args=[self.request.user.username])

    def get_object(self):
        return self.request.user.profile


def authenticate_email(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user

    return None


class LoginView(generic.View):
    form_class = UserForm
    initial = {'key': 'value'}
    success_url = ''
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        if '@' in username_or_email:
            user = authenticate_email(email=username_or_email, password=password)
        else:
            user = authenticate(username=username_or_email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            error = 'The username you entered does not belong to an account. Please check your username and try again.'
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username_or_email, password))

        return render(request, self.template_name, {'form': form, 'error': error})


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            print('Your Profile has been updated!')
            return redirect('')
    else:
        p_form = ProfileUpdateForm(instance=request.user)
        u_form = UserUpdateForm(instance=request.user.profile)

    context = {'p_form': p_form, 'u_form': u_form}
    return render(request, 'accounts/profile_update.html', context)