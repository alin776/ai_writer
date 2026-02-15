from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class WorkStatus(str, enum.Enum):
    """作品状态"""
    DRAFT = "draft"  # 草稿
    WRITING = "writing"  # 连载中
    COMPLETED = "completed"  # 已完结
    ABANDONED = "abandoned"  # 已弃坑


class WorkGenre(str, enum.Enum):
    """作品类型"""
    FANTASY = "fantasy"  # 玄幻
    URBAN = "urban"  # 都市
    ROMANCE = "romance"  # 言情
    SCIFI = "scifi"  # 科幻
    WUXIA = "wuxia"  # 武侠
    GAME = "game"  # 游戏
    HISTORY = "history"  # 历史
    MILITARY = "military"  # 军事
    SUSPENSE = "suspense"  # 悬疑
    WESTERN_FANTASY = "western_fantasy"  # 西幻
    APOCALYPSE = "apocalypse"  # 末世
    OTHER = "other"  # 其他


class Work(Base):
    """作品模型"""
    
    __tablename__ = "works"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # 基本信息
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    cover_image = Column(String(500), nullable=True)
    
    # 分类和状态
    genre = Column(Enum(WorkGenre), nullable=False, default=WorkGenre.OTHER)
    status = Column(Enum(WorkStatus), nullable=False, default=WorkStatus.DRAFT)
    is_published = Column(Boolean, default=False, nullable=False, comment="是否发布到小说广场")
    is_featured = Column(Boolean, default=False, nullable=False, index=True, comment="是否为推荐作品(最多5本)")

    # 统计信息
    total_words = Column(Integer, default=0, nullable=False)
    total_chapters = Column(Integer, default=0, nullable=False)
    view_count = Column(Integer, default=0, nullable=False)
    favorite_count = Column(Integer, default=0, nullable=False, comment="收藏数")
    worldview_version = Column(Integer, default=1, nullable=False, comment="世界观版本号")
    
    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关联关系
    author = relationship("User", back_populates="works")
    chapters = relationship("Chapter", back_populates="work", cascade="all, delete-orphan", order_by="Chapter.order")
    characters = relationship("Character", back_populates="work", cascade="all, delete-orphan")
    locations = relationship("Location", back_populates="work", cascade="all, delete-orphan")
    settings = relationship("Setting", back_populates="work", cascade="all, delete-orphan")
    guidelines = relationship("WorkGuidelines", back_populates="work", cascade="all, delete-orphan", uselist=False)
    ai_guidelines = relationship("AIGuidelines", back_populates="work", cascade="all, delete-orphan", uselist=False)
    novel_analysis = relationship("NovelAnalysis", back_populates="work", cascade="all, delete-orphan", uselist=False)
    analysis_vectors = relationship("NovelAnalysisVector", back_populates="work", cascade="all, delete-orphan")
    knowledge_items = relationship("KnowledgeItem", back_populates="work", cascade="all, delete-orphan")
    bookshelf_items = relationship("Bookshelf", back_populates="work", cascade="all, delete-orphan", passive_deletes=True)
    entity_relationships = relationship("EntityRelationship", back_populates="work", cascade="all, delete-orphan")
    work_ratings = relationship("WorkRating", back_populates="work", cascade="all, delete-orphan")
    channel = relationship("Channel", back_populates="work", cascade="all, delete-orphan", uselist=False)
    comments = relationship("Comment", back_populates="work", cascade="all, delete-orphan")
    glossary_terms = relationship("GlossaryTerm", back_populates="work", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Work {self.title}>"
