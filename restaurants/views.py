from django.http        import JsonResponse
from django.views       import View
from restaurants.models import Image, Restaurant

class RestaurantFoodView(View):
    def get(self, request, restaurant_id):
        try:
            foods_queryset = Restaurant.objects.get(id=restaurant_id).foods.all()
            foods          = []
            
            for food_instance in foods_queryset:
                
                food = {
                    "id":food_instance.id,
                    "name":food_instance.name,
                    "price":food_instance.price,
                }
                foods.append(food)
            
            return JsonResponse({"message":"success", "result":foods}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=400)