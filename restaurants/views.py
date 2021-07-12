from django.http                 import JsonResponse
from django.views                import View
from django.db.models.aggregates import Avg

from restaurants.models          import Image, Restaurant

class RestaurantFoodView(View):
    def get(self, request, restaurant_id):
        try:
            foods         = Restaurant.objects.get(id=restaurant_id).foods.all()
            average_price = foods.aggregate(Avg("price"))["price__avg"]
            foods_list    = []

            for f in foods:
                images = Image.objects.filter(food=f)
                images_list = []

                for image in images:
                    images_list.append(image.image_url)

                food = {
                    "id":f.id,
                    "name":f.name,
                    "price":f.price,
                    "images":images_list,
                }
                foods_list.append(food)

            result = {
                "foods"         : foods_list,
                "average_price" : average_price
            }
            
            return JsonResponse({"message":"success", "result":result}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)