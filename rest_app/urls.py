from django.urls  import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .views import WatchListViewSet

router=DefaultRouter()
router.register("",WatchListViewSet,basename="list")

urlpatterns = [
    # path("list/",views.WatchListAV.as_view()),
    # path("<int:pk>/",views.WatchListDetailsAV.as_view(),name="watchlist-detail"),
    path("",include(router.urls)),
    path("stream/",views.StreamListAV.as_view()),
    path("stream/<int:pk>/",views.StreamDetailsAV.as_view(),name="streamplatform-details"),

    path("<int:pk>/review/",views.ReviewList.as_view(),name='reviewlist'),
    path("review/<int:pk>/",views.ReviewDetail.as_view(),name='reviewdetail'),
    path("<int:pk>/review-create/",views.ReviewCreate.as_view())
    # path("review/",views.ReviewList.as_view(),name='reviewlist'),
    # path("review/<int:pk>",views.ReviewDetail.as_view(),name='reviewdetail'),
]

