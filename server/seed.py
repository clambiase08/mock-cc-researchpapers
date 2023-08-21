#!/usr/bin/env python3
from random import choice as rc
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from models import db, Research, Author, ResearchAuthor

with app.app_context():
    # This will delete any existing rows
    # so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    Research.query.delete()
    Author.query.delete()
    ResearchAuthor.query.delete()

    print("Creating Research...")
    r1 = Research(topic="AI In Day To Day Life", year=1994, page_count=10)
    r2 = Research(topic="Robotics, A Case Study", year=2010, page_count=100)
    r3 = Research(topic="Methods of Training Data", year=2020, page_count=1000)
    research_papers = [r1, r2, r3]
    db.session.add_all(research_papers)
    db.session.commit()
    print("Creating Author...")

    a1 = Author(name="Billy", field_of_study="AI")
    a2 = Author(name="Ted", field_of_study="Robotics")
    a3 = Author(name="Bob", field_of_study="Cybersecurity")
    authors = [a1, a2, a3]
    db.session.add_all(authors)
    db.session.commit()
    print("Creating ResearchAuthors...")

    ra1 = ResearchAuthor(author_id=a1.id, research_id=r1.id)
    ra2 = ResearchAuthor(author_id=a2.id, research_id=r2.id)
    ra3 = ResearchAuthor(author_id=a3.id, research_id=r3.id)
    ra4 = ResearchAuthor(author_id=a1.id, research_id=r3.id)
    researchAuthor = [ra1, ra2, ra3, ra4]

    db.session.add_all(researchAuthor)
    db.session.commit()

    print("Seeding done!")
