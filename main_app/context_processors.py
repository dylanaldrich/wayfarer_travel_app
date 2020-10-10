from .forms import SignUpForm


def SignUpFormGlobal(request):
    return {
        'sign_up_form': SignUpForm()
    }
