from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'hehehe'
with open('saleapp/db/products.json') as f:
    data = json.load(f)

