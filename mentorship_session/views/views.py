from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.mixins.views import ProfileRequiredMixin
from core.models import FreelancerProfile
from ..models import MentorshipSession
from ..forms.mentorship_form import MentorshipSessionCreateForm, MentorshipSessionUpdateForm
from ..repositories.mentorship_repository import MentorshipRepository
from ..services.mentorship_service import MentorshipService

mentorship_service = MentorshipService(repository=MentorshipRepository())

class MentorshipSessionListView(ListView):
    model = MentorshipSession
    template_name = "mentorship_session/mentorship_sessions_list.html"
    context_object_name = "sessions"

    def get_queryset(self):
        return MentorshipSession.objects.all()

class MentorshipSessionFreelancerListView(ProfileRequiredMixin, ListView):
    required_profile = 'freelancer'
    model = MentorshipSession
    template_name = "mentorship_session/freelancer_mentorship_session.html"
    context_object_name = "sessions"

    def get_queryset(self):
        freelancer = get_object_or_404(FreelancerProfile, pk=self.kwargs["freelancer_id"])
        return mentorship_service.list_mentor_sessions(mentor_id=freelancer.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        freelancer = get_object_or_404(FreelancerProfile, pk=self.kwargs["freelancer_id"])
        context["freelancer"] = freelancer
        context["is_freelancer"] = hasattr(self.request.user, 'freelancer_profile')
        return context

class MentorshipSessionCreateView(ProfileRequiredMixin, CreateView):
    required_profile = 'freelancer'
    model = MentorshipSession
    form_class = MentorshipSessionCreateForm
    template_name = "mentorship_session/create_mentorship_session.html"

    def form_valid(self, form):
        freelancer = self.request.user.freelancer_profile

        mentorship_service.create_session(
            topic=form.cleaned_data['topic'],
            start_time=form.cleaned_data['start_time'],
            duration_minutes=form.cleaned_data['duration_minutes'], 
            mentor_id=freelancer.id, 
        )
        return redirect(
            reverse(
                'mentorship_session:sessions_freelancer_list',
                kwargs={'freelancer_id': self.request.user.freelancer_profile.id}
            )
        )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context

class MentorshipSessionUpdateView(ProfileRequiredMixin, UpdateView):
    required_profile = 'freelancer'
    model = MentorshipSession
    form_class = MentorshipSessionUpdateForm
    template_name = "mentorship_session/create_mentorship_session.html"

    def form_valid(self, form):
        session = self.get_object()
        mentorship_service.update_session(
            session_id=session.id,
            topic=form.cleaned_data['topic'],
            start_time=form.cleaned_data['start_time'],
            duration_minutes=form.cleaned_data['duration_minutes'],
            mentor_id=session.mentor.id,
        )
        return redirect(
            reverse(
                'mentorship_session:sessions_freelancer_list',
                kwargs={'freelancer_id': self.request.user.freelancer_profile.id}
            )
        )
        
    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context



class MentorshipSessionDeleteView(ProfileRequiredMixin, DeleteView):
    required_profile = 'freelancer'
    model = MentorshipSession
    template_name = "mentorship_session/mentorship_session_confirm_delete.html"
    success_url = reverse_lazy("mentorship_session:session_list")

    def delete(self, request, *args, **kwargs):
        session = self.get_object()
        mentorship_service.delete_session(session.id)
        return super().delete(request, *args, **kwargs)
