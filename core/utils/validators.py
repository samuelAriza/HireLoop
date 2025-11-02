from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class SkillValidator:
    """Validator for skills field."""

    def __call__(self, value):
        if value:
            skill_list = [skill.strip() for skill in value.split(",") if skill.strip()]
            if len(skill_list) > 20:
                raise ValidationError(_("You cannot have more than 20 skills"))