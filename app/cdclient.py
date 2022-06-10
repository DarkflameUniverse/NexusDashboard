from app import db
from sqlalchemy.dialects import sqlite
from sqlalchemy_utils import generic_relationship
import enum


class AICombatRoles(db.Model):
    __tablename__ = 'AICombatRoles'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    preferredRole = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    specifiedMinRangeNOUSE = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )
    specifiedMaxRangeNOUSE = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )
    specificMinRange = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )
    specificMaxRange = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )


class AccessoryDefaultLoc(db.Model):
    __tablename__ = 'AccessoryDefaultLoc'
    __bind_key__ = 'cdclient'

    GroupID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    Description = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    Pos_X = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    Pos_Y = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    Pos_Z = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    Rot_X = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    Rot_Y = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    Rot_Z = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )


class Activities(db.Model):
    __tablename__ = 'Activities'
    __bind_key__ = 'cdclient'

    ActivityID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    instanceMapID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    minTeams = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    maxTeams = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    minTeamSize = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    maxTeamSize = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    waitTime = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    startDelay = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    requiresUniqueData = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    leaderboardType = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    optionalCostLOT = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    optionalCostCount = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    showUIRewards = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    CommunityActivityFlagID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )

    noTeamLootOnDeath = db.Column(
        sqlite.BOOLEAN(),
        nullable=True
    )

    optionalPercentage = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )


class ActivityRewards(db.Model):
    __tablename__ = 'ActivityRewards'
    __bind_key__ = 'cdclient'

    objectTemplate = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    ActivityRewardIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    activityRating = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    LootMatrixIndex = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    CurrencyIndex = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    ChallengeRating = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class ActivityText(db.Model):
    __tablename__ = 'ActivityText'
    __bind_key__ = 'cdclient'

    activityID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Activities.ActivityID"),
        nullable=False,
        primary_key=True,
    )

    activity = db.relationship(
        'Activities',
        backref="ActivityText"
    )

    type = db.Column(
        sqlite.TEXT(),
        nullable=False,
        primary_key=True
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class AnimationIndex(db.Model):
    __tablename__ = 'AnimationIndex'
    __bind_key__ = 'cdclient'

    animationGroupID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    groupType = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class Animations(db.Model):
    __tablename__ = 'Animations'
    __bind_key__ = 'cdclient'

    animationGroupID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    animation_type = db.Column(
        sqlite.TEXT(),
        nullable=False,
        primary_key=True
    )

    animation_name = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    chance_to_play = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    min_loops = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    max_loops = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    animation_length = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    hideEquip = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    ignoreUpperBody = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    restartable = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    face_animation_name = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    priority = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    blendTime = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )


class BaseCombatAIComponent(db.Model):
    __tablename__ = 'BaseCombatAIComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    behaviorType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    combatRoundLength = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    combatRole = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    minRoundLength = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maxRoundLength = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    tetherSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    pursuitSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    combatStartDelay = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    softTetherRadius = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    hardTetherRadius = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    spawnTimer = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    tetherEffectID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    ignoreMediator = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    aggroRadius = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    ignoreStatReset = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    ignoreParent = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class BehaviorEffect(db.Model):
    __tablename__ = 'BehaviorEffect'
    __bind_key__ = 'cdclient'

    effectID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    effectType = db.Column(
        sqlite.TEXT(),
        nullable=False,
        primary_key=True
    )

    effectName = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    trailID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    pcreateDuration = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    animationName = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    attachToObject = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    boneName = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    useSecondary = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    cameraEffectType = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    cameraDuration = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    cameraFrequency = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    cameraXAmp = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    cameraYAmp = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    cameraZAmp = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    cameraRotFrequency = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    cameraRoll = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    cameraPitch = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    cameraYaw = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    AudioEventGUID = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    renderEffectType = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    renderEffectTime = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    renderStartVal = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    renderEndVal = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    renderDelayVal = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    renderValue1 = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    renderValue2 = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    renderValue3 = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    renderRGBA = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    renderShaderVal = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    motionID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    meshID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    meshDuration = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    meshLockedNode = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class BehaviorParameter(db.Model):
    __tablename__ = 'BehaviorParameter'
    __bind_key__ = 'cdclient'

    behaviorID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    parameterID = db.Column(
        sqlite.TEXT(),
        nullable=False,
        primary_key=True
    )

    value = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )


class BehaviorTemplate(db.Model):
    __tablename__ = 'BehaviorTemplate'
    __bind_key__ = 'cdclient'

    behaviorID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    templateID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    effectID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    effectHandle = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class BehaviorTemplateName(db.Model):
    __tablename__ = 'BehaviorTemplateName'
    __bind_key__ = 'cdclient'

    templateID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    name = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class Blueprints(db.Model):
    __tablename__ = 'Blueprints'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    name = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    accountid = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    characterid = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    price = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    rating = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    categoryid = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    lxfpath = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    deleted = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    created = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    modified = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class BrickColors(db.Model):
    __tablename__ = 'BrickColors'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    red = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    green = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    blue = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    alpha = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    legopaletteid = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    validTypes = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    validCharacters = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    factoryValid = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class BrickIDTable(db.Model):
    __tablename__ = 'BrickIDTable'
    __bind_key__ = 'cdclient'

    NDObjectID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    LEGOBrickID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )


class BuffDefinitions(db.Model):
    __tablename__ = 'BuffDefinitions'
    __bind_key__ = 'cdclient'

    ID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    Priority = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    UIIcon = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class BuffParameters(db.Model):
    __tablename__ = 'BuffParameters'
    __bind_key__ = 'cdclient'

    BuffID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    ParameterName = db.Column(
        sqlite.TEXT(),
        nullable=False,
        primary_key=True
    )

    NumberValue = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    StringValue = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    EffectID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )


