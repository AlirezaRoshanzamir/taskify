import django
from django.core.validators import BaseValidator
import jsonschema
    

class JSONSchemaValidator(BaseValidator):
    def compare(self, value, schema):
        try:
            jsonschema.validate(value, schema, format_checker=jsonschema.FormatChecker())
        except jsonschema.exceptions.ValidationError as e:
            raise django.core.exceptions.ValidationError(
                "JSON schema mismatch: %(detail)s.", params={"value": value, "detail": e.message}
            )
