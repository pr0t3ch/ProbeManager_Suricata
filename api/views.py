from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from core.utils import create_deploy_rules_task, create_check_task
import logging

from django_celery_beat.models import PeriodicTask, CrontabSchedule

from suricata.api import serializers
from suricata.models import Suricata, Configuration, SignatureSuricata, ScriptSuricata, SourceSuricata, RuleSetSuricata

logger = logging.getLogger(__name__)


class ConfigurationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Configuration.objects.all()
    serializer_class = serializers.ConfigurationSerializer


class SuricataViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Suricata.objects.all()
    serializer_class = serializers.SuricataSerializer

    def create(self, request):
        serializer = serializers.SuricataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            suricata = Suricata.get_by_name(request.data['name'])
            logger.debug("create scheduled for " + str(suricata))
            create_deploy_rules_task(suricata)
            create_check_task(suricata)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        suricata = self.get_object()
        try:
            periodic_task = PeriodicTask.objects.get(
                name=suricata.name + "_deploy_rules_" + str(suricata.scheduled_rules_deployment_crontab))
            periodic_task.delete()
            logger.debug(str(periodic_task) + " deleted")
        except PeriodicTask.DoesNotExist:  # pragma: no cover
            pass
        try:
            periodic_task = PeriodicTask.objects.get(name=suricata.name + "_check_task")
            periodic_task.delete()
            logger.debug(str(periodic_task) + " deleted")
        except PeriodicTask.DoesNotExist:  # pragma: no cover
            pass
        suricata.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SuricataUpdateViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Suricata.objects.all()
    serializer_class = serializers.SuricataUpdateSerializer

    def update(self, request, pk=None):
        bro = self.get_object()
        serializer = serializers.SuricataUpdateSerializer(bro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignatureSuricataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SignatureSuricata.objects.all()
    serializer_class = serializers.SignatureSuricataSerializer


class ScriptSuricataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ScriptSuricata.objects.all()
    serializer_class = serializers.ScriptSuricataSerializer


class SourceSuricataViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SourceSuricata.objects.all()
    serializer_class = serializers.SourceSuricataSerializer


class RuleSetSuricataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = RuleSetSuricata.objects.all()
    serializer_class = serializers.RuleSetSuricataSerializer