class Camera(db.Model):
    __tablename__ = 'Camera'
    __bind_key__ = 'cdclient'

    camera_name = db.Column(
        sqlite.TEXT(),
        nullable=False,
        primary_key=True
    )

    pitch_angle_tolerance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    starting_zoom = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    zoom_return_modifier = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    pitch_return_modifier = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    tether_out_return_modifier = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    tether_in_return_multiplier = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    verticle_movement_dampening_modifier = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    return_from_incline_modifier = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    horizontal_return_modifier = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    yaw_behavior_speed_multiplier = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    camera_collision_padding = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    glide_speed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fade_player_min_range = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    min_movement_delta_tolerance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    min_glide_distance_tolerance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    look_forward_offset = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    look_up_offset = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    minimum_vertical_dampening_distance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maximum_vertical_dampening_distance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    minimum_ignore_jump_distance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maximum_ignore_jump_distance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maximum_auto_glide_angle = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    minimum_tether_glide_distance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    yaw_sign_correction = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    set_1_look_forward_offset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_1_look_up_offset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_2_look_forward_offset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_2_look_up_offset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_0_speed_influence_on_dir = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_1_speed_influence_on_dir = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_2_speed_influence_on_dir = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_0_angular_relaxation = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_1_angular_relaxation = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_2_angular_relaxation = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_0_position_up_offset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_1_position_up_offset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_2_position_up_offset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_0_position_forward_offset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_1_position_forward_offset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_2_position_forward_offset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_0_FOV = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_1_FOV = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_2_FOV = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_0_max_yaw_angle = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_1_max_yaw_angle = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_2_max_yaw_angle = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    set_1_fade_in_camera_set_change = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    set_1_fade_out_camera_set_change = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    set_2_fade_in_camera_set_change = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    set_2_fade_out_camera_set_change = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    input_movement_scalar = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    input_rotation_scalar = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    input_zoom_scalar = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    minimum_pitch_desired = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maximum_pitch_desired = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    minimum_zoom = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maximum_zoom = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    horizontal_rotate_tolerance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    horizontal_rotate_modifier = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )


class CelebrationParameters(db.Model):
    __tablename__ = 'CelebrationParameters'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    animation = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    backgroundObject = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )

    duration = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    subText = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    mainText = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    IconID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Icons.IconID"),
        nullable=False
    )

    Icon = db.relationship("Icons")

    celeLeadIn = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    celeLeadOut = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    cameraPathLOT = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    pathNodeName = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    ambientR = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    ambientG = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    ambientB = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    directionalR = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    directionalG = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    directionalB = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    specularR = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    specularG = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    specularB = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    lightPositionX = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    lightPositionY = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    lightPositionZ = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    blendTime = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    fogColorR = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    fogColorG = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    fogColorB = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    musicCue = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    soundGUID = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    mixerProgram = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class ChoiceBuildComponent(db.Model):
    __tablename__ = 'ChoiceBuildComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    # CSV of LOTS
    selections = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    imaginationOverride = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )


class CollectibleComponent(db.Model):
    __tablename__ = 'CollectibleComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    requirement_mission = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Missions.id"),
        nullable=True
    )


class ComponentsRegistry(db.Model):
    __tablename__ = 'ComponentsRegistry'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False,
        primary_key=True
    )

    component_type = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    component_id = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    component = generic_relationship(component_type, component_id)


# From DLU source
class ComponentType(enum.IntEnum):
    COMPONENT_TYPE_CONTROLLABLE_PHYSICS         = 1     # The ControllablePhysics Component
    COMPONENT_TYPE_RENDER                       = 2     # The Render Component
    COMPONENT_TYPE_SIMPLE_PHYSICS               = 3     # The SimplePhysics Component
    COMPONENT_TYPE_CHARACTER                    = 4     # The Character Component
    COMPONENT_TYPE_SCRIPT                       = 5     # The Script Component
    COMPONENT_TYPE_BOUNCER                      = 6     # The Bouncer Component
    COMPONENT_TYPE_BUFF                         = 7     # The Buff Component
    COMPONENT_TYPE_SKILL                        = 9     # The Skill Component
    COMPONENT_TYPE_ITEM                         = 11    # The Item Component
    COMPONENT_TYPE_VENDOR                       = 16    # The Vendor Component
    COMPONENT_TYPE_INVENTORY                    = 17    # The Inventory Component
    COMPONENT_TYPE_SHOOTING_GALLERY             = 19    # The Shooting Gallery Component
    COMPONENT_TYPE_RIGID_BODY_PHANTOM_PHYSICS   = 20    # The RigidBodyPhantomPhysics Component
    COMPONENT_TYPE_COLLECTIBLE                  = 23    # The Collectible Component
    COMPONENT_TYPE_MOVING_PLATFORM              = 25    # The MovingPlatform Component
    COMPONENT_TYPE_PET                          = 26    # The Pet Component
    COMPONENT_TYPE_VEHICLE_PHYSICS              = 30    # The VehiclePhysics Component
    COMPONENT_TYPE_MOVEMENT_AI                  = 31    # The MovementAI Component
    COMPONENT_TYPE_PROPERTY                     = 36    # The Property Component
    COMPONENT_TYPE_SCRIPTED_ACTIVITY            = 39    # The ScriptedActivity Component
    COMPONENT_TYPE_PHANTOM_PHYSICS              = 40    # The PhantomPhysics Component
    COMPONENT_TYPE_PROPERTY_ENTRANCE            = 43    # The PhantomPhysics Component
    COMPONENT_TYPE_PROPERTY_MANAGEMENT          = 45    # The PropertyManagement Component
    COMPONENT_TYPE_REBUILD                      = 48    # The Rebuild Component
    COMPONENT_TYPE_SWITCH                       = 49    # The Switch Component
    COMPONENT_TYPE_ZONE_CONTROL                 = 50    # The ZoneControl Component
    COMPONENT_TYPE_PACKAGE                      = 53    # The Package Component
    COMPONENT_TYPE_PLAYER_FLAG                  = 58    # The PlayerFlag Component
    COMPONENT_TYPE_BASE_COMBAT_AI               = 60    # The BaseCombatAI Component
    COMPONENT_TYPE_MODULE_ASSEMBLY              = 61    # The ModuleAssembly Component
    COMPONENT_TYPE_PROPERTY_VENDOR              = 65    # The PropertyVendor Component
    COMPONENT_TYPE_ROCKET_LAUNCH                = 67    # The RocketLaunch Component
    COMPONENT_TYPE_RACING_CONTROL               = 71    # The RacingControl Component
    COMPONENT_TYPE_MISSION_OFFER                = 73    # The MissionOffer Component
    COMPONENT_TYPE_EXHIBIT                      = 75    # The Exhibit Component
    COMPONENT_TYPE_RACING_STATS                 = 74    # The Exhibit Component
    COMPONENT_TYPE_SOUND_TRIGGER                = 77    # The Sound Trigger Component
    COMPONENT_TYPE_PROXIMITY_MONITOR            = 78    # The Proximity Monitor Component
    COMPONENT_TYPE_MISSION                      = 84    # The Mission Component
    COMPONENT_TYPE_ROCKET_LAUNCH_LUP            = 97    # The LUP Launchpad Componen
    COMPONENT_TYPE_RAIL_ACTIVATOR               = 104
    COMPONENT_TYPE_POSSESSOR                    = 107   # The Component 107
    COMPONENT_TYPE_POSSESSABLE                  = 108   # The Component 108
    COMPONENT_TYPE_BUILD_BORDER                 = 114   # The Build Border Component
    COMPONENT_TYPE_DESTROYABLE                  = 1000  # The Destroyable Component


