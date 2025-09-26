from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.db.models import Count, Q
from .models import *

# --- Existing Views for fetching data ---

class LatestCarsView(generics.ListAPIView):
    queryset = Car.objects.order_by('-release_date')[:10]
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]

class CarDetailView(generics.RetrieveAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]
class FeaturedCarsView(generics.ListAPIView):
    """
    Provides a list of up to 5 cars that are marked as featured.
    """
    queryset = Car.objects.filter(is_featured=True, published=True, sold=False).order_by('-updated_at')[:5]
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]

class AllCarsView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = {
        'maker__name': ['exact'],
        'model__name': ['exact'],
        'city__name': ['exact'],
        'year': ['gte', 'lte'],
        'price': ['gte', 'lte'],
        'Category__name': ['exact'],
    }
    
class AllCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CarStatisticsView(APIView):
    """
    Provides statistics for a single car, such as likes and enquiries.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        # 1. Get the specific car instance, or return a 404 error if it doesn't exist.
        car = get_object_or_404(Car, id=id)

        # 2. Calculate statistics by querying the related CarActivity model.
        #    - Count how many related activities have 'liked' set to True.
        total_likes = car.activities.filter(liked=True).count()
        
        #    - Count how many related activities have 'email_enquiry' set to True.
        total_enquiries = car.activities.filter(email_enquiry=True).count()
        
        # 3. Assemble the data into a dictionary for the JSON response.
        data = {
            'car_id': car.id,
            'total_likes': total_likes,
            'total_enquiries': total_enquiries,
        }
        
        # 4. Return the statistics as a successful response.
        return Response(data, status=status.HTTP_200_OK)

class AllMakersView(generics.ListAPIView):
    queryset = Maker.objects.all().order_by('name')
    serializer_class = MakerSerializer
    permission_classes = [permissions.AllowAny]

class AllModelsView(generics.ListAPIView):
    queryset = ModelName.objects.all().order_by('name')
    serializer_class = ModelNameSerializer
    permission_classes = [permissions.AllowAny]

class AllCitiesView(generics.ListAPIView):
    queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

# --- NEW: Views to handle user actions (Like, Enquire, Mark Sold) ---

class CarLikeView(APIView):
    """
    Handles the logic when a user clicks the 'Like' button.
    It finds or creates a CarActivity record and toggles the 'liked' status.
    """
    permission_classes = [permissions.IsAuthenticated] # Ensures only logged-in users can like.

    def post(self, request, id):
        # 1. Find the car the user is interacting with.
        car = get_object_or_404(Car, id=id)
        
        # 2. Look for an existing CarActivity for this user and this car.
        #    If one doesn't exist, create it. This is the key step.
        activity, created = CarActivity.objects.get_or_create(user=request.user, Car=car)
        
        # 3. Toggle the 'liked' field. If it was True, it becomes False, and vice-versa.
        activity.liked = not activity.liked
        
        # 4. Save the change to the database.
        activity.save()
        
        # 5. Send a response back to the frontend confirming the new status.
        return Response({'liked': activity.liked}, status=status.HTTP_200_OK)


class CarEnquiryView(APIView):
    """
    Handles the logic when a user clicks the 'Enquire' button.
    It finds or creates a CarActivity record and marks an enquiry as made.
    """
    permission_classes = [permissions.IsAuthenticated] # Ensures only logged-in users can enquire.

    def post(self, request, id):
        # 1. Find the car.
        car = get_object_or_404(Car, id=id)
        
        # 2. Get or create the activity record.
        activity, created = CarActivity.objects.get_or_create(user=request.user, Car=car)
        
        # 3. Check if an enquiry has already been made to prevent spam.
        if not activity.email_enquiry:
            # 4. If not, mark the enquiry as True and record the current time.
            activity.email_enquiry = True
            activity.enquiry_date = timezone.now()
            activity.save()
            
            # --- ADDED: Send an email notification to the car seller ---
            try:
                subject = f"New Enquiry for Your Car: {car.title}"
                message = (
                    f"Hello {car.agent.first_name},\n\n"
                    f"You have received a new enquiry for your car listing on our platform.\n\n"
                    f"Car Details:\n"
                    f"  - Title: {car.title}\n"
                    f"  - Year: {car.year}\n"
                    f"  - Price: ${car.price}\n\n"
                    f"Enquirer's Details:\n"
                    f"  - Name: {request.user.first_name} {request.user.last_name}\n"
                    f"  - Email: {request.user.email}\n\n"
                    f"They are interested in your vehicle. Please log in to your account to follow up.\n\n"
                    f"Thank you,\nThe CarList Zimbabwe Team"
                )
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [car.agent.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Optional: Log the error, but don't crash the request if email fails.
                print(f"Error sending email: {e}")
                pass
            # ----------------------------------------------------------------

            # 5. Send a success response.
            return Response({'detail': 'Enquiry sent successfully.'}, status=status.HTTP_200_OK)
        
        # 6. If an enquiry was already made, inform the user.
        return Response({'detail': 'You have already sent an enquiry for this car.'}, status=status.HTTP_400_BAD_REQUEST)


class CarMarkSoldView(APIView):
    """
    Handles toggling the 'sold' status on the Car model itself.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        car = get_object_or_404(Car, id=id)

        # Security check: Only the user who created the listing can mark it as sold.
        if car.agent != request.user:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
            
        car.sold = not car.sold
        car.save()

        return Response({'sold': car.sold}, status=status.HTTP_200_OK)

# --- ADDED: Views for users to manage their own car listings ---

class UserCarsView(generics.ListCreateAPIView):
    """
    GET: Returns a list of cars owned by the currently authenticated user.
    POST: Creates a new car listing for the currently authenticated user.
    """
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """This view should return a list of all the cars
        for the currently authenticated user."""
        return Car.objects.filter(agent=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Assign the logged-in user as the agent of the new car."""
        serializer.save(agent=self.request.user)


class UserCarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles retrieving, updating, and deleting a specific car
    owned by the authenticated user.
    """
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        """
        This view should return a car instance owned by the
        currently authenticated user.
        """
        return Car.objects.filter(agent=self.request.user)


class CarTypeWithCountView(generics.ListAPIView):
    """
    Provides a list of all car types, annotated with the count of active cars.
    """
    serializer_class = CarTypeSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # NOTE: Using 'car_set' which is the Django default reverse lookup name.
        # If you set a `related_name` on the ForeignKey in your Car model, update this string.
        return CarType.objects.annotate(
            car_count=Count('car', filter=Q(car__published=True, car__sold=False))
        ).order_by('-car_count')
class MakerWithCountView(generics.ListAPIView):
    """
    Corresponds to getMakersWithCount().
    Provides a list of all car makers, annotated with the count of active cars.
    """
    serializer_class = MakerWithCountSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Maker.objects.annotate(
            car_count=Count('car', filter=Q(car__published=True, car__sold=False))
        ).order_by('-car_count')
