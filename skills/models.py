from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert')
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):

        return f"{self.name} ({self.get_difficulty_display()})"
        from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
      bio = models.TextField(max_length=500, blank=True)
      location = models.CharField(max_length=200, blank=True)
      profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
      reputation_score = models.IntegerField(default=0)

      skills_offered = models.ManyToManyField(Skill, related_name='skill_providers', through='UserSkill')
      skills_desired = models.ManyToManyField(Skill, related_name='skill_learners', through='UserLearningInterest')

      groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
      user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

      def calculate_reputation(self):
          # Complex reputation calculation logic
          pass
class UserSkill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    verified = models.BooleanField(default=False)

class UserLearningInterest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

class SkillExchange(models.Model):
    STATUS_CHOICES = [
        ('proposed', 'Proposed'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    proposer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='proposed_exchanges')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_exchanges')
    proposed_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='proposed_in_exchanges')
    desired_skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='desired_in_exchanges')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='proposed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Feedback(models.Model):
    exchange = models.OneToOneField(SkillExchange, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


