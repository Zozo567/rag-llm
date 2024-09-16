from enum import Enum


class Stages(Enum):
    LOCAL = 'local'
    PRODUCTION = 'production'
    STAGING = 'staging'
    DEVELOPMENT = 'development'
