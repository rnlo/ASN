from bs4 import BeautifulSoup
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random
import requests
import time
import traceback

# Define the region flag emoji based on the region code
region_and_flag = {
    "US": "🇺🇸",  # United States
    "BR": "🇧🇷",  # Brazil
    "CN": "🇨🇳",  # China
    "RU": "🇷🇺",  # Russia
    "IN": "🇮🇳",  # India
    "GB": "🇬🇧",  # United Kingdom
    "DE": "🇩🇪",  # Germany
    "ID": "🇮🇩",  # Indonesia
    "AU": "🇦🇺",  # Australia
    "PL": "🇵🇱",  # Poland
    "CA": "🇨🇦",  # Canada
    "UA": "🇺🇦",  # Ukraine
    "FR": "🇫🇷",  # France
    "BD": "🇧🇩",  # Bangladesh
    "NL": "🇳🇱",  # Netherlands
    "IT": "🇮🇹",  # Italy
    "RO": "🇷🇴",  # Romania
    "HK": "🇭🇰",  # Hong Kong, China
    "ES": "🇪🇸",  # Spain
    "AR": "🇦🇷",  # Argentina
    "JP": "🇯🇵",  # Japan
    "KR": "🇰🇷",  # Korea, Republic of
    "CH": "🇨🇭",  # Switzerland
    "TR": "🇹🇷",  # Turkey
    "SE": "🇸🇪",  # Sweden
    "ZA": "🇿🇦",  # South Africa
    "BG": "🇧🇬",  # Bulgaria
    "IR": "🇮🇷",  # Iran, Islamic Republic of
    "AT": "🇦🇹",  # Austria
    "VN": "🇻🇳",  # Vietnam
    "NZ": "🇳🇿",  # New Zealand
    "CZ": "🇨🇿",  # Czech Republic
    "SG": "🇸🇬",  # Singapore
    "MX": "🇲🇽",  # Mexico
    "TH": "🇹🇭",  # Thailand
    "PH": "🇵🇭",  # Philippines
    "DK": "🇩🇰",  # Denmark
    "TW": "🇨🇳",  # Taiwan, China
    "CO": "🇨🇴",  # Colombia
    "BE": "🇧🇪",  # Belgium
    "CL": "🇨🇱",  # Chile
    "NO": "🇳🇴",  # Norway
    "FI": "🇫🇮",  # Finland
    "IL": "🇮🇱",  # Israel
    "MY": "🇲🇾",  # Malaysia
    "PK": "🇵🇰",  # Pakistan
    "LV": "🇱🇻",  # Latvia
    "HU": "🇭🇺",  # Hungary
    "IE": "🇮🇪",  # Ireland
    "NG": "🇳🇬",  # Nigeria
    "SI": "🇸🇮",  # Slovenia
    "GR": "🇬🇷",  # Greece
    "EC": "🇪🇨",  # Ecuador
    "SK": "🇸🇰",  # Slovakia
    "KE": "🇰🇪",  # Kenya
    "LT": "🇱🇹",  # Lithuania
    "IQ": "🇮🇶",  # Iraq
    "EE": "🇪🇪",  # Estonia
    "MD": "🇲🇩",  # Moldova, Republic of
    "RS": "🇷🇸",  # Serbia
    "VE": "🇻🇪",  # Venezuela, Bolivarian Republic of
    "KZ": "🇰🇿",  # Kazakhstan
    "NP": "🇳🇵",  # Nepal
    "SA": "🇸🇦",  # Saudi Arabia
    "LB": "🇱🇧",  # Lebanon
    "PE": "🇵🇪",  # Peru
    "HR": "🇭🇷",  # Croatia
    "CY": "🇨🇾",  # Cyprus
    "PA": "🇵🇦",  # Panama
    "MM": "🇲🇲",  # Myanmar
    "GE": "🇬🇪",  # Georgia
    "PT": "🇵🇹",  # Portugal
    "KH": "🇰🇭",  # Cambodia
    "DO": "🇩🇴",  # Dominican Republic
    "AE": "🇦🇪",  # United Arab Emirates
    "BY": "🇧🇾",  # Belarus
    "LU": "🇱🇺",  # Luxembourg
    "AM": "🇦🇲",  # Armenia
    "GH": "🇬🇭",  # Ghana
    "AL": "🇦🇱",  # Albania
    "TZ": "🇹🇿",  # Tanzania, United Republic of
    "CR": "🇨🇷",  # Costa Rica
    "EG": "🇪🇬",  # Egypt
    "HN": "🇭🇳",  # Honduras
    "PR": "🇵🇷",  # Puerto Rico
    "UZ": "🇺🇿",  # Uzbekistan
    "PY": "🇵🇾",  # Paraguay
    "SC": "🇸🇨",  # Seychelles
    "IS": "🇮🇸",  # Iceland
    "AZ": "🇦🇿",  # Azerbaijan
    "KW": "🇰🇼",  # Kuwait
    "GT": "🇬🇹",  # Guatemala
    "AO": "🇦🇴",  # Angola
    "MN": "🇲🇳",  # Mongolia
    "AF": "🇦🇫",  # Afghanistan
    "PS": "🇵🇸",  # Palestine
    "UG": "🇺🇬",  # Uganda
    "KG": "🇰🇬",  # Kyrgyzstan
    "BO": "🇧🇴",  # Bolivia, Plurinational State of
    "MK": "🇲🇰",  # Macedonia, The Former Yugoslav Republic of
    "MU": "🇲🇺",  # Mauritius
    "MT": "🇲🇹",  # Malta
    "BA": "🇧🇦",  # Bosnia and Herzegovina
    "CD": "🇨🇩",  # Congo, The Democratic Republic of the
    "JO": "🇯🇴",  # Jordan
    "SV": "🇸🇻",  # El Salvador
    "BZ": "🇧🇿",  # Belize
    "VG": "🇻🇬",  # Virgin Islands, British
    "UY": "🇺🇾",  # Uruguay
    "ZW": "🇿🇼",  # Zimbabwe
    "LA": "🇱🇦",  # Lao People's Democratic Republic
    "PG": "🇵🇬",  # Papua New Guinea
    "CW": "🇨🇼",  # Curaçao
    "MZ": "🇲🇿",  # Mozambique
    "CM": "🇨🇲",  # Cameroon
    "BW": "🇧🇼",  # Botswana
    "RW": "🇷🇼",  # Rwanda
    "NI": "🇳🇮",  # Nicaragua
    "BT": "🇧🇹",  # Bhutan
    "GI": "🇬🇮",  # Gibraltar
    "TN": "🇹🇳",  # Tunisia
    "MW": "🇲🇼",  # Malawi
    "LY": "🇱🇾",  # Libya
    "CI": "🇨🇮",  # Côte d'Ivoire
    "BF": "🇧🇫",  # Burkina Faso
    "ZM": "🇿🇲",  # Zambia
    "TJ": "🇹🇯",  # Tajikistan
    "BH": "🇧🇭",  # Bahrain
    "LK": "🇱🇰",  # Sri Lanka
    "ME": "🇲🇪",  # Montenegro
    "MA": "🇲🇦",  # Morocco
    "LI": "🇱🇮",  # Liechtenstein
    "IM": "🇮🇲",  # Isle of Man
    "SS": "🇸🇸",  # South Sudan
    "SL": "🇸🇱",  # Sierra Leone
    "SO": "🇸🇴",  # Somalia
    "BM": "🇧🇲",  # Bermuda
    "BJ": "🇧🇯",  # Benin
    "QA": "🇶🇦",  # Qatar
    "OM": "🇴🇲",  # Oman
    "FJ": "🇫🇯",  # Fiji
    "TD": "🇹🇩",  # Chad
    "NC": "🇳🇨",  # New Caledonia
    "NA": "🇳🇦",  # Namibia
    "GN": "🇬🇳",  # Guinea
    "GA": "🇬🇦",  # Gabon
    "DZ": "🇩🇿",  # Algeria
    "CG": "🇨🇬",  # Congo
    "MV": "🇲🇻",  # Maldives
    "SN": "🇸🇳",  # Senegal
    "LR": "🇱🇷",  # Liberia
    "TT": "🇹🇹",  # Trinidad and Tobago
    "SZ": "🇸🇿",  # Swaziland
    "MO": "🇲🇴",  # Macao, China
    "HT": "🇭🇹",  # Haiti
    "AG": "🇦🇬",  # Antigua and Barbuda
    "VU": "🇻🇺",  # Vanuatu
    "SD": "🇸🇩",  # Sudan
    "JM": "🇯🇲",  # Jamaica
    "BS": "🇧🇸",  # Bahamas
    "VI": "🇻🇮",  # Virgin Islands, U.S.
    "TL": "🇹🇱",  # Timor-Leste
    "MG": "🇲🇬",  # Madagascar
    "KY": "🇰🇾",  # Cayman Islands
    "JE": "🇯🇪",  # Jersey
    "GM": "🇬🇲",  # Gambia
    "SM": "🇸🇲",  # San Marino
    "SB": "🇸🇧",  # Solomon Islands
    "BI": "🇧🇮",  # Burundi
    "WS": "🇼🇸",  # Samoa
    "ML": "🇲🇱",  # Mali
    "LS": "🇱🇸",  # Lesotho
    "GG": "🇬🇬",  # Guernsey
    "CV": "🇨🇻",  # Cape Verde
    "TG": "🇹🇬",  # Togo
    "RE": "🇷🇪",  # Réunion
    "NE": "🇳🇪",  # Niger
    "GU": "🇬🇺",  # Guam
    "GD": "🇬🇩",  # Grenada
    "BN": "🇧🇳",  # Brunei Darussalam
    "BB": "🇧🇧",  # Barbados
    "MR": "🇲🇷",  # Mauritania
    "KN": "🇰🇳",  # Saint Kitts and Nevis
    "GP": "🇬🇵",  # Guadeloupe
    "FO": "🇫🇴",  # Faroe Islands
    "SR": "🇸🇷",  # Suriname
    "GQ": "🇬🇶",  # Equatorial Guinea
    "ET": "🇪🇹",  # Ethiopia
    "DM": "🇩🇲",  # Dominica
    "TM": "🇹🇲",  # Turkmenistan
    "MF": "🇲🇫",  # Saint Martin (French part)
    "LC": "🇱🇨",  # Saint Lucia
    "GY": "🇬🇾",  # Guyana
    "GF": "🇬🇫",  # French Guiana
    "CU": "🇨🇺",  # Cuba
    "YE": "🇾🇪",  # Yemen
    "PF": "🇵🇫",  # French Polynesia
    "MQ": "🇲🇶",  # Martinique
    "MH": "🇲🇭",  # Marshall Islands
    "FM": "🇫🇲",  # Micronesia, Federated States of
    "DJ": "🇩🇯",  # Djibouti
    "BQ": "🇧🇶",  # Bonaire, Sint Eustatius and Saba
    "TO": "🇹🇴",  # Tonga
    "SY": "🇸🇾",  # Syrian Arab Republic
    "AW": "🇦🇼",  # Aruba
    "AI": "🇦🇮",  # Anguilla
    "VC": "🇻🇨",  # Saint Vincent and the Grenadines
    "SX": "🇸🇽",  # Sint Maarten (Dutch part)
    "PW": "🇵🇼",  # Palau
    "NR": "🇳🇷",  # Nauru
    "KI": "🇰🇮",  # Kiribati
    "CF": "🇨🇫",  # Central African Republic
    "BL": "🇧🇱",  # Saint Barthélemy
    "VA": "🇻🇦",  # Holy See (Vatican City State)
    "TV": "🇹🇻",  # Tuvalu
    "TK": "🇹🇰",  # Tokelau
    "MC": "🇲🇨",  # Monaco
    "CK": "🇨🇰",  # Cook Islands
    "AS": "🇦🇸",  # American Samoa
    "AD": "🇦🇩",  # Andorra
    "TC": "🇹🇨",  # Turks and Caicos Islands
    "ST": "🇸🇹",  # Sao Tome and Principe
    "NF": "🇳🇫",  # Norfolk Island
    "MP": "🇲🇵",  # Northern Mariana Islands
    "KM": "🇰🇲",  # Comoros
    "GW": "🇬🇼",  # Guinea-Bissau
    "FK": "🇫🇰",  # Falkland Islands (Malvinas)
    "AP": "🌏",  # AP
    "YT": "🇾🇹",  # Mayotte
    "WF": "🇼🇫",  # Wallis and Futuna
    "PM": "🇵🇲",  # Saint Pierre and Miquelon
    "NU": "🇳🇺",  # Niue
    "MS": "🇲🇸",  # Montserrat
    "KP": "🇰🇵",  # Korea, Democratic People's Republic of
    "IO": "🇮🇴",  # British Indian Ocean Territory
    "GL": "🇬🇱",  # Greenland
    "ER": "🇪🇷",  # Eritrea
    "AX": "🇦🇽",  # Åland Islands
    "AQ": "🇦🇶",  # Antarctica
    #   ... and more
}

