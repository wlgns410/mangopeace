from django.http import JsonResponse
from django.views import View

from restaurants.models import SubCategory

class SubCategoryListView(View):
    def get(self, request):
        try:
            subcategorys = SubCategory.objects.all()
                    
            subcategory_list = []
            for subcategory in subcategorys:                            
                subcategory_list.append({
                    "sub_category" : subcategory.id,
                    "image" : subcategory.restaurants.first().foods.first().images.first().image_url
                })

            return JsonResponse({"message":"success", "result":subcategory_list}, status=200)

        except SubCategory.DoesNotExist:
            return JsonResponse({"message":"sub_category_NOT_EXIST"}, status=404)