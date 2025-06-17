# from pydantic_settings import BaseSettings
# from functools import lru_cache

# class Settings(BaseSettings):
#     OPENAI_API_KEY: str
#     DATABASE_URL: str = "sqlite:///./complaints.db"
    
#     class Config:
#         env_file = ".env"

# @lru_cache()
# def get_settings():
#     return Settings()





# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     openai_api_key: str
#     database_url: str = "sqlite:///./complaints.db"
    
#     class Config:
#         env_file = ".env"

# settings = Settings()
######################### open ai 











from pydantic import BaseSettings

class Settings(BaseSettings):
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model: str = "ggml-gpt4all-j-v1.3-groovy.bin"
    database_url: str = "sqlite:///./complaints.db"
    
    class Config:
        env_file = ".env"

settings = Settings()