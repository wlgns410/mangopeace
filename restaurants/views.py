from django.http        import JsonResponse
from django.views       import View
from restaurants.models import Restaurant

class RestaurantReviewView(View):
    def get(self, request, restaurant_id):
        try:
            UNIT_PER_PAGE    = 10
            limit            = int(request.GET.get("limit", 1)) * UNIT_PER_PAGE
            rating_min       = request.GET.get("rating-min", 0)
            rating_max       = request.GET.get("rating-max", 5)
            
            restaurant_instance = Restaurant.objects.get(id=restaurant_id)
            reviews_queryset    = restaurant_instance.review_set
            filtered            = reviews_queryset.filter(rating__gte = rating_min, rating__lte = rating_max).order_by("-created_at")[limit - UNIT_PER_PAGE : limit]
            reviews             = []

            for review_instance in filtered:
                review = {
                    "user":{
                        "id":review_instance.user.id,
                        "nickname":review_instance.user.nickname,
                        "profile_image":review_instance.user.profile_url if hasattr(review_instance.user, "profile_url") else None,
                        "review_count":review_instance.user.reviewed_restaurants.count()
                    },
                    "id":review_instance.id,
                    "content" : review_instance.content,
                    "rating":review_instance.rating,
                    "created_at":review_instance.created_at,
                }
                reviews.append(review)

            return JsonResponse({"message":"success", "result":reviews}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=400)       