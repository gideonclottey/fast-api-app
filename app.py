from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import supplier_pydantic, supplier_pydanticin,Supplier, product_pydantic, product_pydanticin,Products


app = FastAPI()

#sql lite connection through tortoise
register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models":["models"]},
    generate_schemas=True,
    add_exception_handlers= True
)




@app.get("/")
def index():
    return {"message":"go to /docs or /redoc for the api documentation"}

#creating a supplier
@app.post("/supplier")
async def add_supplier(supplier_info:supplier_pydanticin):
    supplier_obj = await Supplier.create(** supplier_info.dict(exclude_unset = True))
    #serialise the data
    response =await supplier_pydantic.from_tortoise_orm(supplier_obj)

    return {"status": "ok", "data":response}

#getting all suppliers 
@app.get("/supplier")
async def get_all_suppliers():
    response = await supplier_pydantic.from_queryset(Supplier.all())
    return {"status": "ok", "data":response}

#get a single supplier 
@app.get("/supplier/{supplier_id}")
async def get_specific_supplier(supplier_id: int):
    response = await supplier_pydantic.from_queryset_single(Supplier.get(id= supplier_id))
    return {"status": "ok", "data":response}
    
#update or making changes to the supplier 
@app.put("/supplier/{supplier_id}")
async def update_supplier(supplier_id:int, update_info: supplier_pydanticin):
    supplier =await Supplier.get(id =supplier_id)
    updated_info = update_info.dict(exclude_unset =True)
    supplier.name = updated_info['name']
    supplier.company = updated_info['company']
    supplier.phone = updated_info['phone']
    supplier.email = updated_info['email']
    await supplier.save()
    #serialise the data
    response = await supplier_pydantic.from_tortoise_orm(supplier)
    return {"status": "ok", "data":response}


#deleting supplier 
@app.delete('/supplier/{supplier_id}')
async def delete_supplier(supplier_id:int):
    await Supplier.get(id=supplier_id).delete()
    return {"status": "ok"}



#product routes starts here ......................

#create new product
@app.post('/product/{supplier_id}')
async def add_product(supplier_id:int,product_details:product_pydanticin):
    supplier = await Supplier.get(id= supplier_id)
    product_details = product_details.dict(exclude_unset = True)
    product_details['revenue'] += product_details['quantity_sold'] * product_details['unit_price']
    product_obj = await Products.create(**product_details,supplied_by= supplier)
    response = await product_pydantic.from_tortoise_orm(product_obj)
    return {"status": "ok", "data":response}

#get all products
@app.get("/products")
async def get_all_products():
    response = await product_pydantic.from_queryset(Products.all())
    return {"status": "ok", "data":response}

# get a specific products
@app.get("/products/{product_id}")
async def get_specific_product(product_id: int):
    response = await product_pydantic.from_queryset_single(Products.get(id=product_id))
    return {"status": "ok", "data":response}


# update product

@app.put('/product/{product_id}')
async def update_product(product_id:int, update_info:product_pydanticin):
    product =await Products.get(id= product_id)
    updated_info = update_info.dict(exclude_unset =True)
    product.name =updated_info['name']
    product.quantity_in_stock =updated_info['quantity_in_stock']
    product.quantity_sold =updated_info['quantity_info']
    product.unit_price =updated_info['unit_price']
    product.revenue += updated_info['quantity_sold'] * update_info['unit_price']
    await product.save()
    #serialise data
    response =await product_pydantic.from_tortoise_orm(product)
    return {"status": "ok", "data":response}


#delete a product

@app.delete("/product/{product_id}")
async def delete_product(product_id:int ):
    await Products.filter(product_id=product_id).delete()
    return {"status": "ok"}
