from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_app.permissions import ReviewUserOrReadOnly,AdminOrReadOnly

from .models import WatchList,StreamPlatform,Review
from .serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer

# Create your views here.

# views using ModelViewSet

# class WatchListModelViewSet(ModelViewSet):
#     queryset=WatchList.objects.all()
#     serializer_class=WatchListSerializer    

# Views using viewset class
class WatchListViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]

    def list(self,request):
        watchlist=WatchList.objects.all()
        serializer=WatchListSerializer(watchlist,many=True,context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self,request,pk):
        try:
            watchlist=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':"movie not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=WatchListSerializer(watchlist)
        return Response(serializer.data)

    def create(self,request):
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        watchlist=WatchList.objects.get(pk=pk)
        watchlist.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)
        
# Class based Views

class WatchListAV(APIView):
    
    def get(self,request):
        movies=WatchList.objects.all()
        
        serializer=WatchListSerializer(movies,many=True,context={'request': request})

        return Response(serializer.data)

    def post(self,request):
        serializer=WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class WatchListDetailsAV(APIView):
    def put(self,request,pk):
        try:
            movies=WatchList.objects.get(pk=pk)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=WatchListSerializer(movies,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"error":"Data invalid format"},status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk):
        try:
            movie=WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error':"movie not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=WatchListSerializer(movie,context={'request': request})

        return Response(serializer.data)

    def delete(self,request,pk):
        movie=WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)
    


class StreamListAV(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        try:
            platform=StreamPlatform.objects.all()
        except StreamPlatform.DoesNotExist:
            return Response({"error":"Platform not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=StreamPlatformSerializer(platform,many=True,context={'request': request})
        # print(request)
        return Response(serializer.data)


    def post(self,request):
        serializer=StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"error":"Invalid data"},status=status.HTTP_400_BAD_REQUEST)
    
class StreamDetailsAV(APIView):
    def get(self,request,pk):
        try:
            platform=StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"error":"platform not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=StreamPlatformSerializer(platform,context={'request': request})
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            platform=StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({"error":"platform not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=StreamPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"error":"Data invalid format"},status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk):
        platform=StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response({"error":"Data deleted"},status=status.HTTP_404_NOT_FOUND)


# Using Generic api view

class ReviewList(generics.ListAPIView):
    
    '''
    All the review for a particular watchlist
    '''

    # queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        pk=self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]


class ReviewCreate(generics.CreateAPIView):

    '''
    so only the user who have not written a review will be
    allowed to create a review and a user can not create a
    review twice.
    '''


    # queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        
        pk=self.kwargs.get('pk')
        watchlist=WatchList.objects.get(pk=pk)
        review_user=self.request.user
        user=Review.objects.filter(watchlist=watchlist,review_user=review_user)

        if user.exists():
            raise ValidationError("U have already given review")
        
        if watchlist.avg_rating == 0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating=watchlist.number_rating+1

        watchlist.save()

        serializer.save(watchlist=watchlist,review_user=review_user)    
        


# Using mixins

# class ReviewList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class=ReviewSerializer

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
#     queryset=Review.objects.all()
#     serializer_class =ReviewSerializer

#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request,*args,**kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request,*args,**kwargs)
    

    








# Function based view
# @api_view(['GET','POST'])
# def home(request):
#     if request.method == "GET":
#         movie=Movie.objects.all()
#         serializer=MovieSerializer(movie,many=True)

#         return Response(serializer.data)
    
#     if request.method == "POST":
#         serializer=MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def update(request,pk):
#     if request.method == "GET":
#         try:
#             movie=Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error':"movie not found"},status=status.HTTP_404_NOT_FOUND)
#         serializer=MovieSerializer(movie)

#         return Response(serializer.data)

#     if request.method == "PUT":
#         try:
#             movie=Movie.objects.get(pk=pk)
#         except:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer=MovieSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response({"error":"Data invalid format"},status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == "DELETE":
#         movie=Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_404_NOT_FOUND)

