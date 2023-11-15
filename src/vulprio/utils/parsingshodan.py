import re

import requests
from bs4 import BeautifulSoup

# Daftar IP yang akan dikunjungi
# Open the file in read mode
with open("listip.txt", "r") as file:
    # Read lines from the file and remove newline characters
    lines = file.readlines()

# Extracting IPs and removing leading/trailing whitespaces
list_of_ips = [line.strip() for line in lines]

# Printing the list of IPs
print("List of IPs:")
for ip in list_of_ips:
    print(ip)


# URL Shodan
shodan_url = "https://www.shodan.io/host/"


# Fungsi untuk melakukan get request ke Shodan untuk setiap IP dan melakukan parsing
def get_and_parse_shodan_data(ip):
    try:
        # Membuat URL spesifik untuk setiap IP
        url = shodan_url + ip
        # print(url)

        # Melakukan get request dengan header Cookie
        headers = {
            "Cookie": f'polito="$updatecookie"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 Safari/537.3",
        }
        response = requests.get(url, headers=headers)
        # print(response.text)

        # Menampilkan status code
        print(f"Status code untuk IP {ip}: {response.status_code}")

        # Melakukan parsing HTML jika response berhasil
        if response.status_code == 200:
            # Menggunakan BeautifulSoup untuk parsing HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Mencari elemen dengan class 'text-dark' untuk mendapatkan teks "Indonesia"
            vulnerabilities_elements = soup.find_all("a", class_="text-dark")

            # Menampilkan CVE ID yang ditemukan
            for element in vulnerabilities_elements:
                cve_match = re.search(r"CVE-\d{4}-\d+", element.text)
                if cve_match:
                    cve_id = cve_match.group()
                    print(f"CVE ID untuk IP {ip}: {cve_id}")

    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")


# Iterasi melalui daftar IP dan panggil fungsi get_and_parse_shodan_data
for ip in list_of_ips:
    get_and_parse_shodan_data(ip)
