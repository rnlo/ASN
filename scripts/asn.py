import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Define the region flag emoji based on the region code
region_flags = {
    'US': '🇺🇸',  # United States
    'BR': '🇧🇷',  # Brazil
    'CN': '🇨🇳',  # China
    'RU': '🇷🇺',  # Russia
    'IN': '🇮🇳',  # India
    'GB': '🇬🇧',  # United Kingdom
    'DE': '🇩🇪',  # Germany
    'ID': '🇮🇩',  # Indonesia
    'AU': '🇦🇺',  # Australia
    'PL': '🇵🇱',  # Poland
    'CA': '🇨🇦',  # Canada
    'UA': '🇺🇦',  # Ukraine
    'FR': '🇫🇷',  # France
    'BD': '🇧🇩',  # Bangladesh
    'NL': '🇳🇱',  # Netherlands
    'IT': '🇮🇹',  # Italy
    'RO': '🇷🇴',  # Romania
    'HK': '🇭🇰',  # Hong Kong, China
    'ES': '🇪🇸',  # Spain
    'AR': '🇦🇷',  # Argentina
    'JP': '🇯🇵',  # Japan
    'KR': '🇰🇷',  # Korea, Republic of
    'CH': '🇨🇭',  # Switzerland
    'TR': '🇹🇷',  # Turkey
    'SE': '🇸🇪',  # Sweden
    'ZA': '🇿🇦',  # South Africa
    'BG': '🇧🇬',  # Bulgaria
    'IR': '🇮🇷',  # Iran, Islamic Republic of
    'AT': '🇦🇹',  # Austria
    'VN': '🇻🇳',  # Vietnam
    'NZ': '🇳🇿',  # New Zealand
    'CZ': '🇨🇿',  # Czech Republic
    'SG': '🇸🇬',  # Singapore
    'MX': '🇲🇽',  # Mexico
    'TH': '🇹🇭',  # Thailand
    'PH': '🇵🇭',  # Philippines
    'DK': '🇩🇰',  # Denmark
    'TW': '🇨🇳',  # Taiwan, China
    'CO': '🇨🇴',  # Colombia
    'BE': '🇧🇪',  # Belgium
    'CL': '🇨🇱',  # Chile
    'NO': '🇳🇴',  # Norway
    'FI': '🇫🇮',  # Finland
    'IL': '🇮🇱',  # Israel
    'MY': '🇲🇾',  # Malaysia
    'PK': '🇵🇰',  # Pakistan
    'LV': '🇱🇻',  # Latvia
    'HU': '🇭🇺',  # Hungary
    'IE': '🇮🇪',  # Ireland
    'NG': '🇳🇬',  # Nigeria
    'SI': '🇸🇮',  # Slovenia
    'GR': '🇬🇷',  # Greece
    'EC': '🇪🇨',  # Ecuador
    'SK': '🇸🇰',  # Slovakia
    'KE': '🇰🇪',  # Kenya
    'LT': '🇱🇹',  # Lithuania
    'IQ': '🇮🇶',  # Iraq
    'EE': '🇪🇪',  # Estonia
    'MD': '🇲🇩',  # Moldova, Republic of
    'RS': '🇷🇸',  # Serbia
    'VE': '🇻🇪',  # Venezuela, Bolivarian Republic of
    'KZ': '🇰🇿',  # Kazakhstan
    'NP': '🇳🇵',  # Nepal
    'SA': '🇸🇦',  # Saudi Arabia
    'LB': '🇱🇧',  # Lebanon
    'PE': '🇵🇪',  # Peru
    'HR': '🇭🇷',  # Croatia
    'CY': '🇨🇾',  # Cyprus
    'PA': '🇵🇦',  # Panama
    'MM': '🇲🇲',  # Myanmar
    'GE': '🇬🇪',  # Georgia
    'PT': '🇵🇹',  # Portugal
    'KH': '🇰🇭',  # Cambodia
    'DO': '🇩🇴',  # Dominican Republic
    'AE': '🇦🇪',  # United Arab Emirates
    'BY': '🇧🇾',  # Belarus
    'LU': '🇱🇺',  # Luxembourg
    'AM': '🇦🇲',  # Armenia
    'GH': '🇬🇭',  # Ghana
    'AL': '🇦🇱',  # Albania
    'TZ': '🇹🇿',  # Tanzania, United Republic of
    'CR': '🇨🇷',  # Costa Rica
    'EG': '🇪🇬',  # Egypt
    'HN': '🇭🇳',  # Honduras
    'PR': '🇵🇷',  # Puerto Rico
    'UZ': '🇺🇿',  # Uzbekistan
    'PY': '🇵🇾',  # Paraguay
    'SC': '🇸🇨',  # Seychelles
    'IS': '🇮🇸',  # Iceland
    'AZ': '🇦🇿',  # Azerbaijan
    'KW': '🇰🇼',  # Kuwait
    'GT': '🇬🇹',  # Guatemala
    'AO': '🇦🇴',  # Angola
    'MN': '🇲🇳',  # Mongolia
    'AF': '🇦🇫',  # Afghanistan
    'PS': '🇵🇸',  # Palestine
    'UG': '🇺🇬',  # Uganda
    'KG': '🇰🇬',  # Kyrgyzstan
    'BO': '🇧🇴',  # Bolivia, Plurinational State of
    'MK': '🇲🇰',  # Macedonia, The Former Yugoslav Republic of
    'MU': '🇲🇺',  # Mauritius
    'MT': '🇲🇹',  # Malta
    'BA': '🇧🇦',  # Bosnia and Herzegovina
    'CD': '🇨🇩',  # Congo, The Democratic Republic of the
    'JO': '🇯🇴',  # Jordan
    'SV': '🇸🇻',  # El Salvador
    'BZ': '🇧🇿',  # Belize
    'VG': '🇻🇬',  # Virgin Islands, British
    'UY': '🇺🇾',  # Uruguay
    'ZW': '🇿🇼',  # Zimbabwe
    'LA': '🇱🇦',  # Lao People's Democratic Republic
    'PG': '🇵🇬',  # Papua New Guinea
    'CW': '🇨🇼',  # Curaçao
    'MZ': '🇲🇿',  # Mozambique
    'CM': '🇨🇲',  # Cameroon
    'BW': '🇧🇼',  # Botswana
    'RW': '🇷🇼',  # Rwanda
    'NI': '🇳🇮',  # Nicaragua
    'BT': '🇧🇹',  # Bhutan
    'GI': '🇬🇮',  # Gibraltar
    'TN': '🇹🇳',  # Tunisia
    'MW': '🇲🇼',  # Malawi
    'LY': '🇱🇾',  # Libya
    'CI': '🇨🇮',  # Côte d'Ivoire
    'BF': '🇧🇫',  # Burkina Faso
    'ZM': '🇿🇲',  # Zambia
    'TJ': '🇹🇯',  # Tajikistan
    'BH': '🇧🇭',  # Bahrain
    'LK': '🇱🇰',  # Sri Lanka
    'ME': '🇲🇪',  # Montenegro
    'MA': '🇲🇦',  # Morocco
    'LI': '🇱🇮',  # Liechtenstein
    'IM': '🇮🇲',  # Isle of Man
    'SS': '🇸🇸',  # South Sudan
    'SL': '🇸🇱',  # Sierra Leone
    'SO': '🇸🇴',  # Somalia
    'BM': '🇧🇲',  # Bermuda
    'BJ': '🇧🇯',  # Benin
    'QA': '🇶🇦',  # Qatar
    'OM': '🇴🇲',  # Oman
    'FJ': '🇫🇯',  # Fiji
    'TD': '🇹🇩',  # Chad
    'NC': '🇳🇨',  # New Caledonia
    'NA': '🇳🇦',  # Namibia
    'GN': '🇬🇳',  # Guinea
    'GA': '🇬🇦',  # Gabon
    'DZ': '🇩🇿',  # Algeria
    'CG': '🇨🇬',  # Congo
    'MV': '🇲🇻',  # Maldives
    'SN': '🇸🇳',  # Senegal
    'LR': '🇱🇷',  # Liberia
    'TT': '🇹🇹',  # Trinidad and Tobago
    'SZ': '🇸🇿',  # Swaziland
    'MO': '🇲🇴',  # Macao, China
    'HT': '🇭🇹',  # Haiti
    'AG': '🇦🇬',  # Antigua and Barbuda
    'VU': '🇻🇺',  # Vanuatu
    'SD': '🇸🇩',  # Sudan
    'JM': '🇯🇲',  # Jamaica
    'BS': '🇧🇸',  # Bahamas
    'VI': '🇻🇮',  # Virgin Islands, U.S.
    'TL': '🇹🇱',  # Timor-Leste
    'MG': '🇲🇬',  # Madagascar
    'KY': '🇰🇾',  # Cayman Islands
    'JE': '🇯🇪',  # Jersey
    'GM': '🇬🇲',  # Gambia
    'SM': '🇸🇲',  # San Marino
    'SB': '🇸🇧',  # Solomon Islands
    'BI': '🇧🇮',  # Burundi
    'WS': '🇼🇸',  # Samoa
    'ML': '🇲🇱',  # Mali
    'LS': '🇱🇸',  # Lesotho
    'GG': '🇬🇬',  # Guernsey
    'CV': '🇨🇻',  # Cape Verde
    'TG': '🇹🇬',  # Togo
    'RE': '🇷🇪',  # Réunion
    'NE': '🇳🇪',  # Niger
    'GU': '🇬🇺',  # Guam
    'GD': '🇬🇩',  # Grenada
    'BN': '🇧🇳',  # Brunei Darussalam
    'BB': '🇧🇧',  # Barbados
    'MR': '🇲🇷',  # Mauritania
    'KN': '🇰🇳',  # Saint Kitts and Nevis
    'GP': '🇬🇵',  # Guadeloupe
    'FO': '🇫🇴',  # Faroe Islands
    'SR': '🇸🇷',  # Suriname
    'GQ': '🇬🇶',  # Equatorial Guinea
    'ET': '🇪🇹',  # Ethiopia
    'DM': '🇩🇲',  # Dominica
    'TM': '🇹🇲',  # Turkmenistan
    'MF': '🇲🇫',  # Saint Martin (French part)
    'LC': '🇱🇨',  # Saint Lucia
    'GY': '🇬🇾',  # Guyana
    'GF': '🇬🇫',  # French Guiana
    'CU': '🇨🇺',  # Cuba
    'YE': '🇾🇪',  # Yemen
    'PF': '🇵🇫',  # French Polynesia
    'MQ': '🇲🇶',  # Martinique
    'MH': '🇲🇭',  # Marshall Islands
    'FM': '🇫🇲',  # Micronesia, Federated States of
    'DJ': '🇩🇯',  # Djibouti
    'BQ': '🇧🇶',  # Bonaire, Sint Eustatius and Saba
    'TO': '🇹🇴',  # Tonga
    'SY': '🇸🇾',  # Syrian Arab Republic
    'AW': '🇦🇼',  # Aruba
    'AI': '🇦🇮',  # Anguilla
    'VC': '🇻🇨',  # Saint Vincent and the Grenadines
    'SX': '🇸🇽',  # Sint Maarten (Dutch part)
    'PW': '🇵🇼',  # Palau
    'NR': '🇳🇷',  # Nauru
    'KI': '🇰🇮',  # Kiribati
    'CF': '🇨🇫',  # Central African Republic
    'BL': '🇧🇱',  # Saint Barthélemy
    'VA': '🇻🇦',  # Holy See (Vatican City State)
    'TV': '🇹🇻',  # Tuvalu
    'TK': '🇹🇰',  # Tokelau
    'MC': '🇲🇨',  # Monaco
    'CK': '🇨🇰',  # Cook Islands
    'AS': '🇦🇸',  # American Samoa
    'AD': '🇦🇩',  # Andorra
    'TC': '🇹🇨',  # Turks and Caicos Islands
    'ST': '🇸🇹',  # Sao Tome and Principe
    'NF': '🇳🇫',  # Norfolk Island
    'MP': '🇲🇵',  # Northern Mariana Islands
    'KM': '🇰🇲',  # Comoros
    'GW': '🇬🇼',  # Guinea-Bissau
    'FK': '🇫🇰',  # Falkland Islands (Malvinas)
    'GL': '🇬🇱',  # Greenland
#   ... and more
}

