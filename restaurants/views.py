from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View
from django.db.utils import DataError
from django.db.models import Avg

from restaurants.models import Restaurant

class HighListView(View):
    def get(self, request, restaurant_id):
        try:        
            restaurants = Restaurant.objects.all()
            restaurant_list = []
            for restaurant in restaurants:
                restaurant_list.append({
                    "sub_category"      : restaurant.sub_category.name,
                    "category"          : restaurant.sub_category.category.name,
                    "restaurant_name"   : restaurant.name,
                    "address"           : restaurant.address,
                    "rating"            : round(restaurant.review_set.all().aggregate(Avg('rating'))['rating__avg'], 1),
                    "image"             : restaurant.foods.all()[0].images.all()[0].image_url
                })
            restaurant_list = sorted(restaurant_list, key=lambda x:x['rating'], reverse=True)
      
            return JsonResponse({"message":"success", "result":restaurant_list[:5]}, status=200)

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
