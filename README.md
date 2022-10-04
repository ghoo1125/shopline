# Setup
Clone the repository then run the following command, the script will build and run two containers `api` and `mysql-db`. And feed testing data into database. Please make sure `docker` is installed first.
```
./scripts/run.sh
```

# API
Open browser and connect to service [swagger API](http://localhost:8000/docs) to view and play with the shopping cart and order endpoints. 
There are 3 APIs put item into shopping cart and checkout cart and get cart for better viewing.
<img width="1394" alt="Screen Shot 2022-10-04 at 10 33 20 PM" src="https://user-images.githubusercontent.com/15011876/193847536-be22f0cc-adf5-463e-b79d-1195ef5181bb.png">



# Database
Assume users and products are handled by external services, in previous steps we will feed testing users and products into database.
You could log into DB container using test user account and password `testUser:password` with the commnad.
```
docker exec -it mysql-db mysql -u testUser -p
```
There are total 5 tables under `testDB` database which are User, Product, CartItem, Order and LineItem. Detailed schema please refer to the [file](https://github.com/ghoo1125/shopline/blob/main/shopline/database/model.py).
Testing users and products are shown in the image.
<img width="611" alt="Screen Shot 2022-10-04 at 10 43 08 PM" src="https://user-images.githubusercontent.com/15011876/193850078-2d95719f-0ba2-43a3-bd73-2ffca1c9c103.png">


# Demo
1. Add product to test user's cart
<img width="1073" alt="Screen Shot 2022-10-04 at 10 55 50 PM" src="https://user-images.githubusercontent.com/15011876/193853198-b15ddb42-3f2e-42a3-8f71-25a772b6894e.png">

2. Get test user's cart
<img width="1071" alt="Screen Shot 2022-10-04 at 10 56 39 PM" src="https://user-images.githubusercontent.com/15011876/193853389-55f607b6-be92-4af7-9dd6-532aa5042337.png">

3. Checkout test user's cart
<img width="1072" alt="Screen Shot 2022-10-04 at 10 57 29 PM" src="https://user-images.githubusercontent.com/15011876/193853559-5a99f2c9-1326-4ccc-aa75-7d7efd9f31ea.png">

4. User order, line items have been created in database and inventory of product 111 has been changed (10 -> 9)
<img width="288" alt="Screen Shot 2022-10-04 at 11 00 15 PM" src="https://user-images.githubusercontent.com/15011876/193854276-dcf0924a-e533-4f45-93f7-70dca7227bbb.png">

Note: You could rerun the `run.sh` to reset the environment if something goes wrong 
