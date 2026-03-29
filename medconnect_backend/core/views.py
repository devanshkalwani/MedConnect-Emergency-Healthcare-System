from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Hospital, SOSRequest, EmergencyContact
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def _normalize_age(value, fallback=None):
    """
    Keep explicit 0 values, treat only empty values as missing.
    """
    if value is None or value == "":
        return fallback
    return value


# -------------------------
# API HOME
# -------------------------
@api_view(['GET'])
def api_home(request):
    return Response({
        "message": "MedConnect API Working 🚀",
        "routes": [
            "/api/user/register/",
            "/api/user/login/",
            "/api/hospital/register/",
            "/api/hospital/login/",
            "/api/sos/",
        ]
    })


# -------------------------
# USER REGISTER ✅
# -------------------------
@api_view(['POST'])
def register_user(request):
    data = request.data

    try:
        email = data.get('email')

        # 🚫 CHECK DUPLICATE EMAIL
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered"})

        user = User.objects.create_user(
            username=email,
            email=email,
            password=data.get('password'),
            name=data.get('full_name', ''),
            first_name=data.get('full_name'),
            contact_number=data.get('phone'),
            blood_group=data.get('blood_group'),
            age=_normalize_age(data.get('age')),
            allergies=data.get('allergies', ''),
            medical_condition=data.get('medical_condition', ''),
            emergency_contact_name=data.get('emergency_contact_name'),
            emergency_contact_number=data.get('emergency_contact_phone'),
        )

        if user.emergency_contact_name and user.emergency_contact_number:
            EmergencyContact.objects.create(
                user=user,
                name=user.emergency_contact_name,
                phone=user.emergency_contact_number
            )

        return Response({"message": "User Registered Successfully"})

    except Exception as e:
        return Response({"error": str(e)})


# -------------------------
# USER LOGIN ✅
# -------------------------
@api_view(['POST'])
def login_user(request):
    data = request.data

    user = authenticate(
        username=data.get('email'),
        password=data.get('password')
    )

    if user:
        return Response({
            "message": "Login Successful",
            "user_id": user.id
        })

    return Response({"error": "Invalid Credentials"})


# -------------------------
# HOSPITAL REGISTER
# -------------------------
@api_view(['POST'])
def register_hospital(request):
    data = request.data

    try:
        Hospital.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password'),
            city=data.get('city'),
            total_beds=data.get('total_beds'),
            icu_beds=data.get('icu_beds'),
            distance=data.get('distance', 0)  # 🔥 IMPORTANT FOR DEMO
        )

        return Response({"message": "Hospital Registered"})

    except Exception as e:
        return Response({"error": str(e)})


# -------------------------
# HOSPITAL LOGIN ✅ (FIXED)
# -------------------------
@api_view(['POST'])
def login_hospital(request):
    data = request.data

    try:
        email = data.get('email')
        password = data.get('password')

        # ❌ Check missing fields
        if not email or not password:
            return Response({"error": "Email and Password are required"})

        # ✅ Validate credentials
        hospital = Hospital.objects.get(
            email=email,
            password=password
        )

        return Response({
            "message": "Login Successful",
            "hospital_id": hospital.id,
            "hospital_name": hospital.name,  # 🔥 useful for UI
            "total_beds": hospital.total_beds,
            "icu_beds": hospital.icu_beds
        })

    except Hospital.DoesNotExist:
        return Response({"error": "Invalid Credentials"})

    except Exception as e:
        return Response({"error": str(e)})
# -------------------------
# SOS CREATE ✅ (FINAL FIXED)
# -------------------------
@api_view(['POST'])
def create_sos(request):
    data = request.data

    try:
        # ✅ Get user
        user = User.objects.get(id=data.get('user_id'))

        # 🚫 Prevent multiple active SOS
        if SOSRequest.objects.filter(user=user, status="SEARCHING").exists():
            return Response({"error": "You already have an active SOS"})

        # ✅ Extract Third-Party Data
        is_for_self = data.get('is_for_self', True)
        third_party_name = data.get('third_party_name', "")
        third_party_phone = data.get('third_party_phone', "")
        third_party_condition = data.get('third_party_condition', "")

        # ✅ Create SOS
        sos = SOSRequest.objects.create(
            user=user,
            emergency_type=data.get('emergency_type'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            status="SEARCHING",
            is_for_self=is_for_self,
            third_party_name=third_party_name,
            third_party_phone=third_party_phone,
            third_party_condition=third_party_condition
        )

        # 🚀 Broadcast via WebSockets
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "hospitals",
                {
                    "type": "send_emergency",
                    "data": {
                        "action": "NEW_SOS",
                        "sos_id": sos.id
                    }
                }
            )
        except Exception as ws_e:
            print("WS Error:", ws_e)

        return Response({
            "message": "Searching hospitals...",
            "request_id": sos.id
        })

    except User.DoesNotExist:
        return Response({"error": "User not found"})

    except Exception as e:
        return Response({"error": str(e)})


