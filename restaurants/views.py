from django.http        import JsonResponse
from django.views       import View

from users.utils        import ConfirmUser
from restaurants.models import Restaurant

class WishListView(View):
    @ConfirmUser
    def post(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)

            if request.user.wishlist_restaurants.filter(id=restaurant_id).exists():
                return JsonResponse({"message":"WISHLIST_ALREADY_EXISTS"}, status=400)

            request.user.wishlist_restaurants.add(restaurant)
            
            return JsonResponse({"message":"success"}, status=201)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)   
        
    @ConfirmUser
    def delete(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)

            if not request.user.wishlist_restaurants.filter(id=restaurant_id).exists():
                return JsonResponse({"message":"WISHLIST_NOT_EXISTS"}, status=404)
           
            request.user.wishlist_restaurants.remove(restaurant)

            return JsonResponse({"message":"success"}, status=204)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)