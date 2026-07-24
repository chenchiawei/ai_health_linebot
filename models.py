from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    """使用者個人檔案表"""
    __tablename__ = "users"

    line_user_id = Column(String(100), primary_key=True, index=True)
    name = Column(String(50), nullable=True)
    gender = Column(String(10), default="male")  # male / female
    age = Column(Integer, default=25)
    height = Column(Float, default=170.0)       # cm
    weight = Column(Float, default=70.0)        # kg
    body_fat = Column(Float, nullable=True)     # %
    activity_level = Column(Float, default=1.375) # 1.2(久坐), 1.375(輕度), 1.55(中度), 1.725(重度)
    goal = Column(String(20), default="cut")    # cut (減脂) / maintain (維持) / bulk (增肌)
    
    # AI 動態計算之熱量與三大營養素目標
    bmr = Column(Float, default=1600.0)
    tdee = Column(Float, default=2200.0)
    target_calories = Column(Float, default=1700.0)
    target_protein = Column(Float, default=140.0)  # 克
    target_carbs = Column(Float, default=170.0)    # 克
    target_fat = Column(Float, default=50.0)       # 克
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    health_logs = relationship("HealthLog", back_populates="user", cascade="all, delete-orphan")
    meal_logs = relationship("MealLog", back_populates="user", cascade="all, delete-orphan")

class HealthLog(Base):
    """體重與體脂歷史紀錄表"""
    __tablename__ = "health_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_user_id = Column(String(100), ForeignKey("users.line_user_id"), nullable=False)
    weight = Column(Float, nullable=False)
    body_fat = Column(Float, nullable=True)
    notes = Column(String(255), nullable=True)
    logged_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="health_logs")

class MealLog(Base):
    """飲食打卡與熱量紀錄表"""
    __tablename__ = "meal_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    line_user_id = Column(String(100), ForeignKey("users.line_user_id"), nullable=False)
    meal_type = Column(String(20), default="meal") # breakfast / lunch / dinner / snack
    meal_name = Column(String(100), nullable=False)
    calories = Column(Float, default=0.0)
    protein = Column(Float, default=0.0)
    carbs = Column(Float, default=0.0)
    fat = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    logged_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="meal_logs")
