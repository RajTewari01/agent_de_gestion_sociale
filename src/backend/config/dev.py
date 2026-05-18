from .base import BaseAppConfig,ProductionVariable 

class DevConfig(BaseAppConfig):
    D_EXEC : bool = False
    DEBUG  : bool = True
    PRODUCTION_VARIABLE : ProductionVariable = ProductionVariable.DEVELOPMENT # Immediate switch between consequtive production and development

