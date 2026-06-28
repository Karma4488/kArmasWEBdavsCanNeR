# kArmasWEBdavsCanNeR

# Basic scan
python3 kArmasWEBdavsCanNeR.py http://192.168.1.100

# With auth + specific path + JSON report
python3 kArmasWEBdavsCanNeR.py https://target.local -u admin -P pass -p /dav -o report.json

# Skip banner (faster for automation)
python3 kArmasWEBdavsCanNeR.py http://target -y --skip-banner

# Skip brute-force, custom timeout
python3 kArmasWEBdavsCanNeR.py http://target --no-defaults -t 15
