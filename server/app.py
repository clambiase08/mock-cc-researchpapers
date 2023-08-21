#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource, abort

from models import db, Research, Author, ResearchAuthor

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class ResearchResource(Resource):
    def get(self):
        research = [
            r.to_dict(rules=("-researchauthors",)) for r in Research.query.all()
        ]
        return make_response(research, 200)


api.add_resource(ResearchResource, "/research")


class ResearchById(Resource):
    def get(self, id):
        research = Research.query.get_or_404(
            id, description="Research paper not found"
        ).to_dict(
            rules=(
                "-researchauthors",
                "authors",  # this makes sure the authors is included
                "-authors.researchauthors",  # this makes sure the research authors is not included on the authors we added back
            )
        )
        return make_response(research, 200)

    def delete(self, id):
        research = Research.query.get_or_404(id, description="Research paper not found")
        db.session.delete(research)
        db.session.commit()
        return make_response("", 204)


api.add_resource(ResearchById, "/research/<int:id>")


class Authors(Resource):
    def get(self):
        authors = [a.to_dict(rules=("-researchauthors",)) for a in Author.query.all()]
        return make_response(authors, 200)


api.add_resource(Authors, "/authors")


class ResearchAuthors(Resource):
    def post(self):
        data = request.get_json()
        try:
            new_researchauthors = ResearchAuthor(**data)
        except Exception as e:
            abort(422, errors=["validation errors"])
        db.session.add(new_researchauthors)
        db.session.commit()
        return make_response(
            new_researchauthors.author.to_dict(rules=("-researchauthors",)),
            201,
        )


api.add_resource(ResearchAuthors, "/research_author")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
