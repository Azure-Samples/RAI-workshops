from django.shortcuts import render, redirect
from .models import Comment
from .forms import CommentForm
from .moderate_content import analyze_text


def home(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['text']

            # Call the moderation function
            moderation_message = analyze_text(comment_text)
            if moderation_message == None:  # If the comment triggers moderation
                form.save()
                return redirect('home')
            else:
                form.add_error('text', moderation_message)
    else:
        form = CommentForm()

    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'form': form, 'comments': comments})