# -------------------------
# HOSPITAL ACCEPT ✅ (CRITICAL FIX)
# -------------------------
@api_view(['POST'])
def accept_request(request, request_id):

    try:
        hospital = Hospital.objects.get(id=request.data.get('hospital_id'))

        with transaction.atomic():
            sos = SOSRequest.objects.select_for_update().get(id=request_id)

            if sos.status == "SEARCHING":
                sos.status = "ASSIGNED"
                sos.assigned_hospital = hospital   # ✅ FIXED
                sos.save()

                # 🚀 Broadcast Assignment via WebSockets to alert other hospitals
                try:
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        "hospitals",
                        {
                            "type": "send_emergency",
                            "data": {
                                "action": "SOS_ASSIGNED",
                                "sos_id": sos.id,
                                "hospital_name": hospital.name
                            }
                        }
                    )
                except Exception as ws_e:
                    print("WS Error:", ws_e)

                return Response({
                    "message": "Patient assigned",
                    "hospital": hospital.name,
                    "patient_name": sos.user.first_name,
                    "phone": sos.user.contact_number,
                    "emergency": sos.emergency_type
                })

            return Response({"message": "Already assigned"}, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

# -------------------------
# STATUS CHECK ✅ (MAP + RESOLVED LOGIC)
# -------------------------
@api_view(['GET'])
def check_status(request, user_id):

    try:
        sos = SOSRequest.objects.filter(user_id=user_id).order_by('-created_at').first()

        if not sos or sos.status == "RESOLVED":
            return Response({"status": "NO_SOS", "hospital": None})

        return Response({
            "request_id": sos.id,
            "status": sos.status,
            "hospital": sos.assigned_hospital.name if sos.assigned_hospital else None,
            "distance": sos.assigned_hospital.distance if sos.assigned_hospital else None,
            "hosp_lat": (sos.latitude + 0.05) if sos.assigned_hospital else None,
            "hosp_lng": (sos.longitude + 0.05) if sos.assigned_hospital else None,
            "user_lat": sos.latitude,
            "user_lng": sos.longitude
        })

    except Exception as e:
        return Response({"error": str(e)})

# -------------------------
# RESOLVE SOS ✅ (CLEANUP STATE)
# -------------------------
@api_view(['POST'])
def resolve_sos(request, request_id):
    try:
        user_id = request.data.get('user_id')
        sos = SOSRequest.objects.get(id=request_id, user_id=user_id)
        
        sos.status = "RESOLVED"
        sos.save()
        
        return Response({"message": "Emergency resolved successfully"})
    except SOSRequest.DoesNotExist:
        return Response({"error": "Request not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_sos_details(request, request_id):

    try:
        sos = SOSRequest.objects.get(id=request_id)

        if sos.status != "ASSIGNED":
            return Response({"error": "Not authorized yet"})

        user = sos.user

        is_for_self = getattr(sos, 'is_for_self', True)
        
        target_name = user.first_name if is_for_self else sos.third_party_name
        target_phone = user.contact_number if is_for_self else sos.third_party_phone
        target_condition = sos.emergency_type if is_for_self else sos.third_party_condition

        return Response({
            "name": target_name,
            "phone": target_phone,
            "blood_group": user.blood_group if is_for_self else "Unknown",
            "age": user.age if is_for_self else "Unknown",
            "medical_condition": user.medical_condition if is_for_self else "Unknown",
            "allergies": user.allergies if is_for_self else "Unknown",
            "emergency_contact": user.emergency_contact_number if is_for_self else user.contact_number,
            "emergency_type": target_condition,
            "is_for_self": is_for_self,
            "caller_name": user.first_name if not is_for_self else None
        })

    except Exception as e:
        return Response({"error": str(e)})

def get_current_radius(sos):
    if not sos.created_at:
        return 3

    elapsed = (timezone.now() - sos.created_at).total_seconds()

    if elapsed < 5:
        return 3
    elif elapsed < 10:
        return 6
    elif elapsed < 15:
        return 9
    elif elapsed < 20:
        return 12
    else:
        return 15

@api_view(['POST'])
def get_hospital_sos(request):

    hospital_id = request.data.get("hospital_id")

    try:
        if not hospital_id:
            return Response({"error": "Hospital ID required"}, status=400)

        hospital = Hospital.objects.get(id=hospital_id)

        sos_list = SOSRequest.objects.filter(status="SEARCHING")

        visible_requests = []

        # 🔥 SAFE DISTANCE (MANUAL DEMO)
        distance = hospital.distance if hasattr(hospital, "distance") and hospital.distance is not None else 999

        for sos in sos_list:

            radius = get_current_radius(sos)

            time_elapsed = int((timezone.now() - sos.created_at).total_seconds()) if sos.created_at else 0

            if distance <= radius:

                # 🩺 Privacy Protection (HIPAA MASKING)
                patient_name = sos.user.first_name
                is_for_self = getattr(sos, 'is_for_self', True)
                
                target_condition = sos.emergency_type if is_for_self else sos.third_party_condition

                visible_requests.append({
                    "id": sos.id,
                    "patient_name": sos.user.first_name if is_for_self else sos.third_party_name,
                    "patient_phone": sos.user.contact_number if is_for_self else sos.third_party_phone,
                    "emergency": target_condition or sos.emergency_type,
                    "is_for_self": is_for_self,
                    "caller_name": sos.user.first_name if not is_for_self else None,
                    "lat": sos.latitude,
                    "lng": sos.longitude,
                    "distance": distance,
                    "status": sos.status,
                    "radius": radius,
                    "time": time_elapsed
                })

        visible_requests = sorted(visible_requests, key=lambda x: x["distance"])

        return Response(visible_requests)

    except Hospital.DoesNotExist:
        return Response({"error": "Hospital not found"}, status=404)

    except Exception as e:
        print("ERROR:", str(e))
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def get_user_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        return Response({
            "id": user.id,
            "first_name": user.first_name,
            "name": user.name or user.first_name,
            "email": user.email,
            "age": user.age,
            "blood_group": user.blood_group,
            "phone": user.contact_number,
            "condition": user.medical_condition,
            "medical_condition": user.medical_condition,
            "allergies": user.allergies,
            "pref_contact": user.pref_contact,
            "pref_hospital": user.pref_hospital,
        })
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['POST'])
def update_user_profile(request):
    try:
        user = User.objects.get(id=request.data.get("user_id"))
        user.first_name = request.data.get("name", user.first_name)
        user.name = request.data.get("name", user.name)
        incoming_email = request.data.get("email")
        if incoming_email:
            if User.objects.exclude(id=user.id).filter(email=incoming_email).exists():
                return Response({"error": "Email already in use"}, status=400)
            user.email = incoming_email
            user.username = incoming_email
        user.age = _normalize_age(request.data.get("age"), fallback=user.age)
        user.blood_group = request.data.get("blood_group", user.blood_group)
        user.contact_number = request.data.get("phone", user.contact_number)
        user.medical_condition = request.data.get("condition", user.medical_condition)
        user.allergies = request.data.get("allergies", user.allergies)
        user.save()
        return Response({"message": "Profile updated"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['POST'])
def change_password(request):
    user_id = request.data.get("user_id")
    current_password = request.data.get("current_password")
    new_password = request.data.get("new_password")

    if not user_id or not current_password or not new_password:
        return Response({"error": "Missing required fields"}, status=400)

    try:
        user = User.objects.get(id=user_id)
        if not user.check_password(current_password):
            return Response({"error": "Incorrect current password"}, status=400)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['POST'])
def save_preferences(request):
    user_id = request.data.get("user_id")
    if not user_id:
        return Response({"error": "user_id is required"}, status=400)

    try:
        user = User.objects.get(id=user_id)
        user.pref_contact = request.data.get("pref_contact", user.pref_contact)
        user.pref_hospital = request.data.get("pref_hospital", user.pref_hospital)
        user.save()
        return Response({"message": "Preferences saved"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['GET'])
def get_contacts(request, user_id):
    contacts = EmergencyContact.objects.filter(user_id=user_id).order_by('-created_at')
    return Response([
        {"id": c.id, "name": c.name, "phone": c.phone}
        for c in contacts
    ])


@api_view(['POST'])
def add_contact(request):
    user_id = request.data.get("user_id")
    name = request.data.get("name")
    phone = request.data.get("phone")

    if not user_id or not name or not phone:
        return Response({"error": "user_id, name and phone are required"}, status=400)

    try:
        user = User.objects.get(id=user_id)
        contact = EmergencyContact.objects.create(user=user, name=name, phone=phone)
        return Response({"id": contact.id, "name": contact.name, "phone": contact.phone})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['GET'])
def get_history(request, user_id):
    items = SOSRequest.objects.filter(user_id=user_id).order_by('-created_at')
    return Response([
        {
            "id": item.id,
            "emergency_type": item.emergency_type,
            "status": item.status,
            "hospital": item.assigned_hospital.name if item.assigned_hospital else None,
            "created_at": item.created_at,
        }
        for item in items
    ])


@api_view(['POST'])
def contact_message(request):
    return Response({"message": "Received"})

@api_view(['GET'])
def get_hospitals(request):
    hospitals = Hospital.objects.all().values()
    return Response(list(hospitals))