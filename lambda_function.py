import json
import pynamodb
from pynamodb.models import Model
from pynamodb.attributes import NumberAttribute, UnicodeAttribute, BooleanAttribute

HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404


class Book(Model):
    class Meta:
        table_name = "books"
        region = "eu-central-1"

    id = NumberAttribute(hash_key=True)
    title = UnicodeAttribute()
    author = UnicodeAttribute()
    is_read = BooleanAttribute()


def lambda_handler(event: dict, context):
    # Retrieve initial data
    http_method = event.get("http_method")
    body = event.get("body")
    # Execute the provided method
    if http_method == "GET":
        return method_get(body)
    elif http_method == "LIST":
        return method_list()
    elif http_method == "POST":
        return method_post(body)
    elif http_method == "PUT":
        return method_put(body)
    elif http_method == "PATCH":
        return method_patch(body)
    elif http_method == "DELETE":
        return method_delete(body)
    else:
        return {
            "statusCode": HTTP_404_NOT_FOUND,
            "body": json.dumps({"error": "Invalid HTTP method."})
        }


def method_get(body: dict):
    book = Book.get(body["id"])
    book_data = {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "is_read": book.is_read
    }
    return {
        "statusCode": HTTP_200_OK,
        "body": json.dumps(book_data)
    }


def method_list():
    books = Book.scan()
    books_data: list = []
    for book in books:
        book_data = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "is_read": book.is_read
        }
        books_data.append(book_data)
    return {
        "statusCode": HTTP_200_OK,
        "body": json.dumps(books_data)
    }


def method_post(body: dict):
    book = Book(id=body["id"], title=body["title"], author=body["author"], is_read=body.get("is_read", False))
    book.save()
    return {
        "statusCode": HTTP_201_CREATED,
        "body": "Book added."
    }


def method_put(body: dict):
    book = Book(id=body["id"], title=body["title"], author=body["author"], is_read=body.get("is_read", False))
    book.save()
    return {
        "statusCode": HTTP_200_OK,
        "body": "Book updated."
    }


def method_patch(body: dict):
    book = Book.get(body["id"])
    body.pop("id")
    for attribute, value in body.items():
        setattr(book, attribute, value)
    book.save()
    return {
        "statusCode": HTTP_200_OK,
        "body": "Book updated."
    }


def method_delete(body: dict):
    book = Book.get(body["id"])
    book.delete()
    return {
        "statusCode": HTTP_204_NO_CONTENT,
        "body": {}
    }
