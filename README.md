# Products API
An products APIs to manage catalog with integration of AWS S3 as file storage service and SQLite as database.

### Project setup
+ Fork and clone the repository
```powershell
https://github.com/<github_username>/products-api
```

+ Create and activate a virtual environment
```powershell
python -m venv env
```

```powershell
source env/scripts/activate
```

+ Install the dependencies
```powershell
pip install -r requirements.txt
```

+ Run the server
```
uvicorn main:app --reload
```

*Running the server will create a `products.db` file locally as a database service*

+ Access the endpoints
```
http://127.0.0.1:8000/docs
```

### Note
Upload a `.env` file with the following credentials
```js
AWS_ACCESS_KEY_ID = 
AWS_SECRET_ACCESS_KEY = 
AWS_REGION = 
S3_Bucket = 
S3_Key = 
```
Add the mentioned fields respectively

### Endpoints

+ **GET** `/` - Check server running status
+ **GET** `/products` - Get all the products
    + Optional - `search?<name>` query to search products by name
+ **POST** `products/` - Create a new product as a form data (as a file is also needed to be posted)
    + Response
    ```py
    {
        "name": "string",
        "category": "string",
        "brand_name": "string",
        "image_url": "string"
    }
    ```
+ **Put** `products/{id}` - Update a the product
+ **Delete** `products/{id}` - Delete a product by id.