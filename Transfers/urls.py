from django.contrib import admin
from django.urls import path, include

from mainapp.views import *

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="TopFootballTransfers API",
      default_version='v1',
      description="Football Transfers uchun API",
      contact=openapi.Contact(email="akmaljonyoqubov088@gmail.com"),
      license=openapi.License(name="Akamljon Yoqubov"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0)),

    path('clubs/', ClubsAPIView.as_view()),
    path('players/', PlayersAPIView.as_view()),
    path('clubs/<str:country>/', ClubsCountryAPIView.as_view()),
    path('season/<str:n>/', SeasonAPIView.as_view()),
    path('club_players/<str:club>/', ClubPlayersAPIView.as_view()),
    path('U20-players/', U20PlayersAPIView.as_view()),
    path('latest-transfers/', LatestTransfersAPIView.as_view()),
    path('predictions/', AccuratePredictions150APIView.as_view()),
    path('record_transfers/', TransfersRecordsAPIView.as_view()),
    path('top-clubs-by-expenditure/', TopClubsExpenditureAPIView.as_view()),
]
