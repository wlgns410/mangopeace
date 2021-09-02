# 망고 플레이트 Project Backend
<br>

<img width="671" alt="스크린샷 2021-09-02 오후 2 33 53" src="https://user-images.githubusercontent.com/81137234/131787627-f1fcc1ad-6114-4e04-a9bb-499f4ecb1378.png">
- [유투브 링크](https://youtu.be/micnaXndqY8)

<br>

## 작성한 엔드포인트

- 인기있는 레스토랑 
```
class PopularView(View):
    @query_debugger
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
```

<img width="606" alt="스크린샷 2021-09-02 오후 3 37 15" src="https://user-images.githubusercontent.com/81137234/131794635-c75840d9-efb6-4f01-8db2-3c93b08fe343.png">
<img width="632" alt="스크린샷 2021-09-02 오후 3 37 27" src="https://user-images.githubusercontent.com/81137234/131794648-a2d655b0-1dd2-4737-94a4-5209f29cdf3c.png">

<br>

- 카테고리별 레스토랑 리스트 

```
class RestaurantView(View):
    @query_debugger
    def get(self, request, restaurant_id):
        try:
            ordering = request.GET.get("ordering", None)
            sub_category = int(request.GET.get("sub_category_id", None))

            q_object = Q()
            if sub_category:
                q_object &= Q(sub_category_id=sub_category)
                restaurants = Restaurant.objects.prefetch_related(Prefetch("foods", queryset=Food.objects.prefetch_related(
                    Prefetch("images", queryset=Image.objects.all(), to_attr="all_images")
                    ), to_attr="all_foods")).filter(q_object).annotate(average_rating=Avg("review__rating")).order_by("-"+ordering)
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
```

<img width="606" alt="스크린샷 2021-09-02 오후 3 43 01" src="https://user-images.githubusercontent.com/81137234/131795327-7431e578-6182-4f87-9a2c-cc4c37773ad5.png">
<img width="682" alt="스크린샷 2021-09-02 오후 3 43 11" src="https://user-images.githubusercontent.com/81137234/131795337-30db12cf-6826-4b96-9d17-86ea30e3d961.png">

<br> 

- 배너 리스트

```
class BannerView(View):
    @query_debugger
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
```
<img width="606" alt="스크린샷 2021-09-02 오후 3 43 52" src="https://user-images.githubusercontent.com/81137234/131795544-70027999-de95-41bb-aa38-4a39032ea4e4.png">
<img width="671" alt="스크린샷 2021-09-02 오후 3 44 01" src="https://user-images.githubusercontent.com/81137234/131795552-4a73aa58-f34f-4561-b86d-5d23b8f7a1ee.png">


<br>

## 프로젝트 소개
- 망고플레이트란, 사용자 데이터 기반의 식당추천 서비스로 주변 맛집 정보 및 추천 맛집 리스트 등, 종합적인 맛집 발견 경험을 제공하는 사이트입니다.
- 우리의 프로젝트는, 망고플레이트의 기능(맛집 리스트, 검색 필터링, 가고싶다, 리뷰, 평점 등)을 모티브한 프로젝트입니다.
- 짧은 프로젝트 기간동안 개발에 집중해야 하므로 디자인 및 기능의 기획 부분을 차용했습니다.
- 개발은 초기 세팅부터 전부 직접 구현했으며, 모두 백앤드와 연결하여 실제 사용할 수 있는 서비스 수준으로 개발한 것입니다.
- [백엔드 github 링크](https://github.com/wecode-bootcamp-korea/22-1st-mangoPeace-backend)
- [프론트엔드 github 링크](https://github.com/wecode-bootcamp-korea/22-1st-mangoPeace-frontend)

### 개발 인원 및 기간
- 개발기간 : 2021/7/5 ~ 2030/7/16
- 개발 인원 : 백엔드 3명, 프론트엔드 3명
- 백엔드 : [이원석(PM)](https://github.com/wonseok2877), [최준영](https://github.com/showmethr23), [이지훈](https://github.com/wlgns410)
- 프론트엔드 : [정빛열음](https://github.com/kylee817), [이의연](https://github.com/euiyeonlee), [이경민](https://github.com/glorious-min)

### 프로젝트 선정이유
- 위코드 커리큘럼에서 배운 기술들을 그대로 적용하고 응용하는 데에 있어 난이도가 적합하다고 판단했습니다.
- 사용자의 선택에 따라 구분되는 필터링이 매력적이라고 생각했습니다.
- 맛집 추천과 SNS 개념의 접목이 매력적이라고 생각했습니다.

<br>

## 적용 기술 및 협업 툴

### 협업 툴

> - [Notion](https://www.notion.so/072c9c94dcaa424486c3e8b567a234b1)
> - [Trello](https://trello.com/b/aXkK1j1t/%EC%8B%B8%EC%9A%B0%EC%A7%80%EB%A7%9D%EA%B3%A0-%F0%9F%A5%AD)
> - Github
> - Slack
> - Postman
> - AqueryTool

<img width="980" alt="스크린샷 2021-09-02 오후 2 36 15" src="https://user-images.githubusercontent.com/81137234/131787831-d4298d41-cd12-49ef-a8eb-81f7d4141b02.png">

### 적용 기술

> - Front-End : javascript, React.js framwork, sass, Kakao Map API
> - Back-End : Python, Django, MySQL, Bcrypt, pyjwt
> - Common : AWS, RESTful API,AqueryTool

### 구현 기능

#### 회원가입 / 로그인 모달
- 회원가입 시 정규식을 통한 유효성 검사. (소문자, 대문자, 특수문자의 조합)
- 로그인을 이후 토큰 발행, 계정 활성화
- 계정 없을 시 바로 회원가입 모달로 이동할 수 있도록 구현.

#### 메인페이지

- 검색바에서 키워드 검색시 검색 페이지로 이동.
- 맛집 리스트 배너. 클릭 시 리스트 페이지로 이동.
- TOP5 식당 배너. 클릭 시 해당 식당의 상세 페이지로 이동.
- 하단 푸터를 통한 사이트 설명.

#### 검색 페이지

- 키워드(카테고리, 식당 이름) 필터링.
- 리뷰순, 평점순, 가격대에 대한 세부 필터링.
- 페이지네이션.

#### 리스트페이지

- 카테고리에 대한 식당 리스트를 평점순으로 나열.
- 클릭시 상세 페이지로 이동.

#### 상세페이지

- 위도와 경도를 이용한 kakao map API 구현.
- 식당 상세정보, 음식 사진 정보, 가고싶다 여부.
- 식당에 대한 리뷰 평점순으로 나열, 페이지네이션.
- 가고싶다(위시리스트) 생성, 삭제
- 리뷰 생성, 수정, 삭제

#### 네비게이션 바
- 검색바.
- 회원가입, 로그인 버튼.
- 이름, 사진, 가고싶다 목록 등 유저 정보.


<br>

## Reference

- 이 프로젝트는 [망고플레이트](https://www.mangoplate.com/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
