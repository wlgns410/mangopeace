import jwt

import functools, time
from django.db   import connection, reset_queries
from django.conf import settings

from django.http.response import JsonResponse

from jwt.exceptions       import ExpiredSignatureError, InvalidSignatureError, DecodeError

import my_settings
from users.models         import User

def query_debugger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        number_of_start_queries = len(connection.queries)
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        number_of_end_queries = len(connection.queries)
        print(f"-------------------------------------------------------------------")
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {number_of_end_queries-number_of_start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        print(f"-------------------------------------------------------------------")
        return result
    return wrapper

class ConfirmUser:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization")
            
            if not access_token:
                return JsonResponse({"message" : "ACCESS_TOKEN_REQUIRED"})
            
            payload      = jwt.decode(jwt=access_token, key=my_settings.SECRET_KEY,  algorithms=my_settings.ALGORITHM)
            user         = User.objects.get(id=payload["id"])
            request.user = user
            
            return self.func(self, request, *args, **kwargs)
        
        except InvalidSignatureError:
            return JsonResponse({"message":"INVALID_SIGNATURE"}, status=400)
        
        except ExpiredSignatureError:
            return JsonResponse({"message":"EXPIRED_SIGNATURE"}, status=400)
        
        except DecodeError:
            return JsonResponse({"message":"DECODE_ERROR"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message":"USER_NOT_EXIST"}, status=404)

class LooseConfirmUser:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization")
            
            if access_token:
                payload      = jwt.decode(jwt=access_token, key=my_settings.SECRET_KEY,  algorithms=my_settings.ALGORITHM)
                request.user = User.objects.get(id=payload["id"])
            else:
                request.user = None
            
            return self.func(self, request, *args, **kwargs)
        
        except InvalidSignatureError:
            return JsonResponse({"message":"INVALID_SIGNATURE"}, status=400)
        
        except ExpiredSignatureError:
            return JsonResponse({"message":"EXPIRED_SIGNATURE"}, status=400)
        
        except DecodeError:
            return JsonResponse({"message":"DECODE_ERROR"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message":"USER_NOT_EXIST"}, status=404)