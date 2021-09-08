from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.views import generic
from django.apps import apps


Post = apps.get_model('main', 'Post')
Work = apps.get_model('main', 'Work')


class SearchResultsPostView(generic.ListView):
    model = Post
    template_name = 'search/search_results_post.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query)
        )
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super(SearchResultsPostView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        context['myurl'] = reverse('search_results_post')
        self.request.session['request_type'] = 'Post'

        return context


class SearchResultsUserView(generic.ListView):
    model = User
    template_name = 'search/search_results_user.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        object_list = User.objects.filter(
            Q(username__icontains=query)
        )
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super(SearchResultsUserView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        context['myurl'] = reverse('search_results_user')
        self.request.session['request_type'] = 'User'

        return context


class SearchResultsWorkView(generic.ListView):
    model = Work
    template_name = 'search/search_results_work.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        object_list = Work.objects.filter(
            Q(title__icontains=query)
        )
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super(SearchResultsWorkView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        context['myurl'] = reverse('search_results_work')
        print(reverse('search_results_work'))
        self.request.session['request_type'] = 'Work'

        return context