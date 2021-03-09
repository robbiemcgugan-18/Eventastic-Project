from django.shortcuts import render

def index(request):
    context_dict = {'name': 'Robbie McGugan'}

    return render(request, 'team_10e_app/index.html', context=context_dict)
