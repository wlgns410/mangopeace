from django.http        import JsonResponse
from django.views       import View
from restaurants.models import Restaurant

class RestaurantFoodView(View):
    def get(self, request, restaurant_id):
        try:
            foods_queryset = Restaurant.objects.get(id=restaurant_id).foods.all()
            foods          = []
            prices         = []

            for food_instance in foods_queryset:
                food = {
                    "id":food_instance.id,
                    "name":food_instance.name,
                }
                foods.append(food)
                prices.append(food_instance.price)

            average_price = sum(prices) / len(prices)
            result        = {
                "foods":foods,
                "average_price" : average_price
            }
            
            return JsonResponse({"message":"success", "result":result}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=400)
