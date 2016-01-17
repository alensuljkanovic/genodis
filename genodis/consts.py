__author__ = 'Alen Suljkanovic'

SRC_GEN_PATH = "src-gen"
TEMPLATES_PATH = "templates"
DJANGO_TEMPLATES = "django"

DJANGO_DESTINATION = "django"

PROPERTY_TYPES = ["string", "text", "int", "float", "decimal", "datetime",
                  "date", "choice", "calculated_field"]


FOREIGN_KEY = "FK"
ONE_TO_ONE = "1..1"
ONE_TO_MANY = "1..*"
MANY_TO_MANY = "*..*"
MANY_TO_ONE = "*..1"