class ControlSchemes(db.Model):
    __tablename__ = 'ControlSchemes'
    __bind_key__ = 'cdclient'

    control_scheme = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    scheme_name = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    rotation_speed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    walk_forward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    walk_backward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    walk_strafe_speed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    walk_strafe_forward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    walk_strafe_backward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    run_backward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    run_strafe_speed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    run_strafe_forward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    run_strafe_backward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    keyboard_zoom_sensitivity = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    keyboard_pitch_sensitivity = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    keyboard_yaw_sensitivity = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    mouse_zoom_wheel_sensitivity = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    x_mouse_move_sensitivity_modifier = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    y_mouse_move_sensitivity_modifier = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    freecam_speed_modifier = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    freecam_slow_speed_multiplier = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    freecam_fast_speed_multiplier = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    freecam_mouse_modifier = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    gamepad_pitch_rot_sensitivity = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    gamepad_yaw_rot_sensitivity = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    gamepad_trigger_sensitivity = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )


class CurrencyDenominations(db.Model):
    __tablename__ = 'CurrencyDenominations'
    __bind_key__ = 'cdclient'

    value = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True,
    )

    objectid = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )


class CurrencyTable(db.Model):
    __tablename__ = 'CurrencyTable'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    currencyIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    npcminlevel = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    minvalue = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    maxvalue = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class DBExclude(db.Model):
    __tablename__ = 'DBExclude'
    __bind_key__ = 'cdclient'

    table = db.Column(
        sqlite.TEXT(),
        nullable=False,
        primary_key=True
    )

    column = db.Column(
        sqlite.TEXT(),
        nullable=False,
        primary_key=True
    )


class DeletionRestrictions(db.Model):
    __tablename__ = 'DeletionRestrictions'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    restricted = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    # CSV of LOTS
    ids = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    checkType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class DestructibleComponent(db.Model):
    __tablename__ = 'DestructibleComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    faction = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Factions.faction"),
        nullable=True
    )

    # CSV of factions?
    factionList = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    life = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    imagination = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    LootMatrixIndex = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    CurrencyIndex = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    level = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    armor = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    death_behavior = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    isnpc = db.Column(
        sqlite.BOOLEAN(),
        nullable=True
    )

    attack_priority = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    isSmashable = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    difficultyLevel = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )


class DevModelBehaviors(db.Model):
    __tablename__ = 'DevModelBehaviors'
    __bind_key__ = 'cdclient'

    ModelID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    BehaviorID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )


class Emotes(db.Model):
    __tablename__ = 'Emotes'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    animationName = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    iconFilename = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    channel = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    command = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    locked = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class EventGating(db.Model):
    __tablename__ = 'EventGating'
    __bind_key__ = 'cdclient'

    eventName = db.Column(
        sqlite.TEXT(),
        nullable=False,
        primary_key=True
    )

    date_start = db.Column(
        sqlite.TIMESTAMP(),
        nullable=False
    )

    date_end = db.Column(
        sqlite.TIMESTAMP(),
        nullable=False
    )


class ExhibitComponent(db.Model):
    __tablename__ = 'ExhibitComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    length = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    width = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    height = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    offsetX = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    offsetY = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    offsetZ = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fReputationSizeMultiplier = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fImaginationCost = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )


class Factions(db.Model):
    __tablename__ = 'Factions'
    __bind_key__ = 'cdclient'

    faction = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    # CSV of factions
    factionList = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    factionListFriendly = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    # CSV of factions
    friendList = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    # CSV of factions
    enemyList = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class FeatureGating(db.Model):
    __tablename__ = 'FeatureGating'
    __bind_key__ = 'cdclient'

    featureName = db.Column(
        sqlite.TEXT(),
        nullable=False,
        primary_key=True
    )

    major = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    current = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    minor = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class FlairTable(db.Model):
    __tablename__ = 'FlairTable'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    asset = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class Icons(db.Model):
    __tablename__ = 'Icons'
    __bind_key__ = 'cdclient'

    IconID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    IconPath = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    IconName = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class InventoryComponent(db.Model):
    __tablename__ = 'InventoryComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    # LOT?
    itemid = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    count = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    equip = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class ItemComponent(db.Model):
    __tablename__ = 'ItemComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    equipLocation = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    baseValue = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    isKitPiece = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    rarity = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    itemType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    itemInfo = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    inLootTable = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    inVendor = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    isUnique = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    isBOP = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    isBOE = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    reqFlagID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    reqSpecialtyID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    reqSpecRank = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    reqAchievementID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    stackSize = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    color1 = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    decal = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    offsetGroupID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    buildTypes = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    reqPrecondition = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    animationFlag = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    equipEffects = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    readyForQA = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    itemRating = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    isTwoHanded = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    minNumRequired = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    delResIndex = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    currencyLOT = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    altCurrencyCost = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    subItems = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    audioEventUse = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    noEquipAnimation = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    commendationLOT = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    commendationCost = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    audioEquipMetaEventSet = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    currencyCosts = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    ingredientInfo = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    forgeType = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    SellMultiplier = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )


class ItemEggData(db.Model):
    __tablename__ = 'ItemEggData'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    # LOT?
    chassie_type_id = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class ItemFoodData(db.Model):
    __tablename__ = 'ItemFoodData'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    element_1 = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    element_1_amount = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    element_2 = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    element_2_amount = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    element_3 = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    element_3_amount = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    element_4 = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    element_4_amount = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class ItemSetSkills(db.Model):
    __tablename__ = 'ItemSetSkills'
    __bind_key__ = 'cdclient'

    SkillSetID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    SkillID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    SkillCastType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class ItemSets(db.Model):
    __tablename__ = 'ItemSets'
    __bind_key__ = 'cdclient'

    setID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # CSV of LOTS
    itemIDs = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    kitType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    kitRank = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    kitImage = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Icons.IconID"),
        nullable=True
    )

    skillSetWith2 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("ItemSetSkills.SkillSetID"),
        nullable=True
    )

    skillSetWith3 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("ItemSetSkills.SkillSetID"),
        nullable=True
    )

    skillSetWith4 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("ItemSetSkills.SkillSetID"),
        nullable=True
    )

    skillSetWith5 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("ItemSetSkills.SkillSetID"),
        nullable=True
    )

    skillSetWith6 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("ItemSetSkills.SkillSetID"),
        nullable=True
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )
    # ???
    kitID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    priority = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )


