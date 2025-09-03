cd /app/arxiv_web

cp arxiv_wildfire_database.db backups/arxiv_wildfire_database.db.latestbackup
cp arxiv_wildfire_intervals.json backups/arxiv_wildfire_intervals.json.latestbackup
cp arxiv_wildfire_excel.xlsx backups/arxiv_wildfire_excel.xlsx.latestbackup

gsutil cp gs://datasciencedev/satellite_imaging/wildfire_forcasting/paper_aggregator/latest.csv temp.csv

python store_data.py >> store_data.log 2>&1