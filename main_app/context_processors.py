from .forms import SignUpForm, Comment_Form


def SignUpFormGlobal(request):
    return {
        'sign_up_form': SignUpForm()
    }

def CommentFormGlobal(request):
    return {
        'comment_form_global': Comment_Form()
    }