class JetPackPadComponent(db.Model):
    __tablename__ = 'JetPackPadComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    xDistance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    yDistance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    warnDistance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    lotBlocker = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=True
    )

    lotWarningVolume = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=True
    )


class LUPExhibitComponent(db.Model):
    __tablename__ = 'LUPExhibitComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    minXZ = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maxXZ = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maxY = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    offsetX = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    offsetY = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    offsetZ = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )


class LUPExhibitModelData(db.Model):
    __tablename__ = 'LUPExhibitModelData'
    __bind_key__ = 'cdclient'

    LOT = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False,
        primary_key=True
    )

    minXZ = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maxXZ = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maxY = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    owner = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class LUPZoneIDs(db.Model):
    __tablename__ = 'LUPZoneIDs'
    __bind_key__ = 'cdclient'

    zoneID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("ZoneTable.zoneID"),
        nullable=False,
        primary_key=True
    )


class LanguageType(db.Model):
    __tablename__ = 'LanguageType'
    __bind_key__ = 'cdclient'

    LanguageID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    LanguageDescription = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class LevelProgressionLookup(db.Model):
    __tablename__ = 'LevelProgressionLookup'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    requiredUScore = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    # BehaviorEffect ?
    BehaviorEffect = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class LootMatrix(db.Model):
    __tablename__ = 'LootMatrix'
    __bind_key__ = 'cdclient'

    # FK?
    LootMatrixIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK
    LootTableIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK
    RarityTableIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    percent = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    minToDrop = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    maxToDrop = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    flagID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class LootMatrixIndex(db.Model):
    __tablename__ = 'LootMatrixIndex'
    __bind_key__ = 'cdclient'

    LootMatrixIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    inNpcEditor = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class LootTable(db.Model):
    __tablename__ = 'LootTable'
    __bind_key__ = 'cdclient'

    # LOT
    itemid = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    LootTableIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    MissionDrop = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    sortPriority = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class LootTableIndex(db.Model):
    __tablename__ = 'LootTableIndex'
    __bind_key__ = 'cdclient'

    LootTableIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )


class MinifigComponent(db.Model):
    __tablename__ = 'MinifigComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    head = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    chest = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    legs = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("MinifigDecals_Legs.ID"),
        nullable=False
    )

    hairstyle = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    haircolor = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    chestdecal = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("MinifigDecals_Torsos.ID"),
        nullable=False
    )

    headcolor = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    lefthand = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    righthand = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    eyebrowstyle = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("MinifigDecals_Eyebrows.ID"),
        nullable=False
    )

    eyesstyle = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("MinifigDecals_Eyes.ID"),
        nullable=False
    )

    mouthstyle = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("MinifigDecals_Mouths.ID"),
        nullable=False
    )


class MinifigDecals_Eyebrows(db.Model):
    __tablename__ = 'MinifigDecals_Eyebrows'
    __bind_key__ = 'cdclient'

    ID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    High_path = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    Low_path = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    CharacterCreateValid = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    male = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    female = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class MinifigDecals_Eyes(db.Model):
    __tablename__ = 'MinifigDecals_Eyes'
    __bind_key__ = 'cdclient'

    ID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    High_path = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    Low_path = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    CharacterCreateValid = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    male = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    female = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class MinifigDecals_Legs(db.Model):
    __tablename__ = 'MinifigDecals_Legs'
    __bind_key__ = 'cdclient'

    ID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    High_path = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class MinifigDecals_Mouths(db.Model):
    __tablename__ = 'MinifigDecals_Mouths'
    __bind_key__ = 'cdclient'

    ID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    High_path = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    Low_path = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    CharacterCreateValid = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    male = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    female = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class MinifigDecals_Torsos(db.Model):
    __tablename__ = 'MinifigDecals_Torsos'
    __bind_key__ = 'cdclient'

    ID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    High_path = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    CharacterCreateValid = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    male = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    female = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class MissionEmail(db.Model):
    __tablename__ = 'MissionEmail'
    __bind_key__ = 'cdclient'

    ID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    messageType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    notificationGroup = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    missionID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Missions.id"),
        nullable=False
    )

    mission = db.relationship("Missions")

    attachmentLOT = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=True
    )

    attachment = db.relationship("Objects")

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class MissionNPCComponent(db.Model):
    __tablename__ = 'MissionNPCComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    missionID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Missions.id"),
        nullable=False
    )

    offersMission = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    acceptsMission = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class MissionTasks(db.Model):
    __tablename__ = 'MissionTasks'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    taskType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK ?
    target = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )
    # CSV of ?
    targetGroup = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    targetValue = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    taskParam1 = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    largeTaskIcon = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    IconID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Icons.IconID"),
        nullable=False
    )

    Icon = db.relationship("Icons")

    uid = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    largeTaskIconID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class MissionText(db.Model):
    __tablename__ = 'MissionText'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    story_icon = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    missionIcon = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    offerNPCIcon = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    IconID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Icons.IconID"),
        nullable=False
    )

    Icon = db.relationship("Icons", foreign_keys=[IconID])

    state_1_anim = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    state_2_anim = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    state_3_anim = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    state_4_anim = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    state_3_turnin_anim = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    state_4_turnin_anim = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    onclick_anim = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    CinematicAccepted = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    CinematicAcceptedLeadin = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    CinematicCompleted = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    CinematicCompletedLeadin = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    CinematicRepeatable = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    CinematicRepeatableLeadin = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    CinematicRepeatableCompleted = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    CinematicRepeatableCompletedLeadin = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    AudioEventGUID_Interact = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventGUID_OfferAccept = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventGUID_OfferDeny = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventGUID_Completed = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventGUID_TurnIn = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventGUID_Failed = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventGUID_Progress = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioMusicCue_OfferAccept = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioMusicCue_TurnIn = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    turnInIconID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Icons.IconID"),
        nullable=False
    )

    turnInIcon = db.relationship("Icons", foreign_keys=[turnInIconID])

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK
    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class Missions(db.Model):
    __tablename__ = 'Missions'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    defined_type = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    defined_subtype = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    UISortOrder = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    offer_objectID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    target_objectID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_currency = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    LegoScore = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_reputation = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    isChoiceReward = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    reward_item1 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )

    reward_item1_count = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_item2 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )

    reward_item2_count = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_item3 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )

    reward_item3_count = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_item4 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )

    reward_item4_count = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_emote = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Emotes.id"),
        nullable=False
    )

    reward_emote2 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Emotes.id"),
        nullable=False
    )

    reward_emote3 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Emotes.id"),
        nullable=True
    )

    reward_emote4 = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Emotes.id"),
        nullable=True
    )

    reward_maximagination = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_maxhealth = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_maxinventory = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_maxmodel = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    reward_maxwidget = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    reward_maxwallet = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    repeatable = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    reward_currency_repeatable = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    reward_item1_repeatable = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )

    reward_item1_repeat_count = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_item2_repeatable = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )

    reward_item2_repeat_count = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_item3_repeatable = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )

    reward_item3_repeat_count = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_item4_repeatable = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )

    reward_item4_repeat_count = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    time_limit = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    isMission = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    missionIconID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Icons.IconID"),
        nullable=False
    )

    missionIcon = db.relationship("Icons")

    # pipe SV of missions?
    prereqMissionID = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    inMOTD = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    cooldownTime = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    isRandom = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    randomPool = db.Column(
        sqlite.TEXT(),
        nullable=True
    )
    # FK ?
    UIPrereqID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )

    HUDStates = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reward_bankinventory = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )


