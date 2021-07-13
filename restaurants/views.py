from django.http        import JsonResponse
from django.views       import View

from restaurants.models import Food, Restaurant

class RestaurantFoodsView(View):
    def get(self, request, restaurant_id):
        try:
            foods      = Food.objects.filter(restaurant_id=restaurant_id)
            foods_list = [{"id":f.id, "name":f.name, "price":f.price, "images":[i.image_url for i in f.images.all()]} for f in foods]
            result     = {"foods" : foods_list}
            
            return JsonResponse({"message":"success", "result":result}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)