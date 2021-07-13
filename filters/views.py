import logging
from django.http import JsonResponse
from django.views import View
from django.db.models import Q, Count

from restaurants.models import *

class SearchFormVeiw(View):
    def get(self, request):
        try:
            keyword = request.GET.get('name')
            q = Q()
            if keyword:
                q &= Q(name = keyword)

            restaurants = Restaurant.objects.filter(q).distinct()
            sub_categories = SubCategory.objects.filter(q).distinct()

            # result = [{
            #     "restaurantID" : keyword,
            #     "restaurantName" : restaurant.name,
            #     "restaurantAddress" : restaurant.address,
            #     "restaurantPhoneNum" : restaurant.phone_number,
            #     "restaurantCoordinate" : restaurant.coordinate,
            #     "restaurantOpenTime" : restaurant.open_time
            # }for restaurant in restaurants]

            results = [{
                # "sub_categoryID" : restaurant.sub_category.name,  # 참조
                "sub_category->restaurant": sub_category.restaurant_set.name
                # "restaurantPhoneNum" : sub_category.phone_number,
                # "restaurantCoordinate" : sub_category.coordinate,
                # "restaurantOpenTime" : sub_category.open_time
            }for sub_category in sub_categories]

            return JsonResponse({"restaurant_info":results}, status=200)
        except KeyError:
            return JsonResponse({"nah":"ananan"}, status=400)




































        # try:
        #     # category = request.GET.getlist('category', None)
        #     restaurant = request.GET.getlist('restaurant', None)

        #     q = Q()
        #     # if category:
        #     #     q &= Q(category_id__in = category)
        #     if restaurant:
        #         q &= Q(restaurant__name__in = restaurant)
            
        #     restaurants = Restaurant.objects.filter(q).distinct()

        #     result = [{
        #         "restaurantID" : restaurant.id,
        #         "restaurantName" : restaurant.name,
        #         "restaurantAddress" : restaurant.address,
        #         "restaurantPhone" : restaurant.phone_number,
        #         "restaurantCoordinate" : restaurant.coordinate,
        #         "restaurantOpenTimes" : restaurant.open_time,
        #         # "food_image" : [food_image.image_url for food_image in restaurant.food_set.image_set.all()],
        #     }for restaurant in restaurants]
        #     return JsonResponse({"message":result},status=200)
        
        # except TypeError:
        #     return JsonResponse({"message":"TYPE_ERROR"}, status=400)
        # except ValueError:
        #     return JsonResponse({"message":"VALUE_ERROR"}, status=400)
        
        # try:
            # category = request.GET.getlist('category', None)
            # restaurant = request.GET.getlist('restaurant', None)
            

            # q = Q()
            # if category:
            #     q &= Q(category_id = restaurant)
            # if restaurant:
            #     q &= Q(restaurant_name = restaurant)

            # restaurants = Restaurant.objects.filter(q)
            # restaurant_info = [{
            #     "pk" : restaurant.pk,
            #     "name" : restaurant.name,
            #     "address" : restaurant.address,
            #     "phone" : restaurant.phone_number,
            #     "coordinate": restaurant.coordinate,
            #     "open time" : restaurant.open_time
            # }for restaurant in restaurants]

            # categories = Category.objects.all()

            # category_info = [{
            #     "name" : category.name
            # }for category in categories]

            # return JsonResponse({"category_info" : category_info, "restaurant_info":restaurant_info},status=200)
        # except KeyError:
        #     return JsonResponse({"message":"NOPE"},status=400)
























        # try:
            # category_info     = []
        #     sub_category_info = []
        #     # restaurant_info   = []

            # category     = request.GET.getlist('category', None)
        #     sub_category = request.GET.getlist('sub_category', None)
        #     # restaurant   = request.GET.get('restaurant', None)
            # q = Q()

            # if category:
            #     q &= Q(category_name__in=category)
        #     if sub_category:
        #         q &= Q(sub_category_id__in=sub_category)
        #     # if restaurant:
        #     #     q &= Q(restaurant_id=restaurant)

            # categories      = Category.objects.filter(q)
        #     sub_categories  = SubCategory.objects.filter(q)
        #     # restaurants     = Restaurant.objects.filter(q)

            # category_info=[{
            #         "pk"   : category.pk,
            #         "name" : category.name,
            #         "menu_id": category.id
            #     }for category in categories]
            
        #     sub_category_info = [{
        #         "pk" : sub_category.pk,
        #         "name" : sub_category.name,
        #         "category_id" : sub_category.category.id
        #         }for sub_category in sub_categories]

        #     for restaurant in restaurants:
        #         restaurant_info.append({
        #             "pk"   : restaurant.pk,
        #             "name" : restaurant.name,
        #             "address" : restaurant.address,
        #             "phone_number" : restaurant.phone_number,
        #             "coordinate" : restaurant.coordinate,
        #             "sub_category_id" : restaurant.sub_category.id
        #         })

            # return JsonResponse({
            #     "message":"SUCCESS!",
            #     "category_info" : category_info}, status=200)
        #     },{"sub_category_info" : sub_category_info}, status=201)









            # category = request.GET.getlist('category', None)
            # sub_category = request.GET.getlist('sub_category', None)
            # restaurant = request.GET.get('restaurant', None)

            # q = Q()

            # if category:
            #     q &= Q(sub_category_id__in=category)
            # if sub_category:
            #     q &= Q(sub_category_id__in=sub_category)
            # if restaurant:
            #     q &= Q(restaurant_id=restaurant)
            
            # restaurants = Restaurant.objects.filter(q)
        
            # return JsonResponse({
            #     "message":"SUCCESS!",
            #     "restaurant":restaurants,
            # }, status=200)

        # except KeyError:
        #     return JsonResponse({"message":"hehe"}, status=401)