# Define the header with the User-Agent for the latest macOS Safari browser
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
}


def get_and_parse_data(region_code):
    try:
        url = f"https://bgp.he.net/country/{region_code}"

        with requests.Session() as session:
            retries = Retry(
                total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504]
            )
            session.mount("https://", HTTPAdapter(max_retries=retries))

            session.headers.update(headers)
            response = session.get(url)

            if response.status_code != 200:
                print(f"Request to {url} returned status code {response.status_code}.")
                return None, None, None, None

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("tbody")

            if table is None:
                print(f"No table found in the response from {url}.")
                return None, None, None, None

            selected_data, ipv4_data, ipv6_data = [], [], []
            for row in table.find_all("tr"):
                columns = row.find_all("td")

                if columns[0].text.strip().startswith("AS"):
                    asn = columns[0].text.strip().replace("AS", "IP-ASN,")
                    selected_data.append(asn)

                    if columns[2].text.strip() != "0":
                        ipv4_data.append(asn)
                    if columns[4].text.strip() != "0":
                        ipv6_data.append(asn)

        return selected_data, ipv4_data, ipv6_data, url
    except requests.exceptions.RequestException as e:
        print(
            f"Request error occurred while scraping data for region code {region_code}. Error: {e}"
        )
        return None, None, None, None
    except Exception as e:
        print(
            f"Error occurred while scraping data for region code {region_code}. Error: {e}"
        )
        print(traceback.format_exc())
        return None, None, None, None


