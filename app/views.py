from app.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from app.models import create_auth_token
from rest_framework.authtoken.models import Token
# Create your views here.



@api_view(['POST'])
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

            token= Token.objects.get_or_create(user=account)
            data['Token'] = str(token)
            
        else:
            serializer.errors
        return Response(data)

