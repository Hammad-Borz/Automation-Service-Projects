"""Command-line entry point for the ReportFlow demonstration."""

from .workflow import ReportingWorkflow


def main() -> None:
    result = ReportingWorkflow().run()
    print("\nReportFlow demo completed successfully")
    print(f"Revenue: ${result.analytics.kpis['total_revenue']:,.2f}")
    print(f"Orders: {result.analytics.kpis['total_orders']}")
    print(f"Average order value: ${result.analytics.kpis['average_order_value']:,.2f}")
    print(f"Excel report: {result.excel_report}")
    print(f"Text report: {result.text_report}")
    print("CSV exports:")
    for path in result.csv_exports:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
