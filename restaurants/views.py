from django.http        import JsonResponse
from django.views       import View

from users.models       import User
from restaurants.models import Restaurant

class RestaurantDetailView(View):
    def get(self, request, restaurant_id):
        try:
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)
            fake_user_instance  = User.objects.get(id=1)
            is_wished           = fake_user_instance.wishlist_restaurants.filter(id=restaurant_id).exists()
            reviews_queryset    = Restaurant.objects.get(id=restaurant_id).review_set.all()
            average_rating      = reviews_queryset.aggregate(Avg("rating"))["rating__avg"]
            review_count        = Restaurant.objects.get(id=restaurant_id).review_set.all().count()
            result              = {
            "id":restaurant_instance.id,
            "sub_category": restaurant_instance.sub_category.name,
            "name": restaurant_instance.name,
            "address": restaurant_instance.address,
            "phone_number": restaurant_instance.phone_number,
            "coordinate": restaurant_instance.coordinate,
            "open_time": restaurant_instance.open_time,
            "updated_at": restaurant_instance.updated_at,
            "is_wished" : is_wished,
            "review_count" : review_count,
            "average_rating" : average_rating,
        }

            return JsonResponse({"message":"success", "result":result}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=400)