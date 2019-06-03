from app import app
from flask import Flask, render_template, redirect, url_for, request, make_response


if __name__ == "__main__":
    app.run(debug=True)