def scrape_data(region_code):
    # Define the URL to scrape
    url = f'https://bgp.he.net/country/{region_code}'

    # Define the header with the User-Agent for the latest macOS Safari browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15'
    }

    # Make the request with the specified headers
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract content from tbody table where td[2] is not empty or td[3] is not 0
    # Replace "AS" with "IP-ASN,"
    table = soup.find('tbody')
    selected_data = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 2 and (columns[1].text.strip() or columns[2].text.strip() != '0') and columns[0].text.strip().startswith("AS"):
            selected_data.append(columns[0].text.strip().replace("AS", "IP-ASN,"))

    # Check if the result contains more than 0 lines, if so, write to file
    if len(selected_data) > 0:

        # Write the scraped content to the file with timestamp at the beginning
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        region_flag = region_flags.get(region_code.upper(), '')

        with open(f'{region_code}.list', 'w') as file:
            file.write(f"# {region_flag}{region_code}ASN Generated from {url}\n")
            file.write(f"# Updated at UTC {timestamp}\n")
            file.write(f"# Total lines: {len(selected_data)}\n")
            file.write("# https://github.com/rnlo/ASN\n")
            for item in selected_data:
                file.write(item + '\n')
        print(f"{region_code}ASN Generated from {url} and saved to ASN{region_code}.list.")
    else:
        print(f"Result has less than 0 lines for {region_code}. Not writing to file.")

