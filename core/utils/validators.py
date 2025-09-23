from django.core.exceptions import ValidationError


class SkillValidator:
    """Validator for skills field."""

    def __call__(self, value):
        if value:
            skill_list = [skill.strip() for skill in value.split(",") if skill.strip()]
            if len(skill_list) > 20:
                raise ValidationError("You cannot have more than 20 skills")
