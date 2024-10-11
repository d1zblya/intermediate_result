from __main__ import app
from flask import render_template
import aiohttp


@app.route("/products")
async def products_page():
    session = aiohttp.ClientSession()
    products = await session.get(f'http://127.0.0.1:5000/api/page/product')
    products = await products.json()
    products = products['products']
    
    return render_template(
        "products.html",
        items=products,
    )
