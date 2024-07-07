from django.shortcuts import render

def golovna(request):
    return render(request, 'dovidka/golovna.html')

def abonement(request):
    return render(request, 'dovidka/abonement.html')

def administratora(request):
    return render(request, 'dovidka/administratora.html')

def administratsijna_panel(request):
    return render(request, 'dovidka/administratsijna_panel.html')

def bronyuvannya_chitachiv(request):
    return render(request, 'dovidka/bronyuvannya_chitachiv.html')

def chitacha(request):
    return render(request, 'dovidka/chitacha.html')

def dodavannya_onovlennya_knigi(request):
    return render(request, 'dovidka/dodavannya_onovlennya_informatsii_knigi.html')

def index(request):
    return render(request, 'dovidka/index.html')

def informatsiya(request):
    return render(request, 'dovidka/informatsiya.html')

def informatsiya_pro_knigi(request):
    return render(request, 'dovidka/informatsiya_pro_knigi.html')

def katalog_knig(request):
    return render(request, 'dovidka/katalog_knig.html')

def koshik(request):
    return render(request, 'dovidka/koshik.html')

def mij_profil(request):
    return render(request, 'dovidka/mij_profil.html')

def oformlennya_bronyuvannya(request):
    return render(request, 'dovidka/oformlennya_bronyuvannya.html')

def pdf_fajli(request):
    return render(request, 'dovidka/pdf_fajli.html')

def profil_1(request):
    return render(request, 'dovidka/profil_1.html')

def profil_2(request):
    return render(request, 'dovidka/profil_2.html')

def profil(request):
    return render(request, 'dovidka/profil.html')

def proterminovani_bronyuvannya(request):
    return render(request, 'dovidka/proterminovani_bronyuvannya.html')

def storinka_bronyuvannya(request):
    return render(request, 'dovidka/storinka_bronyuvannya.html')

def storinka_knigi(request):
    return render(request, 'dovidka/storinka_knigi.html')

def vkhid_re_stratsiya(request):
    return render(request, 'dovidka/vkhid_re_stratsiya.html')

