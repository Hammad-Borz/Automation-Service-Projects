"""Command-line demo entry point."""

from .workflow import DataOpsWorkflow


def main() -> None:
    result = DataOpsWorkflow().run()
    kpis = result.analytics.kpis
    print("DataOps Automator - Database Automation System")
    print("=" * 48)
    print("\nDatabase initialized successfully")
    print("\nLoading business data...")
    print(f"Records processed: {result.records_processed}")
    print(f"Database records: {result.database_records}")
    print("\nBusiness Analytics:\n")
    print(f"Total Revenue: ${kpis['total_revenue']:,.2f}")
    print(f"Total Orders: {kpis['total_orders']}")
    print(f"Average Order Value: ${kpis['average_order_value']:,.2f}")
    print(f"Total Quantity Sold: {kpis['total_quantity_sold']}")
    print("\nReports generated:")
    for path in result.report_paths:
        print(f"- {path.name}")
    print(f"\nDatabase:\n{result.database_path}")
    print("\nAutomation completed successfully.")


if __name__ == "__main__":
    main()