class ModelBehavior(db.Model):
    __tablename__ = 'ModelBehavior'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    definitionXMLfilename = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class ModularBuildComponent(db.Model):
    __tablename__ = 'ModularBuildComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    buildType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    xml = db.Column(
        sqlite.VARCHAR(),
        nullable=False
    )

    createdLOT = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )

    createdPhysicsID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    AudioEventGUID_Snap = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    AudioEventGUID_Complete = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventGUID_Present = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class ModuleComponent(db.Model):
    __tablename__ = 'ModuleComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    partCode = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    buildType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    xml = db.Column(
        sqlite.VARCHAR(),
        nullable=False
    )

    primarySoundGUID = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    assembledEffectID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )


class MotionFX(db.Model):
    __tablename__ = 'MotionFX'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    typeID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    slamVelocity = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    addVelocity = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    duration = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    destGroupName = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    startScale = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    endScale = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    velocity = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    distance = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )


class MovementAIComponent(db.Model):
    __tablename__ = 'MovementAIComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    MovementType = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    WanderChance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    WanderDelayMin = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    WanderDelayMax = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    WanderSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    WanderRadius = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    attachedPath = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class MovingPlatforms(db.Model):
    __tablename__ = 'MovingPlatforms'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    platformIsSimpleMover = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    platformMoveX = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    platformMoveY = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    platformMoveZ = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    platformMoveTime = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    platformStartAtEnd = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class NpcIcons(db.Model):
    __tablename__ = 'NpcIcons'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    color = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    offset = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    LOT = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False
    )

    Texture = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    isClickable = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    scale = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    rotateToFace = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    compositeHorizOffset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    compositeVertOffset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    compositeScale = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    compositeConnectionNode = db.Column(
        sqlite.TEXT(),
        nullable=True
    )
    # FK?
    compositeLOTMultiMission = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )
    # FK?
    compositeLOTMultiMissionVentor = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    compositeIconTexture = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class ObjectBehaviorXREF(db.Model):
    __tablename__ = 'ObjectBehaviorXREF'
    __bind_key__ = 'cdclient'

    LOT = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    behaviorID1 = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    behaviorID2 = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    behaviorID3 = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    behaviorID4 = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    behaviorID5 = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    type = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class ObjectBehaviors(db.Model):
    __tablename__ = 'ObjectBehaviors'
    __bind_key__ = 'cdclient'

    BehaviorID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    xmldata = db.Column(
        sqlite.VARCHAR(),
        nullable=False
    )


class ObjectSkills(db.Model):
    __tablename__ = 'ObjectSkills'
    __bind_key__ = 'cdclient'

    objectTemplate = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Objects.id"),
        nullable=False,
        primary_key=True
    )

    skillID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("SkillBehavior.skillID"),
        nullable=False
    )

    castOnType = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    AICombatWeight = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )


class Objects(db.Model):
    __tablename__ = 'Objects'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    name = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    placeable = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    type = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )
    # FK?
    npcTemplateID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    displayName = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    interactionDistance = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    nametag = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    _internalNotes = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK
    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )

    HQ_valid = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class PackageComponent(db.Model):
    __tablename__ = 'PackageComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    LootMatrixIndex = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("LootMatrix.LootMatrixIndex"),
        nullable=False,
        primary_key=True
    )
    # Enum?
    packageType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class PetAbilities(db.Model):
    __tablename__ = 'PetAbilities'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    AbilityName = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    ImaginationCost = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class PetComponent(db.Model):
    __tablename__ = 'PetComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    minTameUpdateTime = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maxTameUpdateTime = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    percentTameChance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    tamability = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    elementType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    walkSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    runSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    sprintSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    idleTimeMin = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    idleTimeMax = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    petForm = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    imaginationDrainRate = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    AudioMetaEventSet = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    # CSV of BuffDefinitions.ID's ?
    buffIDs = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class PetNestComponent(db.Model):
    __tablename__ = 'PetNestComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    ElementalType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class PhysicsComponent(db.Model):
    __tablename__ = 'PhysicsComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    static = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    physics_asset = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    jump = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    doublejump = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    speed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    rotSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    playerHeight = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    playerRadius = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    pcShapeType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    collisionGroup = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    airSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    boundaryAsset = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    jumpAirSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    friction = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    gravityVolumeAsset = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class PlayerFlags(db.Model):
    __tablename__ = 'PlayerFlags'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    SessionOnly = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    OnlySetByServer = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    SessionZoneOnly = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class PlayerStatistics(db.Model):
    __tablename__ = 'PlayerStatistics'
    __bind_key__ = 'cdclient'

    statID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    sortOrder = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class PossessableComponent(db.Model):
    __tablename__ = 'PossessableComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK
    controlSchemeID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK???
    minifigAttachPoint = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    minifigAttachAnimation = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    minifigDetachAnimation = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    mountAttachAnimation = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    mountDetachAnimation = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    attachOffsetFwd = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    attachOffsetRight = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    possessionType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    wantBillboard = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    billboardOffsetUp = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    depossessOnHit = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    hitStunTime = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    skillSet = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )


