from datetime import datetime

from utils.file_handler import read_sales_data

from utils.data_processor import parse_transactions
from utils.data_processor import validate_and_filter
from utils.data_processor import calculate_total_revenue
from utils.data_processor import region_wise_sales
from utils.data_processor import top_selling_products
from utils.data_processor import customer_analysis
from utils.data_processor import daily_sales_trend
from utils.data_processor import find_peak_sales_day
from utils.data_processor import low_performing_products
from utils.data_processor import enrich_sales_data

from utils.api_handler import fetch_all_products
from utils.api_handler import create_product_mapping



def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """

    try:
        with open(output_file, 'w', encoding='utf-8') as file:

            # =========================
            # 1. HEADER
            # =========================
            file.write("=" * 44 + "\n")
            file.write("          SALES ANALYTICS REPORT\n")
            file.write(f"    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"    Records Processed: {len(transactions)}\n")
            file.write("=" * 44 + "\n\n")

            # =========================
            # 2. OVERALL SUMMARY
            # =========================
            file.write("OVERALL SUMMARY\n")
            file.write("-" * 44 + "\n")

            total_revenue = calculate_total_revenue(transactions)
            total_transactions = len(transactions)

            avg_order_value = (
                total_revenue / total_transactions
                if total_transactions > 0 else 0
            )

            dates = [tx["Date"] for tx in transactions]
            date_range = (
                f"{min(dates)} to {max(dates)}"
                if dates else "N/A"
            )

            file.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
            file.write(f"Total Transactions:   {total_transactions}\n")
            file.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
            file.write(f"Date Range:           {date_range}\n\n")

            # =========================
            # 3. REGION-WISE PERFORMANCE
            # =========================
            from utils.data_processor import region_wise_sales

            file.write("REGION-WISE PERFORMANCE\n")
            file.write("-" * 44 + "\n")
            file.write("Region    Sales           % of Total   Transactions\n")

            region_stats = region_wise_sales(transactions)

            for region, stats in region_stats.items():
                file.write(
                    f"{region:<9} "
                    f"₹{stats['total_sales']:>12,.2f}   "
                    f"{stats['percentage']:>8.2f}%       "
                    f"{stats['transaction_count']}\n"
                )

            file.write("\n")

            # =========================
            # 4. TOP 5 PRODUCTS
            # =========================
            from utils.data_processor import top_selling_products

            file.write("TOP 5 PRODUCTS\n")
            file.write("-" * 44 + "\n")
            file.write("Rank  Product Name                 Quantity   Revenue\n")

            top_products = top_selling_products(transactions, n=5)

            rank = 1
            for product_name, quantity, revenue in top_products:
                file.write(
                    f"{rank:<5} "
                    f"{product_name:<28} "
                    f"{quantity:>8}   "
                    f"₹{revenue:>10,.2f}\n"
                )
                rank += 1

            file.write("\n")

            # =========================
            # 5. TOP 5 CUSTOMERS
            # =========================
            from utils.data_processor import customer_analysis

            file.write("TOP 5 CUSTOMERS\n")
            file.write("-" * 44 + "\n")
            file.write("Rank  Customer ID   Total Spent      Orders\n")

            customer_stats = customer_analysis(transactions)

            rank = 1
            for customer_id, stats in customer_stats.items():
                if rank > 5:
                    break

                file.write(
                    f"{rank:<5} "
                    f"{customer_id:<13} "
                    f"₹{stats['total_spent']:>12,.2f}   "
                    f"{stats['purchase_count']}\n"
                )
                rank += 1

            file.write("\n")
            # =========================
            # 6. DAILY SALES TREND
            # =========================
            from utils.data_processor import daily_sales_trend

            file.write("DAILY SALES TREND\n")
            file.write("-" * 44 + "\n")
            file.write("Date         Revenue          Transactions   Customers\n")

            daily_trend = daily_sales_trend(transactions)

            for date, stats in daily_trend.items():
                file.write(
                    f"{date:<12} "
                    f"₹{stats['revenue']:>12,.2f}   "
                    f"{stats['transaction_count']:>12}   "
                    f"{stats['unique_customers']}\n"
                )

            file.write("\n")

            # =========================
            # 7. PRODUCT PERFORMANCE ANALYSIS
            # =========================
            from utils.data_processor import (
                find_peak_sales_day,
                low_performing_products,
                region_wise_sales
            )

            file.write("PRODUCT PERFORMANCE ANALYSIS\n")
            file.write("-" * 44 + "\n")

            # Best selling day
            peak_date, peak_revenue, peak_tx_count = find_peak_sales_day(transactions)
            file.write(f"Best Selling Day: {peak_date} (₹{peak_revenue:,.2f}, {peak_tx_count} transactions)\n\n")

            # Low performing products
            low_products = low_performing_products(transactions)

            if low_products:
                file.write("Low Performing Products:\n")
                for product, qty, revenue in low_products:
                    file.write(
                        f"- {product}: {qty} units sold, ₹{revenue:,.2f}\n"
                    )
            else:
                file.write("Low Performing Products: None\n")

            file.write("\n")

            # Average transaction value per region
            file.write("Average Transaction Value per Region:\n")

            region_stats = region_wise_sales(transactions)

            for region, stats in region_stats.items():
                avg_value = (
                    stats['total_sales'] / stats['transaction_count']
                    if stats['transaction_count'] > 0 else 0
                )
                file.write(f"- {region}: ₹{avg_value:,.2f}\n")

            file.write("\n")

            # =========================
            # 8. API ENRICHMENT SUMMARY
            # =========================
            file.write("API ENRICHMENT SUMMARY\n")
            file.write("-" * 44 + "\n")

            total_records = len(enriched_transactions)
            successful = [tx for tx in enriched_transactions if tx.get("API_Match") is True]
            failed = [tx for tx in enriched_transactions if tx.get("API_Match") is False]

            success_count = len(successful)
            failure_count = len(failed)

            success_rate = (
                (success_count / total_records) * 100
                if total_records > 0 else 0
            )

            file.write(f"Total Records Enriched: {total_records}\n")
            file.write(f"Successful Enrichments: {success_count}\n")
            file.write(f"Failed Enrichments:     {failure_count}\n")
            file.write(f"Success Rate:           {success_rate:.2f}%\n\n")

            if failed:
                file.write("Products That Could Not Be Enriched:\n")
                unique_failed_products = sorted(
                    set(tx.get("ProductName") for tx in failed)
                )
                for product in unique_failed_products:
                    file.write(f"- {product}\n")
            else:
                file.write("All products were successfully enriched.\n")

            file.write("\n")


        print(f"Sales report generated at {output_file}")

    except Exception as e:
        print("Error generating sales report:", e)

def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)
        print()

        # 1/10 Read sales data
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions\n")

        # 2/10 Parse and clean
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records\n")

        # 3/10 Filter options
        print("[3/10] Filter Options Available:")
        regions = sorted(set(tx["Region"] for tx in transactions))
        amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in transactions]
        min_amount = min(amounts) if amounts else 0
        max_amount = max(amounts) if amounts else 0

        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min_amount:,.2f} - ₹{max_amount:,.2f}")

        choice = input("Do you want to filter data? (y/n): ").strip().lower()

        if choice == "y":
            region_input = input("Enter region (or press Enter to skip): ").strip()
            min_input = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_input = input("Enter maximum amount (or press Enter to skip): ").strip()

            region_filter = region_input if region_input else None
            min_filter = float(min_input) if min_input else None
            max_filter = float(max_input) if max_input else None

            transactions, invalid_count, summary = validate_and_filter(
                transactions,
                region=region_filter,
                min_amount=min_filter,
                max_amount=max_filter
            )
        else:
            transactions, invalid_count, summary = validate_and_filter(transactions)

        # 4/10 Validation summary
        print("\n[4/10] Validation complete")
        print(f"✓ Valid records: {len(transactions)} | Invalid records: {invalid_count}\n")

        # 5/10 Analysis
        print("[5/10] Analyzing sales data...")
        calculate_total_revenue(transactions)
        region_wise_sales(transactions)
        top_selling_products(transactions)
        customer_analysis(transactions)
        daily_sales_trend(transactions)
        find_peak_sales_day(transactions)
        low_performing_products(transactions)
        print("✓ Analysis complete\n")

        # 6/10 API fetch
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)
        print(f"✓ Fetched {len(api_products)} products\n")

        # 7/10 Enrichment
        print("[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(transactions, product_mapping)
        matched = len([tx for tx in enriched_transactions if tx.get("API_Match")])
        total = len(enriched_transactions)
        print(f"✓ Enriched {matched}/{total} transactions\n")

        # 8/10 Save enriched data
        print("[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # 9/10 Report
        print("[9/10] Generating report...")
        generate_sales_report(transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt\n")

        # 10/10 Done
        print("[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("An error occurred during execution.")
        print("Error details:", e)


if __name__ == "__main__":
    main()
