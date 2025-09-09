import uuid
from django.db import models
from django.conf import settings



class CarType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., Sedan, SUV, Bike, Boat, Trailer

    def __str__(self):
        return self.name


class FuelType(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., Petrol, Diesel, Electric

    def __str__(self):
        return self.name


class Maker(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., Toyota, Honda

    def __str__(self):
        return self.name


class ModelName(models.Model):
    maker = models.ForeignKey(Maker, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)  # e.g., Corolla, Civic

    class Meta:
        unique_together = ('maker', 'name')

    def __str__(self):
        return f"{self.maker.name} {self.name}"


class Province(models.Model):
    name = models.CharField(max_length=100)  # e.g., Harare Province

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)  # e.g., Harare

    def __str__(self):
        return f"{self.name}, {self.state.name}"

class CarBadge(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    Category_CHOICES = [
        ('bikes', 'bikes'),
        ('trailers', 'trailers'),
        ('boats', 'boats'),
        ('vehicles', 'vehicles'),
        
    ]
    name = models.CharField(max_length=255, choices=Category_CHOICES, unique=True)

    def __str__(self):
        return self.name
    
    



class Car(models.Model):
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Cars')
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    Category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    maker = models.ForeignKey(Maker, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(ModelName, on_delete=models.SET_NULL, null=True)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, null=True)


    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.PositiveIntegerField(help_text="Mileage in km")
    transmission = models.CharField(max_length=50, choices=[('manual', 'Manual'), ('automatic', 'Automatic')])
    color = models.CharField(max_length=50, blank=True, null=True)
    published = models.BooleanField(default=False) 

    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    is_featured = models.BooleanField(default=False)
    featured_until = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    badges = models.ManyToManyField(CarBadge, related_name='cars', blank=True)
    

    def __str__(self):
        return f"{self.maker} {self.model} ({self.year})"
    
    @property
    def main_image(self):
        main_img = self.images.filter(is_main=True).first()
        if main_img:
            return main_img.image.url
        return '../../media/car_images/1.jpeg'  # fallback image
  
    @property
    def total_bids(self):
        return self.activities.exclude(email_enquiry__isnull=True).count()

    @property
    def current_supporters(self):
        return self.activities.filter(email_enquiry__isnull=False).values('user').distinct().count()

class CarActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Car_activities')
    Car = models.ForeignKey('Car', on_delete=models.CASCADE, related_name='activities')
    liked = models.BooleanField(default=False)
    email_enquiry = models.BooleanField(default=False)
    enquiry_date = models.DateTimeField(auto_now_add=True)
    equiry_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'Car')

    def __str__(self):
        return f"{self.user.username} on {self.Car.title} (Liked: {self.liked}, Enquiry: {self.email_enquiry})"

class CarFeature(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="features")
    name = models.CharField(max_length=100)  # e.g., Air Conditioning, Sunroof

    def __str__(self):
        return self.name


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="car_images/")
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.car}"