def write_data_to_file(region_code, selected_data, url, suffix="", ip_version=None):
    try:
        if len(selected_data) > 0:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            region_flag = region_and_flag.get(region_code.upper(), "")

            file_name = f"{region_code}{suffix}.list"
            with open(file_name, "w") as file:
                file.write(f"# {region_flag}{region_code}ASN Generated from {url}\n")
                file.write(f"# Updated at UTC {timestamp}\n")
                if ip_version:
                    file.write(f"# {ip_version} Only\n")
                file.write(f"# Total lines: {len(selected_data)}\n")
                file.write("# https://github.com/rnlo/ASN\n")
                file.writelines(f"{line}\n" for line in selected_data)
            print(f"{file_name} generated from {url} and saved.")
        else:
            print(
                f"Result has less than 0 lines for {region_code}. Not writing to file."
            )
    except IOError as e:
        print(
            f"IOError occurred while writing data to file for region code {region_code}. Error: {e}"
        )
    except Exception as e:
        print(
            f"Error occurred while writing data to file for region code {region_code}. Error: {e}"
        )
        print(traceback.format_exc())


def scrape_data():
    try:
        for region_code in region_and_flag.keys():
            selected_data, ipv4_data, ipv6_data, url = get_and_parse_data(region_code)

            # Check if data or url is None
            if (
                selected_data is None
                or ipv4_data is None
                or ipv6_data is None
                or url is None
            ):
                print(f"Skipping region code {region_code} due to missing data.")
                continue

            write_data_to_file(region_code, selected_data, url)  # Save the main data
            write_data_to_file(
                region_code, ipv4_data, url, suffix="4", ip_version="IPv4"
            )  # Save the IPv4 data
            write_data_to_file(
                region_code, ipv6_data, url, suffix="6", ip_version="IPv6"
            )  # Save the IPv6 data

            # Add a random delay between requests
            time.sleep(
                random.uniform(1, 3)
            )  # delay for a random number of seconds between 1 and 3
    except Exception as e:
        print(f"Error occurred while scraping data. Error: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    scrape_data()
