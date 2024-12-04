from django.db.models import Q
from typing import List, Dict
from .models import CustomUser  # Ensure you import your CustomUser model

class SkillMatchingEngine:

    @classmethod
    def find_matches(cls, user, max_matches=10) -> List[Dict]:
        """
        Advanced skill matching algorithm considering multiple factors
        """
        user_learning_interests = user.skills_desired.all()
        user_offered_skills = user.skills_offered.all()

        potential_matches = (
            CustomUser.objects
            .exclude(id=user.id)  # Exclude current user
            .filter(
                Q(skills_offered__in=user_learning_interests) &
                Q(skills_desired__in=user_offered_skills)
            )
            .distinct()
        )

        scored_matches = []
        for match in potential_matches:
            match_score = cls._calculate_match_score(user, match)
            scored_matches.append({
                'user': match,
                'score': match_score,
                'compatible_skills': cls._get_compatible_skills(user, match)
            })

        return sorted(scored_matches, key=lambda x: x['score'], reverse=True)[:max_matches]

    @classmethod
    def _calculate_match_score(cls, user_a, user_b) -> float:
        """
        Complex match scoring considering multiple dimensions
        """
        score = 0.0
        
        # Skill compatibility
        shared_skills = set(user_a.skills_offered.all()) & set(user_b.skills_desired.all())
        score += len(shared_skills) * 10

        # Location proximity (implement geolocation logic)
        score += cls._calculate_location_proximity(user_a, user_b)

        # Reputation and previous exchange success
        score += user_b.reputation_score * 0.1
        
        return score

    @classmethod
    def _get_compatible_skills(cls, user_a, user_b):
        """
        Identify and return compatible skill pairs
        """
        return [
            {
                'offered_skill': offered_skill,
                'desired_skill': desired_skill
            }
            for offered_skill in user_a.skills_offered.all()
            for desired_skill in user_b.skills_desired.all()
            if offered_skill == desired_skill
        ]

    @classmethod
    def _calculate_location_proximity(cls, user_a, user_b):
        """
        Placeholder for location-based matching logic
        In production, use geolocation libraries or services
        """
        # Basic implementation returning random proximity score
        if user_a.location == user_b.location:
            return 15.0
        return 5.0
