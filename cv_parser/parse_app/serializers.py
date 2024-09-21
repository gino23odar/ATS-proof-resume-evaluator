from rest_framework import serializers

class ExperienceSerializer(serializers.Serializer):
    employer_name = serializers.CharField()
    role = serializers.CharField()
    duration = serializers.CharField()

class ResumeDataSerializer(serializers.Serializer):
    applicant_name = serializers.CharField()
    highest_level_of_education = serializers.CharField()
    area_of_study = serializers.CharField()
    institution = serializers.CharField()
    introduction = serializers.CharField()
    skills = serializers.ListField(child=serializers.CharField())
    english_proficiency_level = serializers.CharField()
    experiences = serializers.ListField(child=ExperienceSerializer())

class ResumeInsightsSerializer(serializers.Serializer):
    matched_skills = serializers.ListField(child=serializers.CharField())
    important_skills_missing = serializers.ListField(child=serializers.CharField())
    improved_descriptions = serializers.CharField()
    general_improvements = serializers.CharField()
    things_to_remove = serializers.CharField()
    things_to_add = serializers.CharField()
    resume_score = serializers.IntegerField(min_value=0, max_value=100)