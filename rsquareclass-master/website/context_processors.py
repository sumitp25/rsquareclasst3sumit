from .models import Branch

def user_processor(request):
    context = {}
    if request.user.is_authenticated:
        context["user"] = request.user
        if request.user.is_owner():
            context["branches"] = Branch.objects.all()
    else:
        context["user"] = None
    return context