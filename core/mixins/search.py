from django.db.models import Q


class SearchFilterMixin:
    search_fields = []
    category_field = None
    price_field = None

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request
        search = request.GET.get("search")
        category = request.GET.get("category")
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")

        if search and self.search_fields:
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f"{field}__icontains": search})
            qs = qs.filter(q_objects)

        if category and self.category_field:
            qs = qs.filter(**{self.category_field: category})

        if min_price and self.price_field:
            qs = qs.filter(**{f"{self.price_field}__gte": min_price})
        if max_price and self.price_field:
            qs = qs.filter(**{f"{self.price_field}__lte": max_price})
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        request = self.request
        ctx["current_filters"] = {
            "search": request.GET.get("search", ""),
            "category": request.GET.get("category", ""),
            "min_price": request.GET.get("min_price", ""),
            "max_price": request.GET.get("max_price", ""),
        }
        ctx["has_filters"] = any(ctx["current_filters"].values())
        ctx["popular_categories"] = self.get_popular_categories()
        return ctx

    def get_popular_categories(self):
        return []
