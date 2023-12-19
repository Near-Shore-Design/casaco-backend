from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TourSerializer, PropertyToursSerializer
from properties.models import Property
from tours.func import send_email
from tours.models import Tour

class RequestTour(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = TourSerializer

    def get(self, request, *args, **kwargs):
        serializer = PropertyToursSerializer
        property_tours = []
        property_id = request.GET.get("property_id")
        try:
            if not property_id:
                return Response({"message": "property_id is required field"}, status=400)
            property_tour=Tour.objects.filter(property_id=property_id)
        except (Tour.DoesNotExist, ValueError, TypeError, OverflowError) as exc:
            return Response({"message": "No tour is scheduled against this property"}, status=200)
        
        queryset = property_tour
            
        for tour in queryset:
            property_tours.append({"scheduled_date": tour.scheduled_date.strftime('%d/%m/%Y'), "scheduled_time": tour.scheduled_time.strftime('%H:%M:%S'), "property_id": tour.property_id.property_id, "tour_id":tour.tour_id})
        

        
        return Response({"message": property_tours}, status=200)
        

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        serializer.save()
        user_id = data.get('user_id')
        property_id = data.get('property_id')
        scheduled_date = data.get('scheduled_date')
        scheduled_time = data.get('scheduled_time')

        try:
            selected_property = property_id
            user = user_id
            try:
                send_email(user, selected_property, scheduled_date, scheduled_time)
            except Exception as exc:
                content = {'message': f"{exc}"}
                return Response(content, status=400)
            content = {'message': 'Tour has been scheduled successfully.'}
            return Response(content, status=200)
        except Property.DoesNotExist:
            content = {'message': 'Property id is invalid.'}
            return Response(content, status=200)
        except get_user_model().DoesNotExist:
            content = {'message': 'User id is invalid.'}
            return Response(content, status=200)

    def get_authenticators(self):
        if self.request and (self.request.method == 'POST'):
            return [JWTAuthentication()]
        return []

    def get_permissions(self):
        if self.request and  (self.request.method == 'POST'):
            return [IsAuthenticated()]
        return []