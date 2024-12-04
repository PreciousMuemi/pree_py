from django.contrib import admin
from .models import SkillCategory, Skill, CustomUser, UserSkill, UserLearningInterest, SkillExchange, Feedback, Tag

admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(CustomUser)
admin.site.register(UserSkill)
admin.site.register(UserLearningInterest)
admin.site.register(SkillExchange)
admin.site.register(Feedback)
admin.site.register(Tag)