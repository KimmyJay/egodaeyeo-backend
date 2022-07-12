from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

from item.models import Item as ItemModel
from item.models import Category as CategoryModel
from item.serializers import ItemSerializer, CategorySerializer
from user.models import User as UserModel


class ItemView(APIView):
    
    def get(self, request):
        user = request.user
        items = ItemModel.objects.all().order_by('-created_at')
        categories = CategoryModel.objects.all()
        
        #유저가 주소를 설정 했을때 Query
        try:
            address_query = Q(item__user__address__contains=user.address)
            items = items.filter(address_query)
        except:
            pass
        # 카테고리명 Query Parameter로 가져오기
        category_name = request.GET.get('category', None)
        if category_name is not None:
            query = Q(category__name=category_name)
            items = items.filter(query)
            
        item_serializer = ItemSerializer(items, many=True, context={"request": request})
        category_serializer = CategorySerializer(categories, many=True, context={"request": request})
        data = {
            'categories': category_serializer.data,
            'items': item_serializer.data,
        }
        
        
        return Response(data, status=status.HTTP_200_OK)
        

class DetailView(APIView):

    def get(self, request):
        items = ItemModel.objects.all().values()
        print(items)
        
        # user = UserModel.objects.get(id=request.user)
        # print(user)
        return Response(items)