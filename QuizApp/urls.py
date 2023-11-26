from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger_ui'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)), name='graphQL'),
    path('account/', include('account_app.urls')),
    path('', include('quiz_app.urls')),
]
