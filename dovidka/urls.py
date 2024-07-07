from django.urls import path
from dovidka import views

app_name = 'dovidka'

urlpatterns = [
    path('', views.golovna, name='golovna'),
    path('abonement/', views.abonement, name='abonement'),
    path('administratora/', views.administratora, name='administratora'),
    path('administratsijna_panel/', views.administratsijna_panel, name='administratsijna_panel'),
    path('bronyuvannya_chitachiv/', views.bronyuvannya_chitachiv, name='bronyuvannya_chitachiv'),
    path('chitacha/', views.chitacha, name='chitacha'),
    path('dodavannya_onovlennya_knigi/', views.dodavannya_onovlennya_knigi, name='dodavannya_onovlennya_knigi'),
    path('index/', views.index, name='index'),
    path('informatsiya/', views.informatsiya, name='informatsiya'),
    path('informatsiya_pro_knigi/', views.informatsiya_pro_knigi, name='informatsiya_pro_knigi'),
    path('katalog_knig/', views.katalog_knig, name='katalog_knig'),
    path('koshik/', views.koshik, name='koshik'),
    path('mij_profil/', views.mij_profil, name='mij_profil'),
    path('oformlennya_bronyuvannya/', views.oformlennya_bronyuvannya, name='oformlennya_bronyuvannya'),
    path('pdf_fajli/', views.pdf_fajli, name='pdf_fajli'),
    path('profil_1/', views.profil_1, name='profil_1'),
    path('profil_2/', views.profil_2, name='profil_2'),
    path('profil/', views.profil, name='profil'),
    path('proterminovani_bronyuvannya/', views.proterminovani_bronyuvannya, name='proterminovani_bronyuvannya'),
    path('storinka_bronyuvannya/', views.storinka_bronyuvannya, name='storinka_bronyuvannya'),
    path('storinka_knigi/', views.storinka_knigi, name='storinka_knigi'),
    path('vkhid_re_stratsiya/', views.vkhid_re_stratsiya, name='vkhid_re_stratsiya'),
]
