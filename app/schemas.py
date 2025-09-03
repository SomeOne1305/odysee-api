from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    email = fields.Email(required=True)


class VerifySchema(Schema):
    email = fields.Email(required=True)
    token = fields.String(required=True)


class CreateUserSchema(Schema):
    email = fields.Email(required=True)
    token = fields.String(required=True)
    username = fields.String(
        required=True,
        validate=validate.Regexp(
            r"^[a-zA-Z0-9_]+$",
            error="Username must contain only letters, numbers, and underscores (_).",
        ),
    )
    password = fields.String(
        required=True,
        validate=validate.Length(
            min=8, error="Password must be at least 8 characters long."
        ),
    )
    profile_img = fields.String()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)

class LoginUserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UpdateUserSchema(Schema):
    first_name = fields.String(required=False, validate=validate.Length(min=1, max=40))
    last_name = fields.String(required=False, validate=validate.Length(min=1, max=40))
    cover = fields.String(required=False, validate=validate.Length(min=1))


class CreateContentSchema(Schema):
    video = fields.String()
    thumbnail = fields.String()
    description = fields.String(required=False, validate=validate.Length(min=10, max=255))
    title = fields.String(required=True, validate=validate.Length(min=10, max=80))
    tags = fields.List(fields.UUID(),required=True)
class CreateTagScheme(Schema):
    title = fields.String(required=True, validate=validate.Length(min=3, max=20))

class CreateComment(Schema):
    text = fields.String(required=True, validate=validate.Length(min=1, max=256))