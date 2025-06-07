from django.http import JsonResponse


def test_endpoint(request):
    return JsonResponse({"status": "success", "message": "API is working"})
