from django.http import JsonResponse

def ratelimit_error(request, exception):
  return JsonResponse(
    {
      "result": False,
      "reason": "Too many request"
    }, status=429
  )