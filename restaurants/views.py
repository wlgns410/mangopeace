from django.http import JsonResponse
from django.views import View
from django.db.models import Avg

from restaurants.models import Restaurant

class PopularRestaurantView(View):
    def get(self, request):
        try:
            restaurants = Restaurant.objects.annotate(average_rating=Avg("review__rating")).order_by("-average_rating")
            
            restaurant_list = []
            
            for restaurant in restaurants: 
                restaurant_list.append({
                    "sub_category"      : restaurant.sub_category.name,
                    "category"          : restaurant.sub_category.category.name,
                    "restaurant_name"   : restaurant.name,
                    "address"           : restaurant.address,
                    "rating"            : round(restaurant.average_rating, 1),
                    "image"             : restaurant.foods.all()[0].images.all()[0].image_url,
                    "restaurant_id"     : restaurant.id
                })

            return JsonResponse({"message":"success", "result":restaurant_list[:5]}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)