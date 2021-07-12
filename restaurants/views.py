from django.http        import JsonResponse
from django.views       import View

from users.models       import User
from restaurants.models import Restaurant

class RestaurantDetailView(View):
    def get(self, request, restaurant_id):
        try:
            restaurant     = Restaurant.objects.get(id=restaurant_id)
            user           = request.user
            is_wished      = user.wishlist_restaurants.filter(id=restaurant_id).exists() if request.user
            reviews        = Restaurant.objects.get(id=restaurant_id).review_set.all()
            average_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
            review_count   = Restaurant.objects.get(id=restaurant_id).review_set.all().count()
            result         = {
            "id":restaurant.id,
            "sub_category": restaurant.sub_category.name,
            "name": restaurant.name,
            "address": restaurant.address,
            "phone_number": restaurant.phone_number,
            "coordinate": restaurant.coordinate,
            "open_time": restaurant.open_time,
            "updated_at": restaurant.updated_at,
            "is_wished" : is_wished,
            "review_count" : review_count,
            "average_rating" : average_rating,
        }

            return JsonResponse({"message":"success", "result":result}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=400)