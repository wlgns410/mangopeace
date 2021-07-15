from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q, Count, Avg

from restaurants.models import Restaurant, Image

class FilteringVeiw(View):
    def get(self, request):
        sorted_dict ={
            "rating_sort":"-average_rating",
            "review_count":"-review_counts"
        }

        keyword = request.GET.getlist('keyword', None)
        offset  = int(request.GET.get('offset', 0))
        limit   = int(request.GET.get('limit', 6))
        sort    = request.GET.get("sort", "rating_sort")
        renew  = request.GET.get("renew", None)
        
        q = Q()
        if keyword:
            q &= Q(name__in = keyword)

        category_restaurants        = Restaurant.objects.filter(sub_category__category__name__in=keyword).annotate(average_rating=Avg('review__rating'), review_counts=Count('review')).order_by(sorted_dict[sort])[offset:offset+limit]
        sub_category_restaurants    = Restaurant.objects.filter(sub_category__name__in=keyword).annotate(average_rating=Avg('review__rating'), review_counts=Count('review'))[offset:offset+limit]
        restaurants                 = Restaurant.objects.filter(q).annotate(average_rating=Avg('review__rating'), review_counts=Count('review'))[offset:offset+limit]
        hello = [{Count(category_restaurants, sub_category_restaurants, restaurants)}]

        if renew == "review_count":
            Restaurant.objects.filter(sub_category__category__name__in=keyword).order_by(sorted_dict[renew])[offset:offset+limit]
            Restaurant.objects.filter(sub_category__name__in=keyword).order_by(sorted_dict[renew])[offset:offset+limit]
            Restaurant.objects.filter(q).order_by(sorted_dict[renew])[offset:offset+limit]

        category_result = [{
            "restaurantID"          : category_restaurant.id,
            "restaurantName"        : category_restaurant.name,
            "restaurantAddress"     : category_restaurant.address,
            "restaurantPhoneNum"    : category_restaurant.phone_number,
            "restaurantCoordinate"  : category_restaurant.coordinate,
            "restaurantOpenTime"    : category_restaurant.open_time,
            "food_image_url"        : Image.objects.filter(food__id = category_restaurant.foods.first().id).first().image_url,
            "average_rating"        : category_restaurant.average_rating,
            "review_count"          : category_restaurant.review_counts,
        }for category_restaurant in category_restaurants]

        sub_category_result=[{
            "restaurantID"          : sub_category_restaurant.id,
            "restaurantName"        : sub_category_restaurant.name,
            "restaurantAddress"     : sub_category_restaurant.address,
            "restaurantPhoneNum"    : sub_category_restaurant.phone_number,
            "restaurantCoordinate"  : sub_category_restaurant.coordinate,
            "restaurantOpenTime"    : sub_category_restaurant.open_time,
            "food_image_url"        : Image.objects.filter(food__id = sub_category_restaurant.foods.first().id).first().image_url,
            "average_rating"        : sub_category_restaurant.average_rating,
            "review_count"          : sub_category_restaurant.review_counts,
        }for sub_category_restaurant in sub_category_restaurants]

        restaurant_result=[{
            "restaurantID"          : restaurant.id,
            "restaurantName"        : restaurant.name,
            "restaurantAddress"     : restaurant.address,
            "restaurantPhoneNum"    : restaurant.phone_number,
            "restaurantCoordinate"  : restaurant.coordinate,
            "restaurantOpenTime"    : restaurant.open_time,
            "food_image_url"        : Image.objects.filter(food__id = restaurant.foods.first().id).first().image_url,
            "average_rating"        : restaurant.average_rating,
            "review_count"          : restaurant.review_counts,
        }for restaurant in restaurants]

        return JsonResponse({"yes":hello,
            "category_result"       :category_result,
            "sub_category_result"   :sub_category_result,
            "restaurant_result"     :restaurant_result
            }, status=200)

