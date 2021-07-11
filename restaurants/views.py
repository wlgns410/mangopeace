from django.http        import JsonResponse
from django.views       import View
from restaurants.models import Image, Restaurant

class RestaurantFoodView(View):
    def get(self, request, restaurant_id):
        try:
            foods_queryset = Restaurant.objects.get(id=restaurant_id).foods.all()
            foods          = []
            prices         = []

            for food_instance in foods_queryset:
                prices.append(food_instance.price)
                images_queryset = Image.objects.filter(food=food_instance)
                images          = []

                for image_instance in images_queryset:
                    images.append(image_instance.image_url)
  
                food = {
                    "id":food_instance.id,
                    "name":food_instance.name,
                    "price":food_instance.price,
                    "images":images,
                }
                foods.append(food)

            average_price = sum(prices) / len(prices)
            result        = {
                "foods":foods,
                "average_price" : average_price
            }
            
            return JsonResponse({"message":"success", "result":result}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=400)
