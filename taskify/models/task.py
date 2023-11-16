from django.db import models

from taskify.validators import JSONSchemaValidator


class TaskStatus(models.TextChoices):
    CREATED = "Created"
    OPENED = "Opened"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=TaskStatus.choices, default=TaskStatus.CREATED
    )
    dynamic_fields = models.JSONField(
        default=list,
        null=False,
        blank=True,
        validators=[
            JSONSchemaValidator(
                {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "oneOf": [
                            {
                                "properties": {
                                    "name": {"type": "string"},
                                    "type": {"const": "int"},
                                    "value": {"type": "integer"},
                                },
                                "additionalProperties": False,
                            },
                            {
                                "properties": {
                                    "name": {"type": "string"},
                                    "type": {"const": "text"},
                                    "value": {"type": "string"},
                                },
                                "additionalProperties": False,
                            },
                            {
                                "properties": {
                                    "name": {"type": "string"},
                                    "type": {"const": "date"},
                                    "value": {"type": "string", "format": "date"},
                                },
                                "additionalProperties": False,
                            },
                            {
                                "properties": {
                                    "name": {"type": "string"},
                                    "type": {"const": "user"},
                                    "value": {"type": "string"},
                                },
                                "additionalProperties": False,
                            },
                        ],
                        "required": ["name", "type", "value"],
                    },
                }
            )
        ],
    )

    class Meta:
        ordering = ("-id",)

    def __str__(self) -> str:
        return self.name
