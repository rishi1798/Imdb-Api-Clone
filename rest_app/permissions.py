from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    '''
    So here we are checking if the incoming method is get or read-only
    we are allowing every type of user to perform safe action i.e user can
    only read the data and if the incoming method is not safe method i.e. 
    method is PUT,DELETE or POST we are allowing only staff user to perform 
    unsafe action i.e user can perform create,update or delete operation.
    '''

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)


class IsReviewUserOrReadOnly(permissions.BasePermission):
    
    '''
    so here only that user will be allowed to perform unsafe action
    who has written review so if 'John' has wriiten a review only he 
    and admin will be able to edit it and all other user can read it 
    only 
    '''

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user==request.user or request.user.is_staff