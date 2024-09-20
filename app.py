from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load Excel data
file_path = 'C:/Users/User/Desktop/try/homart_price_tag.xlsx'
excel_data = pd.read_excel(file_path)

# Function to search for product by code (case-insensitive)
def search_product_by_code(product_code):
    product_code_lower = product_code.lower()  # Convert input to lowercase
    excel_data_lower = excel_data.copy()  # Create a copy of the DataFrame
    excel_data_lower["Product's Code"] = excel_data_lower["Product's Code"].str.lower()  # Convert all product codes to lowercase
    
    result = excel_data_lower[excel_data_lower["Product's Code"] == product_code_lower]
    
    if not result.empty:
        return result[['Product\'s Code', 'Type', "Distributor's Price", 'Contractor Price', 'Price tag', 'Qty in stock']].to_dict(orient='records')
    else:
        return {"message": f"No product found with code {product_code}"}

# Endpoint to search product by code
@app.route('/search', methods=['GET'])
def search():
    product_code = request.args.get('code')
    if product_code:
        result = search_product_by_code(product_code)
        return jsonify(result)
    else:
        return jsonify({"message": "Please provide a product code"}), 400


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
