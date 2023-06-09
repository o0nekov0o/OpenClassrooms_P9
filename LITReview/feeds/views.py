from django.shortcuts import render


def index(request, *args, **kwargs):
    name = "donald"
    number = 55
    mylist = [3, 35, 6, 7, 9]
    context = {
        "nom": name,
        "numero": number,
        "maliste": mylist
    }
    return render(request, "index.html", context)