class Preconditions(db.Model):
    __tablename__ = 'Preconditions'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    type = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )
    # CSV of LOTS
    targetLOT = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    targetGroup = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    targetCount = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    IconID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Icons.IconID"),
        nullable=False
    )

    Icon = db.relationship("Icons")

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    validContexts = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK
    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class PropertyEntranceComponent(db.Model):
    __tablename__ = 'PropertyEntranceComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK Zone Table
    mapID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    propertyName = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    isOnProperty = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    groupType = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class PropertyTemplate(db.Model):
    __tablename__ = 'PropertyTemplate'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # ???
    mapID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK ZoneTable
    vendorMapID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    spawnName = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    type = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    sizecode = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    minimumPrice = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    rentDuration = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    path = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    cloneLimit = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    durationType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    achievementRequired = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    zoneX = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    zoneY = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    zoneZ = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maxBuildHeight = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    reputationPerMinute = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK
    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class ProximityMonitorComponent(db.Model):
    __tablename__ = 'ProximityMonitorComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # CSV of Prox Types
    Proximities = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    LoadOnClient = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    LoadOnServer = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class ProximityTypes(db.Model):
    __tablename__ = 'ProximityTypes'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    Name = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    Radius = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    CollisionGroup = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    PassiveChecks = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    IconID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Icons.IconID"),
        nullable=False
    )

    Icon = db.relationship("Icons")

    LoadOnClient = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    LoadOnServer = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class RacingModuleComponent(db.Model):
    __tablename__ = 'RacingModuleComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    topSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    acceleration = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    handling = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    stability = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    imagination = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )


class RailActivatorComponent(db.Model):
    __tablename__ = 'RailActivatorComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK ?
    startAnim = db.Column(
        sqlite.TEXT(),
        nullable=False
    )
    # FK ?
    loopAnim = db.Column(
        sqlite.TEXT(),
        nullable=True
    )
    # FK ?
    stopAnim = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    startSound = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    loopSound = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    stopSound = db.Column(
        sqlite.TEXT(),
        nullable=True
    )
    # FK
    effectIDs = db.Column(
        sqlite.TEXT(),
        nullable=True
    )
    # FK
    preconditions = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    playerCollision = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    cameraLocked = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )
    # FK?
    StartEffectID = db.Column(
        sqlite.TEXT(),
        nullable=True
    )
    # FK?
    StopEffectID = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    DamageImmune = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    NoAggro = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    ShowNameBillboard = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class RarityTable(db.Model):
    __tablename__ = 'RarityTable'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    randmax = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    rarity = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK
    RarityTableIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class RarityTableIndex(db.Model):
    __tablename__ = 'RarityTableIndex'
    __bind_key__ = 'cdclient'

    RarityTableIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )


class RebuildComponent(db.Model):
    __tablename__ = 'RebuildComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    reset_time = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    complete_time = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    take_imagination = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    interruptible = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    self_activator = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )
    # CSV OF LOTS
    custom_modules = db.Column(
        sqlite.TEXT(),
        nullable=True
    )
    # FK
    activityID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    post_imagination_cost = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    time_before_smash = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )


class RebuildSections(db.Model):
    __tablename__ = 'RebuildSections'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK rebuild component
    rebuildID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # LOT
    objectID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    offset_x = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    offset_y = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    offset_z = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fall_angle_x = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    fall_angle_y = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    fall_angle_z = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    fall_height = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    requires_list = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    size = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    bPlaced = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class Release_Version(db.Model):
    __tablename__ = 'Release_Version'
    __bind_key__ = 'cdclient'

    ReleaseVersion = db.Column(
        sqlite.TEXT(),
        nullable=False,
        primary_key=True
    )

    ReleaseDate = db.Column(
        sqlite.TIMESTAMP(),
        nullable=False
    )


class RenderComponent(db.Model):
    __tablename__ = 'RenderComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    render_asset = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    icon_asset = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    IconID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Icons.IconID"),
        nullable=False
    )

    Icon = db.relationship("Icons")
    # FK mapshaders
    shader_id = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    effect1 = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    effect2 = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    effect3 = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    effect4 = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    effect5 = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    effect6 = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    animationGroupIDs = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    fade = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    usedropshadow = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    preloadAnimations = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    fadeInTime = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    maxShadowDistance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    ignoreCameraCollision = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )
    # FK ?
    renderComponentLOD1 = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )
    # FK?
    renderComponentLOD2 = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    gradualSnap = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    animationFlag = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    AudioMetaEventSet = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    billboardHeight = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    chatBubbleOffset = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    staticBillboard = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    LXFMLFolder = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    attachIndicatorsToNode = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class RenderComponentFlash(db.Model):
    __tablename__ = 'RenderComponentFlash'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    interactive = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    animated = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    nodeName = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    flashPath = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    elementName = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    _uid = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )


class RenderComponentWrapper(db.Model):
    __tablename__ = 'RenderComponentWrapper'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    defaultWrapperAsset = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class RenderIconAssets(db.Model):
    __tablename__ = 'RenderIconAssets'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    icon_asset = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    blank_column = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class ReputationRewards(db.Model):
    __tablename__ = 'ReputationRewards'
    __bind_key__ = 'cdclient'

    repLevel = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    sublevel = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    reputation = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )


class RewardCodes(db.Model):
    __tablename__ = 'RewardCodes'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # unique?
    code = db.Column(
        sqlite.TEXT(),
        nullable=False,
    )
    # LOT
    attachmentLOT = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK
    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class Rewards(db.Model):
    __tablename__ = 'Rewards'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    LevelID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    MissionID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    RewardType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # generic relationship
    value = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    count = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )


class RocketLaunchpadControlComponent(db.Model):
    __tablename__ = 'RocketLaunchpadControlComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK Zone Table
    targetZone = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK?
    defaultZoneID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    targetScene = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    gmLevel = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    playerAnimation = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    rocketAnimation = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    launchMusic = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    useLaunchPrecondition = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    useAltLandingPrecondition = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )
    # FK
    launchPrecondition = db.Column(
        sqlite.TEXT(),
        nullable=True
    )
    # FK
    altLandingPrecondition = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    altLandingSpawnPointName = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class SceneTable(db.Model):
    __tablename__ = 'SceneTable'
    __bind_key__ = 'cdclient'

    sceneID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    sceneName = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class ScriptComponent(db.Model):
    __tablename__ = 'ScriptComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    script_name = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    client_script_name = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class SkillBehavior(db.Model):
    __tablename__ = 'SkillBehavior'
    __bind_key__ = 'cdclient'

    skillID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK
    behaviorID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    imaginationcost = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    cooldowngroup = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    cooldown = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    inNpcEditor = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    skillIcon = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )
    # CSV of skills?
    oomSkillID = db.Column(
        sqlite.TEXT(),
        nullable=True
    )
    # FK
    oomBehaviorEffectID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    castTypeDesc = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    imBonusUI = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    lifeBonusUI = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    armorBonusUI = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    damageUI = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    hideIcon = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )
    # FK
    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )

    cancelType = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )


