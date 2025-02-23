from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from products.filters import ProductFilter
from products.models import Product as Product, Category, Order
from products.permissions import IsOwnerOrSuperAdmin
from products.serializers import (
    ProductSerializer,
    ProductViewSerializer,
    CategoryWithProductsSerializer,
    OrderSerializer,
)


class ProductViewSet(ModelViewSet):
    # foreign key - select_related
    # many to many - prefetch_related
    queryset = Product.objects.all().\
        select_related("category").prefetch_related("tags")
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter

    # All different ways to paginate
    # pagination_class = PageNumberPagination
    # pagination_class = LimitOffsetPagination
    pagination_class = CursorPagination

    ordering_fields = ("name", "price")
    ordering = ("name",)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProductViewSerializer
        else:
            return ProductSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().prefetch_related("products")
    serializer_class = CategoryWithProductsSerializer


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrSuperAdmin,
    )
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=self.request.user)
