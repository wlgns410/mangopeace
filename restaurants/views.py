from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Avg

from restaurants.models import SubCategory
from restaurants.models import Restaurant
from users.utils        import ConfirmUser

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

class TopListView(View):
    def get(self, request):
        try:
            dic_sort={ 
                "average_rating" : "-ordering"
            }
            ordering = request.GET.get("ordering", None)
            
            sub_categorys = SubCategory.objects.all()          
            sub_category_list = []
            for sub_category in sub_categorys:
                restaurants = sub_category.restaurants.annotate(ordering=Avg("review__rating")).order_by(dic_sort[ordering])
                                
                restaurant_list = []            
                for restaurant in restaurants:
                    restaurant_list.append({
                            "name"          : restaurant.name,
                            "address"       : restaurant.address,
                            "content"       : restaurant.review_set.order_by('?')[0].content,
                            "profile_url"   : restaurant.review_set.order_by('?')[0].user.profile_url,
                            "nickname"      : restaurant.review_set.order_by('?')[0].user.nickname,
                            "image"         : restaurant.foods.all()[0].images.all()[0].image_url,
                            "rating"        : round(restaurant.ordering, 1),
                            "restaurant_id" : restaurant.id
                        })

                return JsonResponse({"message":"success", "result":restaurant_list}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)         