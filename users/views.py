from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import WorkerProfile

@login_required
def admin_dashboard(request):
    if request.user.is_admin:
        return render(request, 'admin_dashboard.html')
    else:
        return render(request, 'not_authorized.html')


@login_required
def worker_dashboard(request):
    user = request.user
    
    if not hasattr(user, 'workerprofile'):
        # Create a WorkerProfile if it doesn't exist
        WorkerProfile.objects.create(user=user)
    
    # Now access the worker profile
    worker_profile = user.workerprofile
    
    context = {
        'can_enter_raw_products': worker_profile.can_enter_raw_products,
        'can_add_new_orders': worker_profile.can_add_new_orders,
    }
    
    return render(request, 'worker_dashboard.html', context)
    
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        if self.request.user.is_admin:
            return reverse_lazy('admin_dashboard')
        else:
            return reverse_lazy('worker_dashboard')
        