# Example usage:
scrape_data('US')  # United States
scrape_data('BR')  # Brazil
scrape_data('CN')  # China
scrape_data('RU')  # Russia
scrape_data('IN')  # India
scrape_data('GB')  # United Kingdom
scrape_data('DE')  # Germany
scrape_data('ID')  # Indonesia
scrape_data('AU')  # Australia
scrape_data('PL')  # Poland
scrape_data('CA')  # Canada
scrape_data('UA')  # Ukraine
scrape_data('FR')  # France
scrape_data('BD')  # Bangladesh
scrape_data('NL')  # Netherlands
scrape_data('IT')  # Italy
scrape_data('RO')  # Romania
scrape_data('HK')  # Hong Kong, China
scrape_data('ES')  # Spain
scrape_data('AR')  # Argentina
scrape_data('JP')  # Japan
scrape_data('KR')  # Korea, Republic of
scrape_data('CH')  # Switzerland
scrape_data('TR')  # Turkey
scrape_data('SE')  # Sweden
scrape_data('ZA')  # South Africa
scrape_data('BG')  # Bulgaria
scrape_data('IR')  # Iran, Islamic Republic of
scrape_data('AT')  # Austria
scrape_data('VN')  # Vietnam
scrape_data('NZ')  # New Zealand
scrape_data('CZ')  # Czech Republic
scrape_data('SG')  # Singapore
scrape_data('MX')  # Mexico
scrape_data('TH')  # Thailand
scrape_data('PH')  # Philippines
scrape_data('DK')  # Denmark
scrape_data('TW')  # Taiwan, China
scrape_data('CO')  # Colombia
scrape_data('BE')  # Belgium
scrape_data('CL')  # Chile
scrape_data('NO')  # Norway
scrape_data('FI')  # Finland
scrape_data('IL')  # Israel
scrape_data('MY')  # Malaysia
scrape_data('PK')  # Pakistan
scrape_data('LV')  # Latvia
scrape_data('HU')  # Hungary
scrape_data('IE')  # Ireland
scrape_data('NG')  # Nigeria
scrape_data('SI')  # Slovenia
scrape_data('GR')  # Greece
scrape_data('EC')  # Ecuador
scrape_data('SK')  # Slovakia
scrape_data('KE')  # Kenya
scrape_data('LT')  # Lithuania
scrape_data('IQ')  # Iraq
scrape_data('EE')  # Estonia
scrape_data('MD')  # Moldova, Republic of
scrape_data('RS')  # Serbia
scrape_data('VE')  # Venezuela, Bolivarian Republic of
scrape_data('KZ')  # Kazakhstan
scrape_data('NP')  # Nepal
scrape_data('SA')  # Saudi Arabia
scrape_data('LB')  # Lebanon
scrape_data('PE')  # Peru
scrape_data('HR')  # Croatia
scrape_data('CY')  # Cyprus
scrape_data('PA')  # Panama
scrape_data('MM')  # Myanmar
scrape_data('GE')  # Georgia
scrape_data('PT')  # Portugal
scrape_data('KH')  # Cambodia
scrape_data('DO')  # Dominican Republic
scrape_data('AE')  # United Arab Emirates
scrape_data('BY')  # Belarus
scrape_data('LU')  # Luxembourg
scrape_data('AM')  # Armenia
scrape_data('GH')  # Ghana
scrape_data('AL')  # Albania
scrape_data('TZ')  # Tanzania, United Republic of
scrape_data('CR')  # Costa Rica
scrape_data('EG')  # Egypt
scrape_data('HN')  # Honduras
scrape_data('PR')  # Puerto Rico
scrape_data('UZ')  # Uzbekistan
scrape_data('PY')  # Paraguay
scrape_data('SC')  # Seychelles
scrape_data('IS')  # Iceland
scrape_data('AZ')  # For Azerbaijan
scrape_data('KW')  # For Kuwait
scrape_data('GT')  # For Guatemala
scrape_data('AO')  # For Angola
scrape_data('MN')  # For Mongolia
scrape_data('AF')  # For Afghanistan
scrape_data('PS')  # For Palestine
scrape_data('UG')  # For Uganda
scrape_data('KG')  # For Kyrgyzstan
scrape_data('BO')  # For Bolivia, Plurinational State of
scrape_data('MK')  # For Macedonia, The Former Yugoslav Republic of
scrape_data('MU')  # For Mauritius
scrape_data('MT')  # For Malta
scrape_data('BA')  # For Bosnia and Herzegovina
scrape_data('CD')  # For Congo, The Democratic Republic of the
scrape_data('JO')  # For Jordan
scrape_data('SV')  # For El Salvador
scrape_data('BZ')  # For Belize
scrape_data('VG')  # For Virgin Islands, British
scrape_data('UY')  # For Uruguay
scrape_data('ZW')  # For Zimbabwe
scrape_data('LA')  # For Lao People's Democratic Republic
scrape_data('PG')  # For Papua New Guinea
scrape_data('CW')  # For Curaçao
scrape_data('MZ')  # For Mozambique
scrape_data('CM')  # For Cameroon
scrape_data('BW')  # For Botswana
scrape_data('RW')  # For Rwanda
scrape_data('NI')  # For Nicaragua
scrape_data('BT')  # For Bhutan
scrape_data('GI')  # For Gibraltar
scrape_data('TN')  # For Tunisia
scrape_data('MW')  # For Malawi
scrape_data('LY')  # For Libya
scrape_data('CI')  # For Côte d'Ivoire
scrape_data('BF')  # For Burkina Faso
scrape_data('ZM')  # For Zambia
scrape_data('TJ')  # For Tajikistan
scrape_data('BH')  # For Bahrain
scrape_data('LK')  # For Sri Lanka
scrape_data('ME')  # For Montenegro
scrape_data('MA')  # For Morocco
scrape_data('LI')  # For Liechtenstein
scrape_data('IM')  # For Isle of Man
scrape_data('SS')  # For South Sudan
scrape_data('SL')  # For Sierra Leone
scrape_data('SO')  # For Somalia
scrape_data('BM')  # For Bermuda
scrape_data('BJ')  # For Benin
scrape_data('QA')  # For Qatar
scrape_data('OM')  # For Oman
scrape_data('FJ')  # For Fiji
scrape_data('TD')  # For Chad
scrape_data('NC')  # For New Caledonia
scrape_data('NA')  # For Namibia
scrape_data('GN')  # For Guinea
scrape_data('GA')  # For Gabon
scrape_data('DZ')  # For Algeria
scrape_data('CG')  # For Congo
scrape_data('MV')  # For Maldives
scrape_data('SN')  # For Senegal
scrape_data('LR')  # For Liberia
scrape_data('TT')  # For Trinidad and Tobago
scrape_data('SZ')  # For Swaziland
scrape_data('MO')  # For Macao, China
scrape_data('HT')  # For Haiti
scrape_data('AG')  # For Antigua and Barbuda
scrape_data('VU')  # For Vanuatu
scrape_data('SD')  # For Sudan
scrape_data('JM')  # For Jamaica
scrape_data('BS')  # For Bahamas
scrape_data('VI')  # For Virgin Islands, U.S.
scrape_data('TL')  # For Timor-Leste
scrape_data('MG')  # For Madagascar
scrape_data('KY')  # For Cayman Islands
scrape_data('JE')  # For Jersey
scrape_data('GM')  # For Gambia
scrape_data('SM')  # For San Marino
scrape_data('SB')  # For Solomon Islands
scrape_data('BI')  # For Burundi
scrape_data('WS')  # For Samoa
scrape_data('ML')  # For Mali
scrape_data('LS')  # For Lesotho
scrape_data('GG')  # For Guernsey
scrape_data('CV')  # For Cape Verde
scrape_data('TG')  # For Togo
scrape_data('RE')  # For RÉUNION
scrape_data('NE')  # For Niger
scrape_data('GU')  # For Guam
scrape_data('GD')  # For Grenada
scrape_data('BN')  # For Brunei Darussalam
scrape_data('BB')  # For Barbados
scrape_data('MR')  # For Mauritania
scrape_data('KN')  # For Saint Kitts and Nevis
scrape_data('GP')  # For Guadeloupe
scrape_data('FO')  # For Faroe Islands
scrape_data('SR')  # For Suriname
scrape_data('GQ')  # For Equatorial Guinea
scrape_data('ET')  # For Ethiopia
scrape_data('DM')  # For Dominica
scrape_data('TM')  # For Turkmenistan
scrape_data('MF')  # For Saint Martin (French part)
scrape_data('LC')  # For Saint Lucia
scrape_data('GY')  # For Guyana
scrape_data('GF')  # For French Guiana
scrape_data('CU')  # For Cuba
scrape_data('YE')  # For Yemen
scrape_data('PF')  # For French Polynesia
scrape_data('MQ')  # For Martinique
scrape_data('MH')  # For Marshall Islands
scrape_data('FM')  # For Micronesia, Federated States of
scrape_data('DJ')  # For Djibouti
scrape_data('BQ')  # For Bonaire, Sint Eustatius and Saba
scrape_data('TO')  # For Tonga
scrape_data('SY')  # For Syrian Arab Republic
scrape_data('AW')  # For Aruba
scrape_data('AI')  # For Anguilla
scrape_data('VC')  # For Saint Vincent and the Grenadines
scrape_data('SX')  # For Sint Maarten (Dutch part)
scrape_data('PW')  # For Palau
scrape_data('NR')  # For Nauru
scrape_data('KI')  # For Kiribati
scrape_data('CF')  # For Central African Republic
scrape_data('BL')  # For Saint Barthélemy
scrape_data('VA')  # For Holy See (Vatican City State)
scrape_data('TV')  # For Tuvalu
scrape_data('TK')  # For Tokelau
scrape_data('MC')  # For Monaco
scrape_data('CK')  # For Cook Islands
scrape_data('AS')  # For American Samoa
scrape_data('AD')  # For Andorra
scrape_data('TC')  # For Turks and Caicos Islands
scrape_data('ST')  # For Sao Tome and Principe
scrape_data('NF')  # For Norfolk Island
scrape_data('MP')  # For Northern Mariana Islands
scrape_data('KM')  # For Comoros
scrape_data('GW')  # For Guinea-Bissau
scrape_data('FK')  # For Falkland Islands (Malvinas)
scrape_data('GL')  # For Greenland
# scrape_data('**')  # ***
# ... and more