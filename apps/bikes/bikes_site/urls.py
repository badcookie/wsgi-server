from django.urls import include, path
from .views import ProductViewSet, PublicProductViewSet, CategoriesViewSet


user_routes = [
    path('', PublicProductViewSet.as_view({'get': 'list'})),
    path('<int:product_id>/', PublicProductViewSet.as_view({'get': 'retrieve'})),
    path('category/<int:category_id>/', PublicProductViewSet.as_view({'get': 'list'})),
]

manager_routes = [
    path('', ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path(
        '<int:product_id>/',
        ProductViewSet.as_view(
            {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
        ),
    ),
    path('category/<int:category_id>/', ProductViewSet.as_view({'get': 'list'})),
]

urlpatterns = [
    path('products/', include(user_routes)),
    path('company/products/', include(manager_routes)),
    path('categories/', CategoriesViewSet.as_view({'get': 'list'})),
]
