import time
import schedule
from datetime import datetime
from reporter import HotspotReporter


def main_job():
    print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Executing daily hotspot report task...")

    reporter = HotspotReporter()

    all_hotspots = []
    for source in reporter.CONFIG["data_sources"]:
        hotspots = reporter.fetch_hotspots(source)
        all_hotspots.extend(hotspots)
        print(f"Fetched {len(hotspots)} hotspots from {source}")

    all_hotspots.sort(key=lambda x: 0 if x['hot_score'] is None else int(x.get("hot_score", 0)), reverse=True)
    report = reporter.generate_report(all_hotspots)

    if report and "Failed to generate report" not in report:
        reporter.save_report(report)
        # reporter.send_report(report)
    else:
        print("Report generation failed. Nothing saved or sent.")

    print("Task completed")


if __name__ == "__main__":
    main_job()

    schedule.every().day.at("10:00").do(main_job)
    schedule.every().day.at("16:00").do(main_job)

    print("Hotspot monitoring system started. Waiting for scheduled tasks...")
    while True:
        schedule.run_pending()
        time.sleep(60)
