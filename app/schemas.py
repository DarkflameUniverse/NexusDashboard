from flask_marshmallow import Marshmallow
from app.models import (
    PlayKey,
    PetNames,
    Mail,
    UGC,
    PropertyContent,
    Property,
    CharacterXML,
    CharacterInfo,
    Account,
    AccountInvitation,
    ActivityLog,
    CommandLog
)
ma = Marshmallow()


class PlayKeySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlayKey
        include_relationships = False
        load_instance = True
        include_fk = True


class PetNamesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PetNames
        include_relationships = False
        load_instance = True
        include_fk = False


class MailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mail
        include_relationships = False
        load_instance = True
        include_fk = False


class UGCSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UGC
        include_relationships = False
        load_instance = True
        include_fk = False


class PropertyContentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PropertyContent
        include_relationships = True
        load_instance = True
        include_fk = True

    ugc = ma.Nested(UGCSchema)


class PropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Property
        include_relationships = False
        load_instance = True
        include_fk = False

    properties_contents = ma.Nested(PropertyContentSchema, many=True)


class CharacterXMLSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CharacterXML
        include_relationships = False
        load_instance = True
        include_fk = False


class CharacterInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CharacterInfo
        include_relationships = False
        load_instance = True
        include_fk = False

    charxml = ma.Nested(CharacterXMLSchema)
    properties_owner = ma.Nested(PropertySchema, many=True)
    pets = ma.Nested(PetNamesSchema, many=True)
    mail = ma.Nested(MailSchema, many=True)


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        include_relationships = False
        load_instance = True
        include_fk = False

    play_key = ma.Nested(PlayKeySchema)
    charinfo = ma.Nested(CharacterInfoSchema, many=True)


class AccountInvitationSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = AccountInvitation
        include_relationships = True
        load_instance = True
        include_fk = True

    invite_by_user = ma.Nested(AccountSchema)


class ActivityLogSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = ActivityLog
        include_relationships = True
        load_instance = True
        include_fk = True

    character = ma.Nested(CharacterInfoSchema())


class CommandLogSchema(ma.SQLAlchemyAutoSchema): #  noqa
    class Meta:
        model = CommandLog
        include_relationships = True
        load_instance = True
        include_fk = True

    character = ma.Nested(CharacterInfoSchema())
