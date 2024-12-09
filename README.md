# Cafe API Project

This project is a Flask-based API for managing a database of cafes. The API allows users to retrieve information about cafes, search for cafes by location, fetch a random cafe, update cafe details, and add or delete cafes securely.You can use [Postman](https://www.postman.com/) to test the API endpoints

## Features

- **Database Integration**: Utilizes SQLite and SQLAlchemy for database management.
- **Endpoints**:
  - `GET /random`: Fetch a random cafe.
  - `GET /all`: Retrieve all cafes.
  - `GET /search?loc=<location>`: Search cafes by location.
  - `PATCH /update-price/<id>`: Update the coffee price of a specific cafe.
  - `POST /add`: Add a new cafe.
  - `DELETE /report-closed/<id>`: Securely delete a cafe using an API key.
- **JSON Responses**: All data is returned in JSON format.

## Project Structure

```
project/
│
├── app.py                 # Main application file
├── templates/
│   └── index.html         # Home page template
├── cafes.db               # SQLite database
├── static/                # Static files (if any)
└── README.md              # Documentation
```

## Setup Instructions

### Prerequisites

- Python 3.x
- Flask
- Flask-SQLAlchemy

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Dimplektech/Cafe-API-Project
   cd project
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   flask run
   ```

   The application will be available at `http://127.0.0.1:5000/`.

5. Use Postman or any HTTP client to test the API endpoints.

## API Endpoints

### 1. Get a Random Cafe

**Endpoint:**
```
GET /random
```

**Description:**
Returns a random cafe from the database.

**Response Example:**
```json
{
  "cafe": {
    "id": 1,
    "name": "Cafe Latte",
    "map_url": "https://maps.google.com/",
    "img_url": "https://example.com/image.jpg",
    "location": "New York",
    "seats": "50",
    "has_toilet": true,
    "has_wifi": true,
    "has_sockets": true,
    "can_take_calls": false,
    "coffee_price": "$5"
  }
}
```

---

### 2. Get All Cafes

**Endpoint:**
```
GET /all
```

**Description:**
Returns all cafes in the database.

**Response Example:**
```json
[
  {
    "id": 1,
    "name": "Cafe Latte",
    "map_url": "https://maps.google.com/",
    "img_url": "https://example.com/image.jpg",
    "location": "New York",
    "seats": "50",
    "has_toilet": true,
    "has_wifi": true,
    "has_sockets": true,
    "can_take_calls": false,
    "coffee_price": "$5"
  },
  ...
]
```

---

### 3. Search Cafes by Location

**Endpoint:**
```
GET /search?loc=<location>
```

**Description:**
Searches for cafes in the specified location.

**Query Parameters:**
- `loc` (string): The location to search for.

**Example:**
```
GET /search?loc=Peckham
```

**Response Example:**
```json
[
  {
    "id": 1,
    "name": "Cafe Latte",
    "map_url": "https://maps.google.com/",
    "img_url": "https://example.com/image.jpg",
    "location": "Peckham",
    "seats": "50",
    "has_toilet": true,
    "has_wifi": true,
    "has_sockets": true,
    "can_take_calls": false,
    "coffee_price": "$5"
  }
]
```

**Error Example:**
```json
{
  "error": {
    "Not Found": "Sorry, We don't have cafe at this location."
  }
}
```

---

### 4. Update Coffee Price

**Endpoint:**
```
PATCH /update-price/<id>
```

**Description:**
Updates the coffee price of a specific cafe.

**Query Parameters:**
- `coffee_price` (string): The new coffee price.

**Example:**
```
PATCH /update-price/30?coffee_price=£3.00
```

**Response Example:**
```json
{
  "success": "The coffee price has been updated."
}
```

**Error Example:**
```json
{
  "error": {
    "Not Found": "No cafe found with the provided ID."
  }
}
```

---

### 5. Add a New Cafe

**Endpoint:**
```
POST /add
```

**Description:**
Adds a new cafe to the database. This endpoint requires authentication using an API key.

**Query Parameters:**
- `name` (string): The cafe name.
- `map_url` (string): URL to the cafe's location on the map.
- `img_url` (string): URL to an image of the cafe.
- `location` (string): The location of the cafe.
- `seats` (string): The number of seats available.
- `has_toilet` (boolean): Whether the cafe has a toilet.
- `has_wifi` (boolean): Whether the cafe offers Wi-Fi.
- `has_sockets` (boolean): Whether the cafe has power sockets.
- `can_take_calls` (boolean): Whether calls can be taken in the cafe.
- `coffee_price` (string): The price of a coffee.

**Example:**
```
POST /add?name=Timberyard-London&map_url=https://www.google.com/maps/...&img_url=https://example.com/image.jpg&location=Soho&seats=20-30&has_toilet=True&has_wifi=True&has_sockets=True&can_take_calls=True&coffee_price=£3.75
```

**Response Example:**
```json
{
  "success": "New cafe added successfully."
}
```

---

### 6. Remove a Closed Cafe (Authenticated)

**Endpoint:**
```
DELETE /report-closed/<id>
```

**Description:**
Deletes a cafe from the database. This endpoint requires an API key for authentication.

**Query Parameters:**
- `api-key` (string): The API key for authentication.

**Example:**
```
DELETE /report-closed/20?api-key=TopSecretAPIKey
```

**Response Example:**
```json
{
  "success": "Cafe has been deleted successfully."
}
```

**Error Example:**
```json
{
  "error": {
    "Unauthorized": "Invalid API key."
  }
}
```

---

## Postman Documentation

You can use [Postman](https://www.postman.com/) to test the API endpoints. Follow these steps:

1. Open Postman and create a new collection.
2. Add requests to the collection for each endpoint:
   - `GET /random`
   - `GET /all`
   - `GET /search?loc=<location>`
   - `PATCH /update-price/<id>`
   - `POST /add` (Add Authorization header with API key)
   - `DELETE /report-closed/<id>` (Add Authorization header with API key)
3. Set the base URL to `http://127.0.0.1:5000`.
4. Test the requests by sending them to the server.

For more details, export the Postman collection and include it in the repository under the name `postman_collection.json`.

## Future Enhancements

- Add authentication for secure endpoints.
- Include additional endpoints for adding, updating, and deleting cafes.
- Implement filtering and sorting options for cafes.
- Enhance error handling and validation.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
