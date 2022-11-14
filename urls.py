from django.urls import path
from pullgerDataSynchronization__REST import apiREST


urlpatterns = [
    path('ping', apiREST.DataSynchronizationPing.as_view()),
    path('task/send-for-processing', apiREST.TaskSendAllForProcessing.as_view()),
]