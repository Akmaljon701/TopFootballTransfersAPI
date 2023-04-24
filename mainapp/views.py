from django.db.models import F
from django.db.models.functions import Abs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.db.models import F, IntegerField, ExpressionWrapper

from .models import *
from .serializers import *

class ClubsAPIView(APIView):
    def get(self, request):
        clubs = Club.objects.all()
        serializer = ClubSerializer(clubs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LatestTransfersAPIView(APIView):
    def get(self, request):
        transfers = Transfer.objects.filter(mavsum=Hozirgi_mavsum.objects.all()[0])
        serializer = TransferSerializer(transfers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PlayersAPIView(APIView):
    def get(self, request):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClubsCountryAPIView(APIView): # clubs/<str:country>/
    def get(self, request, country):
        clubs = Club.objects.filter(davlat=country)
        serializer = ClubSerializer(clubs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class U20PlayersAPIView(APIView):
    def get(self, request):
        from datetime import date, timedelta
        bugun = date.today()
        boshi = bugun - timedelta(days=7295)
        players = Player.objects.filter(t_yil__range=[boshi, bugun])
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SeasonAPIView(APIView): # season/<str:n>/
    def get(self, request, n):
        season = n + '-' + str(int(n)+1)  # "21-22"
        season_transfers = Transfer.objects.filter(mavsum=season)
        serializer = TransferSerializer(season_transfers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClubPlayersAPIView(APIView):
    def get(self, request, club): # club_players/<str:club>
        club_playes = Player.objects.filter(club__nom=club)
        serializer = PlayerSerializer(club_playes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AccuratePredictions150APIView(APIView):
    def get(self, request):
        players = Player.objects.all()[:150]

        divergence_percent = ExpressionWrapper(
            Abs(F('narxi') - F('tax_narx')) * 100 / F('narxi'),
            output_field=IntegerField()
        )
        transfers = Transfer.objects.filter(player__in=players).annotate(
            divergence_percent=divergence_percent
        ).order_by('divergence_percent')

        serializer = TransferSerializer(transfers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TransfersRecordsAPIView(APIView):
    def get(self, request):
        transfers = Transfer.objects.order_by('-narxi')[:100]
        serializer = TransferSerializer(transfers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TopClubsExpenditureAPIView(generics.ListAPIView):
    queryset = Club.objects.annotate(transfer_narxi=models.Sum('sotuvlari__narxi')).order_by('-transfer_narxi')
    serializer_class = ClubSerializer