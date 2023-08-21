from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata, engine_options={"echo": True})


class TimestampMixin:
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


class Research(db.Model, SerializerMixin, TimestampMixin):
    __tablename__ = "research"
    serialize_rules = (
        "-researchauthors.research",
        "-researchauthors.author",
        "-created_at",
        "-updated_at",
    )

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    year = db.Column(db.Integer, nullable=False)
    page_count = db.Column(db.Integer)

    researchauthors = db.relationship(
        "ResearchAuthor", back_populates="research", cascade="delete"
    )
    authors = association_proxy("researchauthors", "author")

    @validates("year")
    def validate_year(self, key, year):
        if not len(str(year)) == 4 or not isinstance(year, int):
            raise ValueError("Year must be a 4 digit integer")
        return year


class ResearchAuthor(db.Model, SerializerMixin, TimestampMixin):
    __tablename__ = "researchauthors"
    serialize_rules = (
        "-author.researchauthors",
        "-research.researchauthors",
        "-created_at",
        "-updated_at",
    )

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    research_id = db.Column(db.Integer, db.ForeignKey("research.id"))

    research = db.relationship("Research", back_populates="researchauthors")
    author = db.relationship("Author", back_populates="researchauthors")


class Author(db.Model, SerializerMixin, TimestampMixin):
    __tablename__ = "authors"
    serialize_rules = (
        "-researchauthors.research",
        "-researchauthors.author",
        "-created_at",
        "-updated_at",
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    researchauthors = db.relationship(
        "ResearchAuthor", back_populates="author", cascade="delete"
    )
    researches = association_proxy("researchauthors", "research")

    @validates("field_of_study")
    def validate_field(self, key, field):
        study = ["AI", "Robotics", "Machine Learning", "Vision", "Cybersecurity"]
        if field not in study:
            raise ValueError("Invalid field")
        return field
