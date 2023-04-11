from app.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view
# from app.models import models
from rest_framework.authtoken.models import Token
# Create your views here.

@api_view(['POST',])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def registration_view(request):

    if request.method == "POST":

        data = {}
           
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account=serializer.save()
            print(account)
            data['response']='Registration Successful'
            data['username']=account.username
            data['eamil']=account.email

            token,created= Token.objects.get_or_create(user=account)
            data['Token'] = str(token)
            
        else:
            serializer.errors
        return Response(data)

