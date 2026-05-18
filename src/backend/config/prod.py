from .base import BaseAppConfig,ProductionVariable 

class ProdConfig(BaseAppConfig):
    D_EXEC : bool = True
    DEBUG  : bool = False
    PRODUCTION_VARIABLE : ProductionVariable = ProductionVariable.PRODUCTION # Immediate switch between consequtive production and development

