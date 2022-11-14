from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from pullgerInternalControl.pullgerDataSynchronization.REST.logging import logger

from pullgerDataSynchronization import apiDS


class DataSynchronizationPing(APIView):
    permission_classes = (AllowAny, )
    http_method_names = ('get',)

    # serializer_class
    # queryset

    def get(self, request):

        content = {
            'message': None,
            'error': None
        }

        try:
            content['message'] = 'Pong: Thread Task'
            # from pullgerReflection import com_linkedin__TT
        except BaseException as e:
            logRecord = logger.info(
                msgt=f"{str(e)}",
                msg_public="Internal server error."
            )
            content['message'] = 'ERROR'
            content['error'] = logRecord.msg_public
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            content['message'] = 'Pong: Thread Task'
            statusResponse = status.HTTP_200_OK

        return Response(content, status=statusResponse)


class TaskSendAllForProcessing(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = "post"
    logger = logger
    # serializer_class
    # queryset

    def post(self, request, *args, **kwargs):
        content = {
            'message': None,
        }

        try:
            param_filter = request.query_params.get('filter')
            param_limit = request.query_params.get('limit')
            if param_filter is None or param_filter == 'all':
                amount = apiDS.send_all_task_for_processing(limit=param_limit)
            else:
                raise BaseException("Incorrect parameter 'filter'")
        except BaseException as e:
            logRecord = self.logger.info(
                msg_=f"{str(e)}",
                msg_public="Internal server error."
            )
            content['message'] = 'Pong: Thread Task'
            content['error'] = logRecord.msg_public
            statusResponse = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            content['message'] = f"Thread [{amount}] tasks sanded for processing."
            statusResponse = status.HTTP_200_OK

        return Response(content, status=statusResponse)
