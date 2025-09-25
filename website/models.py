from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

     # 🌍 Add location fields here (belongs to the issue report)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    
class Bid(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bids")
    contractor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    proposal = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contractor.username} - {self.amount}"

# website/models.py
class Profile(models.Model):
    USER_ROLES = (
        ('citizen', 'Citizen'),
        ('contractor', 'Contractor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='citizen')

    def __str__(self):
        return f"{self.user.username} - {self.role}"        
    
    
    
