from django.http        import JsonResponse
from django.views       import View

from restaurants.models import Restaurant

class RestaurantReviewView(View):
    def get(self, request, restaurant_id):
        try:
            offset        = int(request.GET.get("offset", 1))
            limit         = int(request.GET.get("limit", 10))
            rating_min    = request.GET.get("rating-min", 1)
            rating_max    = request.GET.get("rating-max", 5)
            
            restaurant  = Restaurant.objects.get(id=restaurant_id)
            reviews     = restaurant.review_set.filter(rating__gte = rating_min, rating__lte = rating_max).order_by("-created_at")[offset : limit]
            review_list = [{
                    "user":{
                        "id":r.user.id,
                        "nickname":r.user.nickname,
                        "profile_image":r.user.profile_url if hasattr(r.user, "profile_url") else None,
                        "review_count":r.user.reviewed_restaurants.count()
                    },
                    "id":r.id,
                    "content" : r.content,
                    "rating":r.rating,
                    "created_at":r.created_at,
                } for r in reviews]
            print(review_list)

            return JsonResponse({"message":"success", "result":review_list}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)