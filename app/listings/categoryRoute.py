from flask_jwt_extended import jwt_required
from flask import jsonify, request
from app.listings import category_bp
from app.models.categoryModel import Category
from app.utils.generators import admin_required
from app.models.productModel import Product


# get products by category
@category_bp.get("/<string:category_id>/products")
def get_products_by_category(category_id):
    products = Product.query.filter_by(category_id=category_id).all()

    products_data = list()

    for product in products:
        product_data = {
            'id': product.product_id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'category_id': product.category_id
        }
        products_data.append(product_data)
    
    return jsonify({
        "message": "Category Products fetched successfully",
        "results": products_data
    }), 201

#Route to retrieve a paginated list of products based on a specific category
@category_bp.get("/<string:category_id>/paginated-products")
def get_paginated_products_by_cateory(category_id):
    #pagination parameters
    page = request.args.get("page", 1, type=int)
    per_page =  request.args.get("per_page", 10, type=int)

    #Query category by category_id
    category = Category.query.get(category_id)

    if not category:
        return jsonify({"error": "Category not found"}), 404
    
    products = Product.query.filter_by(category_id=category_id).paginate(
        page = page,
        per_page= per_page
    )

    #Convert products to json format
    products_data = list()

    for product in products:
        product_data = {
            'id': product.product_id,
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'category_id': product.category_id
        }
        products_data.append(product_data)

    #Consturcting pagination data
    pagination_data = {
        'total': products.total,
        'pages': products.pages,
        'page': products.page,
        'per_page': products.per_page,
        'has_next': products.has_next,
        'has_prev': products.has_prev
    }

    return jsonify({"category":category.name,"products":products_data, "pagination":pagination_data})


@category_bp.post("/add")
@jwt_required()
@admin_required
def create_category():
    data = request.get_json()

    try:
        new_category = Category(
            name = data.get("name"),
            description = data.get("description")
        )

        new_category.save()

        return jsonify({
            "message":"Category created successfully"
        }), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@category_bp.get("/all")
def get_all_categories():
    data = Category.query.all()

    category_list = []

    for cat in data:
        category_list.append({
            "name": cat.name,
            "desc": cat.description
        })

    return jsonify(category_list), 200



