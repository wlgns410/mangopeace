from django.db.models.aggregates import Count, Sum
from django.http import JsonResponse
from django.views import View
from django.db.models import Avg, Q

from restaurants.models import Restaurant

# class HighListView(View):
#     def get(self, request, restaurant_id):
#         try:       
#             restaurants = Restaurant.objects.all()  
#             restaurant_list = []
#             for restaurant in restaurants:
#                 print(restaurant)
#                 restaurant_list.append({
#                     "sub_category"      : restaurant.sub_category.name,
#                     "category"          : restaurant.sub_category.category.name,
#                     "restaurant_name"   : restaurant.name,
#                     "address"           : restaurant.address,
#                     "rating"            : round(restaurant.review_set.all().aggregate(Avg('rating'))['rating__avg'], 1),
#                     "image"             : restaurant.foods.all()[0].images.all()[0].image_url
#                 })

                
#             restaurant_list = sorted(restaurant_list, key=lambda x:x['rating'], reverse=True)

#             return JsonResponse({"message":"success", "result":restaurant_list[:5]}, status=200)

#         except KeyError:
#             return JsonResponse({"message":"KEY_ERROR"}, status=400)

class HighListView(View):
    def get(self, request, restaurant_id):
        try:
            restaurants = Restaurant.objects.annotate(average_rating=Avg("review__rating")) # 바로 2다리 들어가는 명령어           
            print(restaurants)
            restaurants = restaurants.order_by("review__rating")
            print(restaurants)
            
            restaurant_list = []
            for restaurant in restaurants:
 
                print(restaurant.average_rating)
                restaurant_list.append({
                    "sub_category"      : restaurant.sub_category.name,
                    "category"          : restaurant.sub_category.category.name,
                    "restaurant_name"   : restaurant.name,
                    "address"           : restaurant.address,
                    "rating"            : restaurant.average_rating,
                    "image"             : restaurant.foods.all()[0].images.all()[0].image_url
                })
            # restaurant_list = sorted(restaurant_list, key=lambda x:x["rating"], reverse=True)

            return JsonResponse({"message":"success", "result":restaurant_list[:5]}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

          



# import json
# from operator         import itemgetter
# from django.views     import View
# from django.http      import JsonResponse
# from django.db.models import Q
# from django.db.models import Count
# from .models  import Category, Option, Product, ProductCategory
# class ProductsView(View) :
#     def get(self,request) :
#         try :
#             category_id    = request.GET.get("id",0)
#             offset         = int(request.GET.get("offset",0))
#             limit          = int(request.GET.get("limit",10))
#             sort           = request.GET.get("sort", "high_price")
#             category_iamge = ""
#             q = Q()
#             if category_id:
#                 q.add(category__id=category_id, and)
#             if Category.objects.filter(id=category_id).exists():
#                 category = Category.objects.get(id=category_id)
#                 category_iamge = category.iamge_url
#             order = {
#                 "high_price" : "-max_price",
#                 "low_price"  : "max_price",
#                 "bast"       : "-sales"
#             }
#             OFFSET = offset * limit
#             LIMIT  = OFFSET + limit
#             results = {
#                 "category_iamge" : category_iamge,
#                 "products"       : [
#                     {
#                         "id"          : product.id,
#                         "name"        : product.name,
#                         "descirption" : product.description,
#                         "iamge"       : product.thumbnail_image_url,
#                         "hover"       : product.hover_image_url,
#                         "score"       : product.score,
#                         "sales"       : product.sales,
#                         "price"       : product.max_price,
#                         "option"      : [{
#                                 "price" : option.price,
#                                 "sales" : option.sales,
#                                 "weight" : option.weight
#                             } for option in product.option_set.all()]
#                     } for product in Product.objects.filter(category__id=category_id)
#                                                     .annotate(max_price=Max("option__price"))
#                                                     .order_by(order[sort])[OFFSET:LIMIT]
#                 ]
#             }
#             return JsonResponse({'MESSAGE':'SUCCESS', "results": results}, status=201)
#         except KeyError :
#             return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)