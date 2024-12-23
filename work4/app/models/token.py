from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    refresh_token: str

class TokenData(BaseModel):
    # 这个模型用于从JWT令牌载荷中提取数据
    email: str = None

class TokenRefresh(BaseModel):
    # 这个模型用于刷新令牌请求
    refresh_token: str = None

class VerifyToken(BaseModel):
    # 这个模型用于验证令牌请求
    token: str = None