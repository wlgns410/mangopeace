import json
import bcrypt
import jwt
import datetime

from django.views           import View
from django.http            import JsonResponse
from django.db.utils        import DataError
from django.db.models       import Avg

from json.decoder           import JSONDecodeError

import my_settings
from users.models           import Review, User
from users.utils            import ConfirmUser
from restaurants.models     import Image

class SignInView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            email    = data["email"]
            password = data["password"]
            user     = User.objects.get(email=email)
            
            if not bcrypt.checkpw(password.encode(), user.password.encode()):
                return JsonResponse({"message":"VALIDATION_ERROR"}, status=400)        

            exp           = datetime.datetime.now() + datetime.timedelta(hours=24)
            access_token  = jwt.encode(
                payload   = {"id" : user.id, "exp" : exp},
                key       = my_settings.SECRET_KEY,
                algorithm = my_settings.ALGORITHM
            )

            return JsonResponse({"message":"success", "access_token":access_token}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)   
        
        except User.DoesNotExist:
            return JsonResponse({"message":"USER_NOT_EXIST"}, status=404)       

        except DataError:
            return JsonResponse({"message": "DATA_ERROR"}, status=400) 

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.validate(data):
                return JsonResponse({"message":"VALIDATION_ERROR"}, status=401)        

            nickname        = data["nickname"]
            email           = data["email"]
            password        = data["password"]
            phone_number    = data["phone_number"]
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            User.objects.create(
            nickname     = nickname,
            email        = email,
            password     = hashed_password.decode(),
            phone_number = phone_number,
            )

            return JsonResponse({"message":"success"}, status=201)

        except JSONDecodeError:
            return JsonResponse({"message":"JSON_DECODE_ERROR"}, status=400)        
        
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)        
        
        except DataError:
            return JsonResponse({"message": "DATA_ERROR"}, status=400)

class UserDetailView(View):
    @ConfirmUser
    def get(self, request):
        for restaurant in request.user.wishlist_restaurants.annotate(average_rating=Avg("review__rating")):
            print(restaurant.average_rating)
        wish_list = [
            {
            "name"           : restaurant.name,
            "address"        : restaurant.address,
            "sub_category"   : restaurant.sub_category.name,
            "average_rating" : restaurant.review_set.aggregate(Avg("rating"))["rating__avg"] if restaurant.review_set.all().exists() else 0
            if Review.objects.filter(restaurant_id=restaurant.id) else 0,
            "is_wished"      : True,
            "food_image"     : restaurant.foods.first().images.first().image_url
            } for restaurant in request.user.wishlist_restaurants.annotate(average_rating=Avg("review__rating"))]
        result = {
            "nickname"       : request.user.nickname,
            "email"          : request.user.email,
            "profile_url"    : request.user.profile_url,
            "wish_list"      : wish_list,
        }
        
        return JsonResponse({"message":"success","result":result}, status=200)