class SmashableChain(db.Model):
    __tablename__ = 'SmashableChain'
    __bind_key__ = 'cdclient'

    # FK
    chainIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    chainLevel = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    lootMatrixID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK
    rarityTableIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK
    currencyIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    currencyLevel = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    smashCount = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    timeLimit = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    chainStepID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class SmashableChainIndex(db.Model):
    __tablename__ = 'SmashableChainIndex'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    targetGroup = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    continuous = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class SmashableComponent(db.Model):
    __tablename__ = 'SmashableComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK
    LootMatrixIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class SmashableElements(db.Model):
    __tablename__ = 'SmashableElements'
    __bind_key__ = 'cdclient'

    # FK? to brick table or objects?
    elementID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    dropWeight = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class SpeedchatMenu(db.Model):
    __tablename__ = 'SpeedchatMenu'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK to this table
    parentId = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )
    # FK to Emotes
    emoteId = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    imageName = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK
    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class SubscriptionPricing(db.Model):
    __tablename__ = 'SubscriptionPricing'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    countryCode = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    monthlyFeeGold = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    monthlyFeeSilver = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    monthlyFeeBronze = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    monetarySymbol = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    symbolIsAppended = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class SurfaceType(db.Model):
    __tablename__ = 'SurfaceType'
    __bind_key__ = 'cdclient'

    SurfaceType = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    FootstepNDAudioMetaEventSetName = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class TamingBuildPuzzles(db.Model):
    __tablename__ = 'TamingBuildPuzzles'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # LOT
    PuzzleModelLot = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    NPCLot = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    ValidPiecesLXF = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    InvalidPiecesLXF = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    Difficulty = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    Timelimit = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    NumValidPieces = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    TotalNumPieces = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    ModelName = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    FullModelLXF = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    Duration = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    imagCostPerBuild = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class TextDescription(db.Model):
    __tablename__ = 'TextDescription'
    __bind_key__ = 'cdclient'

    TextID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    TestDescription = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class TextLanguage(db.Model):
    __tablename__ = 'TextLanguage'
    __bind_key__ = 'cdclient'

    TextID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    LanguageID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    Text = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class TrailEffects(db.Model):
    __tablename__ = 'TrailEffects'
    __bind_key__ = 'cdclient'

    trailID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    textureName = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    blendmode = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    cardlifetime = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    colorlifetime = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    minTailFade = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    tailFade = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    max_particles = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    birthDelay = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    deathDelay = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    bone1 = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    bone2 = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    texLength = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    texWidth = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    startColorR = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    startColorG = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    startColorB = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    startColorA = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    middleColorR = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    middleColorG = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    middleColorB = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    middleColorA = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    endColorR = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    endColorG = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    endColorB = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    endColorA = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )


class UGBehaviorSounds(db.Model):
    __tablename__ = 'UGBehaviorSounds'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    guid = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK
    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )


class VehiclePhysics(db.Model):
    __tablename__ = 'VehiclePhysics'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    hkxFilename = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    fGravityScale = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fMass = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fChassisFriction = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fMaxSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fEngineTorque = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fBrakeFrontTorque = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fBrakeRearTorque = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fBrakeMinInputToBlock = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fBrakeMinTimeToBlock = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fSteeringMaxAngle = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fSteeringSpeedLimitForMaxAngle = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fSteeringMinAngle = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fFwdBias = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fFrontTireFriction = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fRearTireFriction = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fFrontTireFrictionSlide = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fRearTireFrictionSlide = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fFrontTireSlipAngle = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fRearTireSlipAngle = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fWheelWidth = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fWheelRadius = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fWheelMass = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fReorientPitchStrength = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fReorientRollStrength = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fSuspensionLength = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fSuspensionStrength = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fSuspensionDampingCompression = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fSuspensionDampingRelaxation = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    iChassisCollisionGroup = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    fNormalSpinDamping = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fCollisionSpinDamping = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fCollisionThreshold = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fTorqueRollFactor = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fTorquePitchFactor = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fTorqueYawFactor = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInertiaRoll = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInertiaPitch = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInertiaYaw = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fExtraTorqueFactor = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fCenterOfMassFwd = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fCenterOfMassUp = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fCenterOfMassRight = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fWheelHardpointFrontFwd = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fWheelHardpointFrontUp = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fWheelHardpointFrontRight = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fWheelHardpointRearFwd = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fWheelHardpointRearUp = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fWheelHardpointRearRight = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInputTurnSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInputDeadTurnBackSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInputAccelSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInputDeadAccelDownSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInputDecelSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInputDeadDecelDownSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInputSlopeChangePointX = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInputInitialSlope = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fInputDeadZone = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fAeroAirDensity = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fAeroFrontalArea = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fAeroDragCoefficient = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fAeroLiftCoefficient = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fAeroExtraGravity = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fBoostTopSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fBoostCostPerSecond = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fBoostAccelerateChange = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fBoostDampingChange = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fPowerslideNeutralAngle = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fPowerslideTorqueStrength = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    iPowerslideNumTorqueApplications = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    fImaginationTankSize = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fSkillCost = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fWreckSpeedBase = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    fWreckSpeedPercent = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    fWreckMinAngle = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    AudioEventEngine = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventSkid = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventLightHit = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioSpeedThresholdLightHit = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    AudioTimeoutLightHit = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    AudioEventHeavyHit = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioSpeedThresholdHeavyHit = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    AudioTimeoutHeavyHit = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    AudioEventStart = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadConcrete = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadSand = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadWood = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadDirt = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadPlastic = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadGrass = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadGravel = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadMud = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadWater = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadSnow = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadIce = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadMetal = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventTreadLeaves = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioEventLightLand = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioAirtimeForLightLand = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    AudioEventHeavyLand = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    AudioAirtimeForHeavyLand = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    bWheelsVisible = db.Column(
        sqlite.BOOLEAN(),
        nullable=True
    )


class VehicleStatMap(db.Model):
    __tablename__ = 'VehicleStatMap'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    ModuleStat = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    HavokStat = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    HavokChangePerModuleStat = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )


