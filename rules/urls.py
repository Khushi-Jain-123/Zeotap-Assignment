# rules/urls.py

from django.urls import path
from .views import RuleEngineViewSet

urlpatterns = [
    path('', RuleEngineViewSet.as_view({'get': 'index'}), name='index'),
    path('create_rule/', RuleEngineViewSet.as_view({'post': 'create_rule'}), name='create_rule'),
    path('evaluate_rule/', RuleEngineViewSet.as_view({'post': 'evaluate_rule'}), name='evaluate_rule'),
    path('combine_rules/', RuleEngineViewSet.as_view({'post': 'combine_rules'}), name='combine_rules'),
    path('get_rules/', RuleEngineViewSet.as_view({'post': 'get_rules'}), name='get_rules'),
]
