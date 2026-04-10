from django.shortcuts import render

def not_found_view(request):
    """
    Renders the 404 page.
    """
    return render(request, 'landing/not_found.html')