class VendorComponent(db.Model):
    __tablename__ = 'VendorComponent'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    buyScalar = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    sellScalar = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    refreshTimeSeconds = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )
    # FK
    LootMatrixIndex = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class WhatsCoolItemSpotlight(db.Model):
    __tablename__ = 'WhatsCoolItemSpotlight'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK
    itemID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )
    # FK
    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class WhatsCoolNewsAndTips(db.Model):
    __tablename__ = 'WhatsCoolNewsAndTips'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    IconID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Icons.IconID"),
        nullable=False
    )

    Icon = db.relationship("Icons")

    type = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )
    # FK
    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class WorldConfig(db.Model):
    __tablename__ = 'WorldConfig'
    __bind_key__ = 'cdclient'

    WorldConfigID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    pegravityvalue = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    pebroadphaseworldsize = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    pegameobjscalefactor = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_rotation_speed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_walk_forward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_walk_backward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_walk_strafe_speed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_walk_strafe_forward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_walk_strafe_backward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_run_backward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_run_strafe_speed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_run_strafe_forward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_run_strafe_backward_speed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    global_cooldown = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    characterGroundedTime = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    characterGroundedSpeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    globalImmunityTime = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_max_slope = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    defaultrespawntime = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    mission_tooltip_timeout = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    vendor_buy_multiplier = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    pet_follow_radius = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    character_eye_height = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    flight_vertical_velocity = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    flight_airspeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    flight_fuel_ratio = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    flight_max_airspeed = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    fReputationPerVote = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    nPropertyCloneLimit = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    defaultHomespaceTemplate = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    coins_lost_on_death_percent = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    coins_lost_on_death_min = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    coins_lost_on_death_max = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    character_votes_per_day = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    property_moderation_request_approval_cost = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    property_moderation_request_review_cost = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    propertyModRequestsAllowedSpike = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    propertyModRequestsAllowedInterval = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    propertyModRequestsAllowedTotal = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    propertyModRequestsSpikeDuration = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    propertyModRequestsIntervalDuration = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    modelModerateOnCreate = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    defaultPropertyMaxHeight = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    reputationPerVoteCast = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    reputationPerVoteReceived = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    showcaseTopModelConsiderationBattles = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    reputationPerBattlePromotion = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    coins_lost_on_death_min_timeout = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    coins_lost_on_death_max_timeout = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    mail_base_fee = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    mail_percent_attachment_fee = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    propertyReputationDelay = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    LevelCap = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK?
    LevelUpBehaviorEffect = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    CharacterVersion = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    LevelCapCurrencyConversion = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class ZoneLoadingTips(db.Model):
    __tablename__ = 'ZoneLoadingTips'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK
    zoneid = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    imagelocation = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )
    # FK
    gate_version = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    weight = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )
    # FK?
    targetVersion = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class ZoneSummary(db.Model):
    __tablename__ = 'ZoneSummary'
    __bind_key__ = 'cdclient'

    zoneID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    type = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    value = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )
    # Ignoring, composite key makes more sense
    _uniqueID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class ZoneTable(db.Model):
    __tablename__ = 'ZoneTable'
    __bind_key__ = 'cdclient'

    zoneID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    zoneName = db.Column(
        sqlite.TEXT(),
        nullable=False
    )
    # FK
    scriptID = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    ghostdistance_min = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    ghostdistance = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )

    population_soft_cap = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    population_hard_cap = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    DisplayDescription = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    mapFolder = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    smashableMinDistance = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    smashableMaxDistance = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    mixerProgram = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    clientPhysicsFramerate = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    serverPhysicsFramerate = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    zoneControlTemplate = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    widthInChunks = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    heightInChunks = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )

    petsAllowed = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    localize = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    fZoneWeight = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    thumbnail = db.Column(
        sqlite.TEXT(),
        nullable=True
    )

    PlayerLoseCoinsOnDeath = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    disableSaveLoc = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )

    teamRadius = db.Column(
        sqlite.FLOAT(),
        nullable=True
    )

    gate_version = db.Column(
        sqlite.TEXT(),
        db.ForeignKey("FeatureGating.featureName"),
        nullable=True
    )

    mountsAllowed = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class brickAttributes(db.Model):
    __tablename__ = 'brickAttributes'
    __bind_key__ = 'cdclient'

    ID = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    icon_asset = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    display_order = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    locStatus = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class dtproperties(db.Model):
    __tablename__ = 'dtproperties'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )
    # FK
    objectid = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    property_colume = db.Column(
        'property',
        sqlite.TEXT(),
        nullable=False
    )

    value = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    uvalue = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    lvalue = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    version = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class mapAnimationPriorities(db.Model):
    __tablename__ = 'mapAnimationPriorities'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    name = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    priority = db.Column(
        sqlite.FLOAT(),
        nullable=False
    )


class mapAssetType(db.Model):
    __tablename__ = 'mapAssetType'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    label = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    pathdir = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    typelabel = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class mapIcon(db.Model):
    __tablename__ = 'mapIcon'
    __bind_key__ = 'cdclient'

    LOT = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    IconID = db.Column(
        sqlite.INTEGER(),
        db.ForeignKey("Icons.IconID"),
        nullable=False,
        primary_key=True
    )

    Icon = db.relationship("Icons")

    iconState = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class mapItemTypes(db.Model):
    __tablename__ = 'mapItemTypes'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    equipLocation = db.Column(
        sqlite.TEXT(),
        nullable=True
    )


class mapRenderEffects(db.Model):
    __tablename__ = 'mapRenderEffects'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    gameID = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=False
    )


class mapShaders(db.Model):
    __tablename__ = 'mapShaders'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    label = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    gameValue = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )

    priority = db.Column(
        sqlite.INTEGER(),
        nullable=True
    )


class mapTextureResource(db.Model):
    __tablename__ = 'mapTextureResource'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    texturepath = db.Column(
        sqlite.TEXT(),
        nullable=False
    )
    # FK shaders?
    SurfaceType = db.Column(
        sqlite.INTEGER(),
        nullable=False
    )


class map_BlueprintCategory(db.Model):
    __tablename__ = 'map_BlueprintCategory'
    __bind_key__ = 'cdclient'

    id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    description = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    enabled = db.Column(
        sqlite.BOOLEAN(),
        nullable=False
    )


class sysdiagrams(db.Model):
    __tablename__ = 'sysdiagrams'
    __bind_key__ = 'cdclient'

    name = db.Column(
        sqlite.TEXT(),
        nullable=False
    )

    principal_id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    diagram_id = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    version = db.Column(
        sqlite.INTEGER(),
        nullable=False,
        primary_key=True
    )

    definition = db.Column(
        sqlite.TEXT(),
        nullable=False
    )
