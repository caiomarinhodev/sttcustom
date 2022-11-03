from django.urls import path, include

from app import conf
from app.urls_api import api_urlpatterns
from app.views.recorder import IndexView, AudioView, RecordView, RedirectToViewProcess

urlpatterns = []

urlpatterns += [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls'))
]

urlpatterns += [
    path('', IndexView.as_view(), name='index'),
    path('upload', AudioView.as_view(), name='upload'),
    path('recorder', RecordView.as_view(), name='recorder'),
    path('view', RedirectToViewProcess.as_view(), name='view'),
]

from app.views import process

urlpatterns += [
    # process
    path(
        'process/',
        process.List.as_view(),
        name=conf.PROCESS_LIST_URL_NAME
    ),
    path(
        'process/full/',
        process.ListFull.as_view(),
        name='PROCESS_list_full'
    ),
    path(
        'process/create/',
        process.Create.as_view(),
        name=conf.PROCESS_CREATE_URL_NAME
    ),
    path(
        'process/<int:pk>/',
        process.Detail.as_view(),
        name=conf.PROCESS_DETAIL_URL_NAME
    ),
    path(
        'process/<int:pk>/update/',
        process.Update.as_view(),
        name=conf.PROCESS_UPDATE_URL_NAME
    ),
    path(
        'process/<int:pk>/delete/',
        process.Delete.as_view(),
        name=conf.PROCESS_DELETE_URL_NAME
    ),
    path(
        'process/list/json/',
        process.ProcessListJson.as_view(),
        name=conf.PROCESS_LIST_JSON_URL_NAME
    )
]

urlpatterns += api_urlpatterns
