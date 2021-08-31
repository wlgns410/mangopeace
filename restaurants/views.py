import json
from django.db.models.query import Prefetch
from django.http        import JsonResponse
from django.views       import View
from django.db.utils    import DataError
from django.db.models   import Avg, Q, Count
from django.utils       import timezone

from restaurants.models import Restaurant, Food, SubCategory, Image
from users.utils        import ConfirmUser, LooseConfirmUser
from users.models       import Review

class PopularView(View):
    def get(self, request):
        try:
            dict_sort={
                "average_rating" : "-filtering"
            }
            filtering = request.GET.get("filtering", None)
            restaurants = Restaurant.objects.select_related("sub_category", "sub_category__category").prefetch_related(
                Prefetch("foods", queryset=Food.objects.prefetch_related(
                    Prefetch("images", queryset=Image.objects.all(), to_attr="all_images")
                    ), to_attr="all_foods")).annotate(filtering=Avg("review__rating")).order_by(dict_sort[filtering])
            
            restaurant_list = [{
                    "sub_category" : restaurant.sub_category.name,
                    "category" : restaurant.sub_category.category.name,
                    "restaurant_name" : restaurant.name,
                    "address" : restaurant.address,
                    "rating" : round(restaurant.filtering, 1),
                    "image" : restaurant.all_foods[0].all_images[0].image_url,
                    "restaurant_id" : restaurant.id
            }for restaurant in restaurants]

            return JsonResponse({"message":"SUCCESS", "result":restaurant_list[:5]}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)


class RestaurantDetailView(View):
    @LooseConfirmUser
    def get(self, request, restaurant_id):
        try:
            is_wished = request.user.wishlist_restaurants.filter(id=restaurant_id).exists() if request.user else False

            restaurant = Restaurant.objects.select_related("sub_category").prefetch_related("foods").filter(id=restaurant_id).annotate(
                rating_total = Count("review"),
                rating_one = Count("review", filter=Q(review__rating=1)),
                rating_two = Count("review", filter=Q(review__rating=2)),
                rating_three = Count("review", filter=Q(review__rating=3)),
                rating_four = Count("review", filter=Q(review__rating=4)),
                rating_five = Count("review", filter=Q(review__rating=5)),
                average_rating = Avg("review__rating")
            )[0]

            average_price = restaurant.foods.aggregate(Avg("price"))["price__avg"]

            detail_result = {
            "sub_category_id" : restaurant.sub_category.id,
            "restaurant_id" : restaurant.id,
            "sub_category" : restaurant.sub_category.name,
            "name" : restaurant.name,
            "address" : restaurant.address,
            "phone_number" : restaurant.phone_number,
            "coordinate" : restaurant.coordinate,
            "open_time" : restaurant.open_time,
            "updated_at" : restaurant.updated_at,
            "is_wished" : is_wished,
            "review_count" : {
                "total" : restaurant.rating_total,
                "rating_one" : restaurant.rating_one,
                "rating_two" : restaurant.rating_two,
                "rating_three" : restaurant.rating_three,
                "rating_four" : restaurant.rating_four,
                "rating_five" : restaurant.rating_five,
                },
            "average_rating" : round(restaurant.average_rating, 1),
            "average_price" : round(average_price, 0)
            }

            return JsonResponse({"message":"SUCCESS", "result":detail_result}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)

        except IndexError:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)   

class RestaurantReviewView(View):
    @ConfirmUser
    def post(self, request, restaurant_id):
        try:
            data = json.loads(request.body)
            restaurant = Restaurant.objects.get(id=restaurant_id)
            content = data["content"]
            rating = data["rating"]

            Review.objects.create(
                user = request.user,
                restaurant = restaurant,
                content = content,
                rating = rating
            )

            return JsonResponse({"message":"SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        
        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)     

    def get(self, request, restaurant_id):
        offset        = int(request.GET.get("offset", 0))
        limit         = int(request.GET.get("limit", 10))
        rating_min    = request.GET.get("rating-min", 1)
        rating_max    = request.GET.get("rating-max", 5)
        reviews       = Review.objects.prefetch_related("user").filter(restaurant_id=restaurant_id, rating__gte = rating_min, rating__lte = rating_max).order_by("-created_at")[offset : offset + limit]
        review_list   = [{
            "user":{
                "id"            : review.user.id,
                "nickname"      : review.user.nickname,
                "profile_image" : review.user.profile_url,
                "review_count"  : review.user.reviewed_restaurants.count()
                },
                "id"         : review.id,
                "content"    : review.content,
                "rating"     : review.rating,
                "created_at" : review.created_at,
            } for review in reviews]

        return JsonResponse({"message":"success", "result":review_list}, status=200)

class RestaurantFoodsView(View):
    def get(self, request, restaurant_id):
        try:
            foods      = Food.objects.prefetch_related("images").filter(restaurant_id=restaurant_id)
            foods_list = [{
                "id"     : food.id, 
                "name"   : food.name, 
                "price"  : food.price, 
                "images" : [image.image_url for image in food.images.all()]
            } for food in foods]

            return JsonResponse({"message":"success", "result":foods_list}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)
            
class WishListView(View):
    @ConfirmUser
    def post(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)

            if request.user.wishlist_restaurants.filter(id=restaurant_id).exists():
                return JsonResponse({"message":"WISHLIST_ALREADY_EXISTS"}, status=400)

            request.user.wishlist_restaurants.add(restaurant)
            
            return JsonResponse({"message":"SUCCESS"}, status=201)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXISTS"}, status=404)   
        
    @ConfirmUser
    def delete(self, request, restaurant_id):
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)

            if not request.user.wishlist_restaurants.filter(id=restaurant_id).exists():
                return JsonResponse({"message":"WISHLIST_NOT_EXISTS"}, status=404)

            request.user.wishlist_restaurants.remove(restaurant)

            return JsonResponse({"message":"SUCCESS"}, status=204)

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
    def delete(self, request, restaurant_id, review_id):
        try:
            review = Review.objects.get(id=review_id, user_id=request.user.id)
            review.delete()

            return JsonResponse({"message":"success"}, status=204)

        except DataError:
            return JsonResponse({"message":"DATA_ERROR"}, status=400)

        except Review.DoesNotExist:
            return JsonResponse({"message":"REVIEW_NOT_EXISTS"}, status=404)
            
