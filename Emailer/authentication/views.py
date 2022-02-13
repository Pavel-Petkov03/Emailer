from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        context = {"me": "I am"}
        return Response(context)
