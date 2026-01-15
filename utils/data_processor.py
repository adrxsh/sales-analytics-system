def split_sales_data(lines):
    """
    Splits raw file lines into columns using | delimiter.
    Skips header and empty lines.
    """

    split_rows = []

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if line == "":
            continue

        # Skip header line
        if line.startswith("TransactionID"):
            continue

        # Split by pipe delimiter
        columns = line.split("|")

        split_rows.append(columns)

    print(f"Total data rows after splitting (before cleaning): {len(split_rows)}")

    return split_rows

def clean_sales_data(split_rows):
    """
    Cleans and validates sales data.
    Removes invalid records and cleans valid ones.
    """

    valid_records = []
    invalid_count = 0

    for row in split_rows:
        # Skip rows that do not have exactly 8 columns
        if len(row) != 8:
            invalid_count += 1
            continue

        transaction_id, date, product_id, product_name, quantity, unit_price, customer_id, region = row

        # Validation checks
        if not transaction_id.startswith("T"):
            invalid_count += 1
            continue

        if customer_id == "" or region == "":
            invalid_count += 1
            continue

        # Clean numbers (remove commas)
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except:
            invalid_count += 1
            continue

        if quantity <= 0 or unit_price <= 0:
            invalid_count += 1
            continue

        # Clean product name (remove commas)
        product_name = product_name.replace(",", "")

        # Store cleaned record as dictionary
        record = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        valid_records.append(record)

    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    return valid_records

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    """

    transactions = []

    for line in raw_lines:
        # Split by pipe delimiter
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        transaction_id = parts[0]
        date = parts[1]
        product_id = parts[2]
        product_name = parts[3]
        quantity = parts[4]
        unit_price = parts[5]
        customer_id = parts[6]
        region = parts[7]

        # Clean ProductName (remove commas)
        product_name = product_name.replace(",", "")

        # Clean numeric fields (remove commas)
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        # Convert data types
        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            # Skip rows with invalid numeric data
            continue

        transaction = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        transactions.append(transaction)

    return transactions

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """

    valid_transactions = []
    invalid_count = 0

    total_input = len(transactions)

    # Collect regions and transaction amounts for display
    available_regions = set()
    amounts = []

    for tx in transactions:
        available_regions.add(tx.get("Region"))
        amounts.append(tx.get("Quantity", 0) * tx.get("UnitPrice", 0))

    print("Available regions:", sorted(available_regions))
    if amounts:
        print("Transaction amount range:", min(amounts), "to", max(amounts))

    # ---------------- VALIDATION ----------------
    for tx in transactions:
        # Required fields check
        required_fields = [
            "TransactionID", "Date", "ProductID", "ProductName",
            "Quantity", "UnitPrice", "CustomerID", "Region"
        ]

        if not all(field in tx for field in required_fields):
            invalid_count += 1
            continue

        if tx["Quantity"] <= 0 or tx["UnitPrice"] <= 0:
            invalid_count += 1
            continue

        if not tx["TransactionID"].startswith("T"):
            invalid_count += 1
            continue

        if not tx["ProductID"].startswith("P"):
            invalid_count += 1
            continue

        if not tx["CustomerID"].startswith("C"):
            invalid_count += 1
            continue

        valid_transactions.append(tx)

    filtered_by_region = 0
    filtered_by_amount = 0

    # ---------------- REGION FILTER ----------------
    if region:
        before = len(valid_transactions)
        valid_transactions = [tx for tx in valid_transactions if tx["Region"] == region]
        filtered_by_region = before - len(valid_transactions)
        print("After region filter:", len(valid_transactions))

    # ---------------- AMOUNT FILTER ----------------
    if min_amount is not None or max_amount is not None:
        before = len(valid_transactions)

        def in_range(tx):
            amount = tx["Quantity"] * tx["UnitPrice"]
            if min_amount is not None and amount < min_amount:
                return False
            if max_amount is not None and amount > max_amount:
                return False
            return True

        valid_transactions = [tx for tx in valid_transactions if in_range(tx)]
        filtered_by_amount = before - len(valid_transactions)
        print("After amount filter:", len(valid_transactions))

    filter_summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)
    """

    total_revenue = 0.0

    for tx in transactions:
        total_revenue += tx["Quantity"] * tx["UnitPrice"]

    return total_revenue

def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics
    """

    region_data = {}
    total_sales_all_regions = 0.0

    # First pass: calculate total sales per region and overall total
    for tx in transactions:
        region = tx["Region"]
        sale_amount = tx["Quantity"] * tx["UnitPrice"]

        total_sales_all_regions += sale_amount

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += sale_amount
        region_data[region]["transaction_count"] += 1

    # Second pass: calculate percentage contribution
    for region in region_data:
        percentage = (region_data[region]["total_sales"] / total_sales_all_regions) * 100
        region_data[region]["percentage"] = round(percentage, 2)

    # Sort regions by total_sales descending
    sorted_region_data = dict(
        sorted(
            region_data.items(),
            key=lambda item: item[1]["total_sales"],
            reverse=True
        )
    )

    return sorted_region_data

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_data = {}

    # Aggregate quantity and revenue by ProductName
    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        product_data[product]["total_quantity"] += quantity
        product_data[product]["total_revenue"] += revenue

    # Convert to list of tuples
    product_list = []
    for product, data in product_data.items():
        product_list.append(
            (product, data["total_quantity"], data["total_revenue"])
        )

    # Sort by total quantity sold (descending)
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Return top n products
    return product_list[:n]

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics
    """

    customer_data = {}

    # Aggregate data by CustomerID
    for tx in transactions:
        customer_id = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        product = tx["ProductName"]

        if customer_id not in customer_data:
            customer_data[customer_id] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_data[customer_id]["total_spent"] += amount
        customer_data[customer_id]["purchase_count"] += 1
        customer_data[customer_id]["products_bought"].add(product)

    # Calculate average order value and convert product sets to lists
    for customer_id in customer_data:
        total_spent = customer_data[customer_id]["total_spent"]
        purchase_count = customer_data[customer_id]["purchase_count"]

        customer_data[customer_id]["avg_order_value"] = round(
            total_spent / purchase_count, 2
        )

        customer_data[customer_id]["products_bought"] = list(
            customer_data[customer_id]["products_bought"]
        )

    # Sort customers by total_spent descending
    sorted_customer_data = dict(
        sorted(
            customer_data.items(),
            key=lambda item: item[1]["total_spent"],
            reverse=True
        )
    )

    return sorted_customer_data

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date
    """

    daily_data = {}

    # Aggregate data by date
    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        customer = tx["CustomerID"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += amount
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(customer)

    # Prepare final output and sort chronologically by date
    sorted_daily_data = {}

    for date in sorted(daily_data.keys()):
        sorted_daily_data[date] = {
            "revenue": daily_data[date]["revenue"],
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    return sorted_daily_data

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)
    """

    daily_totals = {}

    # Aggregate revenue and transaction count by date
    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if date not in daily_totals:
            daily_totals[date] = {
                "revenue": 0.0,
                "transaction_count": 0
            }

        daily_totals[date]["revenue"] += amount
        daily_totals[date]["transaction_count"] += 1

    # Find the date with maximum revenue
    peak_date = None
    peak_revenue = 0.0
    peak_tx_count = 0

    for date, stats in daily_totals.items():
        if stats["revenue"] > peak_revenue:
            peak_revenue = stats["revenue"]
            peak_tx_count = stats["transaction_count"]
            peak_date = date

    return (peak_date, peak_revenue, peak_tx_count)

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_data = {}

    # Aggregate quantity and revenue by ProductName
    for tx in transactions:
        product = tx["ProductName"]
        quantity = tx["Quantity"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if product not in product_data:
            product_data[product] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        product_data[product]["total_quantity"] += quantity
        product_data[product]["total_revenue"] += revenue

    # Filter products below threshold
    low_products = []

    for product, data in product_data.items():
        if data["total_quantity"] < threshold:
            low_products.append(
                (product, data["total_quantity"], data["total_revenue"])
            )

    # Sort by TotalQuantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """

    if not enriched_transactions:
        print("No enriched data to save.")
        return

    headers = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region',
        'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
    ]

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('|'.join(headers) + '\n')

            for tx in enriched_transactions:
                row = []
                for h in headers:
                    value = tx.get(h)
                    if value is None:
                        row.append('')
                    else:
                        row.append(str(value))

                file.write('|'.join(row) + '\n')

        print(f"Enriched data saved to {filename}")

    except Exception as e:
        print("Error saving enriched data:", e)

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()
        product_id_str = tx.get("ProductID", "")

        try:
            numeric_id = int(product_id_str.replace('P', ''))
        except ValueError:
            numeric_id = None

        if numeric_id and numeric_id in product_mapping:
            api_product = product_mapping[numeric_id]
            enriched_tx['API_Category'] = api_product.get('category')
            enriched_tx['API_Brand'] = api_product.get('brand')
            enriched_tx['API_Rating'] = api_product.get('rating')
            enriched_tx['API_Match'] = True
        else:
            enriched_tx['API_Category'] = None
            enriched_tx['API_Brand'] = None
            enriched_tx['API_Rating'] = None
            enriched_tx['API_Match'] = False

        enriched_transactions.append(enriched_tx)

    # IMPORTANT: Save enriched data to file
    save_enriched_data(enriched_transactions)

    return enriched_transactions



