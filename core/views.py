from django.http import JsonResponse
from django.shortcuts import render , get_object_or_404
from core.models import Testing
from core.serializers import TestingSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def testing_view(request):
    
    data = Testing.objects.all()
    serializer = TestingSerializer(data, many=True)

    return Response(serializer.data)
def health_check(request):
    return JsonResponse ({'status': 'OK'})

def testing_detail_view(request, id):
    test_data = get_object_or_404(Testing, id=id)
    serializer = TestingSerializer(test_data, many=True)
    return Response(serializer.test_data, safe=False)