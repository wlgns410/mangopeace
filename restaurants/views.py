import json

from django.http        import JsonResponse
from django.views       import View
from django.db.utils    import DataError
from django.db.models   import Avg
from django.utils       import timezone

from users.utils        import ConfirmUser
from users.models       import Review
from restaurants.models import Restaurant

class PopularRestaurantView(View):
    def get(self, request):
        try:
            dict_sort={
                "average_rating" : "-filtering"
            }
            filtering = request.GET.get("filtering", None)
            restaurants = Restaurant.objects.annotate(filtering=Avg("review__rating")).order_by(dict_sort[filtering])
            
            restaurant_list = []
            
            for restaurant in restaurants: 
                restaurant_list.append({
                    "sub_category"      : restaurant.sub_category.name,
                    "category"          : restaurant.sub_category.category.name,
                    "restaurant_name"   : restaurant.name,
                    "address"           : restaurant.address,
                    "rating"            : round(restaurant.filtering, 1),
                    "image"             : restaurant.foods.all()[0].images.all()[0].image_url,
                    "restaurant_id"     : restaurant.id
                })

            return JsonResponse({"message":"success", "result":restaurant_list[:5]}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)

class RestaurantDetailView(View):
    @ConfirmUser
    def get(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            is_wished  = request.user.wishlist_restaurants.filter(id=restaurant_id).exists() if request.user else False

            reviews                   = restaurant.review_set.all()
            average_rating            = reviews.aggregate(Avg("rating"))["rating__avg"]
            review_count              = {
                "total"        : reviews.count(),
                "rating_one"   : reviews.filter(rating=1).count(),
                "rating_two"   : reviews.filter(rating=2).count(),
                "rating_three" : reviews.filter(rating=3).count(),
                "rating_four"  : reviews.filter(rating=4).count(),
                "rating_five"  : reviews.filter(rating=5).count(),
            }

            result = {
            "id"             : restaurant.id,
            "sub_category"   : restaurant.sub_category.name,
            "name"           : restaurant.name,
            "address"        : restaurant.address,
            "phone_number"   : restaurant.phone_number,
            "coordinate"     : restaurant.coordinate,
            "open_time"      : restaurant.open_time,
            "updated_at"     : restaurant.updated_at,
            "is_wished"      : is_wished,
            "review_count"   : review_count,
            "average_rating" : average_rating,
            }

            return JsonResponse({"message":"success", "result":result}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)        

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

class ReviewView(View):
    @ConfirmUser
    def patch(self, request, restaurant_id, review_id):
        try:
            data    = json.loads(request.body)
            content = data["content"]
            rating  = data["rating"]

            if not Review.objects.filter(id=review_id, user_id=request.user.id).exists():
                return JsonResponse({"message":"REVIEW_NOT_EXISTS"}, status=404)

            Review.objects.filter(id=review_id, user_id=request.user.id).update(content=content, rating=rating, updated_at=timezone.now())
            
            return JsonResponse({"message":"success"}, status=204)
            
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)