class BannerView(View):
    def get(self, request):
        try:
            subcategories = SubCategory.objects.prefetch_related(
                Prefetch("restaurants", queryset=Restaurant.objects.prefetch_related(
                    Prefetch("foods", queryset=Food.objects.prefetch_related(
                            Prefetch("images", queryset=Image.objects.all(), to_attr="all_images")
                            ), to_attr="all_foods")
                            ), to_attr="all_restaurants")
            )

            subcategory_list = [{
                "sub_category_id" : subcategory.id,
                "name" : subcategory.name,
                "image" : subcategory.all_restaurants[0].all_foods[0].all_images[0].image_url,
            }for subcategory in subcategories]

            return JsonResponse({"message":"success", "result":subcategory_list}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)

class RestaurantView(View):
    def get(self, request, restaurant_id):
        try:
            ordering = request.GET.get("ordering", None)
            sub_category = int(request.GET.get("sub_category_id", None))

            if sub_category:
                restaurants = Restaurant.objects.prefetch_related(Prefetch("foods", queryset=Food.objects.prefetch_related(
                    Prefetch("images", queryset=Image.objects.all(), to_attr="all_images")
                    ), to_attr="all_foods")).filter(sub_category_id=sub_category).annotate(average_rating=Avg("review__rating")).order_by("-"+ordering)
            else:
                restaurants = Restaurant.objects.prefetch_related(Prefetch("foods", queryset=Food.objects.prefetch_related(
                    Prefetch("images", queryset=Image.objects.all(), to_attr="all_images")
                    ), to_attr="all_foods")).annotate(average_rating=Avg("review__rating")).order_by("-"+ordering)

            restaurant_list = [{
                "name" : restaurant.name,
                "address" : restaurant.address,
                "image" : restaurant.all_foods[0].all_images[0].image_url,
                "rating" : round(restaurant.average_rating, 1),
                "restaurant_id" : restaurant.id
            }for restaurant in restaurants]          

            reviews = Review.objects.prefetch_related("user").filter(restaurant_id=restaurant_id).order_by("-created_at")

            review_list   = [{
                "review_id" : review.user.id,
                "content" : review.content,
                "profile_url" : review.user.profile_url if review.user else None,
                "nickname" : review.user.nickname
            }for review in reviews]
            
            return JsonResponse({"message":"success", "restaurant_list":restaurant_list[:5], "review_list" : review_list}, status=200)

        except Restaurant.DoesNotExist:
            return JsonResponse({"message":"RESTAURANT_NOT_EXIST"}, status=404)


class FilteringView(View):
    def get(self, request):
        sorted_dict ={
            "rating_sort":"-average_rating",
            "review_count":"-review_counts"
        }

        keyword = request.GET.getlist('keyword', None)
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 6))
        sort = request.GET.get("sort", "rating_sort")
        renew = request.GET.get("renew", None)
        
        q = Q()
        if keyword:
            q &= Q(name__in = keyword)

        category_restaurants        = Restaurant.objects.filter(sub_category__category__name__in=keyword).annotate(average_rating=Avg('review__rating'), review_counts=Count('review')).order_by(sorted_dict[sort])[offset:offset+limit]
        sub_category_restaurants    = Restaurant.objects.filter(sub_category__name__in=keyword).annotate(average_rating=Avg('review__rating'), review_counts=Count('review'))[offset:offset+limit]
        restaurants_list            = Restaurant.objects.filter(q).annotate(average_rating=Avg('review__rating'), review_counts=Count('review'))[offset:offset+limit]
        

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
        }for restaurant in restaurants_list]

        return JsonResponse({
            "category_result"       :category_result,
            "sub_category_result"   :sub_category_result,
            "restaurant_result"     :restaurant_result
            }, status=200)