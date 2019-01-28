import bars.receivers
from .views import ReferenceList, BarList, StockList, MenuList, RankList,OrderList, OrderDetail, OrderCreate, OrderItemList
from django.urls import path

urlpatterns = [
    path("api/references/", ReferenceList.as_view(), name="references_list"),
    path("api/bars/", BarList.as_view(), name="bars_list"),
    path('api/stock/<int:bar>/', StockList.as_view(), name="stock_detail"),
    path("api/bars/ranking/", RankList.as_view(), name="ranking_list"),
    path('api/menu/', MenuList.as_view(), name="menu_list"),
    path('api/menu/<int:bar>/', MenuList.as_view(), name="menu_detail"),
    path('api/order/<int:bar>/', OrderCreate.as_view(), name="order_create"),
    path('api/orders/', OrderList.as_view(), name="order_list"),
    path('api/orderitems/', OrderItemList.as_view(), name="orderitem_list"),
    path('api/order/<int:pk>/', OrderDetail.as_view(), name="order_detail"),
]

