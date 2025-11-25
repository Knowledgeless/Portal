import json
from django.http import JsonResponse
from django.conf import settings
import os


def load_bd_address():
    json_path = os.path.join(settings.BASE_DIR, "static/json/address.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


BD_ADDRESS = load_bd_address()


def api_divisions(request):
    """Return list of all divisions"""
    divisions = sorted(list(BD_ADDRESS.keys()))
    return JsonResponse({"divisions": divisions})


def api_districts(request):
    """Return all districts under a division"""
    division = request.GET.get("division")

    if not division or division not in BD_ADDRESS:
        return JsonResponse({"districts": []})

    districts = sorted(list(BD_ADDRESS[division].keys()))
    return JsonResponse({"districts": districts})


def api_upazilas(request):
    """Return all upazilas under district"""
    division = request.GET.get("division")
    district = request.GET.get("district")

    if (
        not division
        or division not in BD_ADDRESS
        or not district
        or district not in BD_ADDRESS[division]
    ):
        return JsonResponse({"upazilas": []})

    upazilas = BD_ADDRESS[division][district]
    return JsonResponse({"upazilas": upazilas})
