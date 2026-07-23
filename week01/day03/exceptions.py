class AppError(Exception):
    """项目所有自定义异常的父类。"""


class ConfigError(AppError):
    """配置相关异常的父类。"""


class ConfigFileNotFoundError(ConfigError):
    """配置文件不存在。"""


class ConfigFormatError(ConfigError):
    """配置文件格式错误。"""

class RetryableError(AppError):
    """允许重试的临时性异常。"""


class TemporaryNetworkError(RetryableError):
    """临时网络异常。"""


class RetryExhaustedError(AppError):
    """达到最大重试次数后仍然失败。"""

class NonRetryableError(AppError):
    """不可通过重试恢复的异常。"""


class AuthenticationError(NonRetryableError):
    """认证信息错误。"""


class QuotaExceededError(NonRetryableError):
    """账户额度不足。"""
    
class ModelRequestError(NonRetryableError):
    """模型请求参数等不可重试错误。"""