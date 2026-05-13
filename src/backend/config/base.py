from enum import Enum
import pydantic as pdt #type: ignore

class ProductionVariable(str,Enum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"

class BaseAppConfig(pdt.BaseModel,strict=True):
    D_EXEC : bool # Deffered Execution : If True, the application will not start immediately, but will wait for a start command.
    DEBUG  : bool # Debug mode: If True, enables debugging features and error reporting.
    PRODUCTION_VARIABLE : ProductionVariable # Immediate switch between consequtive production and development

    