# https://www.iso.org/obp/ui/#search
COUNTRIES = [
    {"code": "AF", "name": "Afghanistan", "continent": "AS"},
    {"code": "AL", "name": "Albania", "continent": "EU"},
    {"code": "DZ", "name": "Algeria", "continent": "AF"},
    {"code": "AS", "name": "American Samoa", "continent": "OC"},
    {"code": "AD", "name": "Andorra", "continent": "EU"},
    {"code": "AO", "name": "Angola", "continent": "AF"},
    {"code": "AI", "name": "Anguilla", "continent": "NA"},
    {"code": "AQ", "name": "Antarctica", "continent": "AN"},
    {"code": "AG", "name": "Antigua and Barbuda", "continent": "NA"},
    {"code": "AR", "name": "Argentina", "continent": "SA"},
    {"code": "AM", "name": "Armenia", "continent": "AS"},
    {"code": "AW", "name": "Aruba", "continent": "NA"},
    {"code": "AU", "name": "Australia", "continent": "OC"},
    {"code": "AT", "name": "Austria", "continent": "EU"},
    {"code": "AZ", "name": "Azerbaijan", "continent": "AS"},
    {"code": "BS", "name": "Bahamas", "continent": "NA"},
    {"code": "BH", "name": "Bahrain", "continent": "AS"},
    {"code": "BD", "name": "Bangladesh", "continent": "AS"},
    {"code": "BB", "name": "Barbados", "continent": "NA"},
    {"code": "BY", "name": "Belarus", "continent": "EU"},
    {"code": "BE", "name": "Belgium", "continent": "EU"},
    {"code": "BZ", "name": "Belize", "continent": "NA"},
    {"code": "BJ", "name": "Benin", "continent": "AF"},
    {"code": "BM", "name": "Bermuda", "continent": "NA"},
    {"code": "BT", "name": "Bhutan", "continent": "AS"},
    {"code": "BO", "name": "Bolivia, Plurinational State of", "continent": "SA"},
    {"code": "BQ", "name": "Bonaire, Sint Eustatius and Saba", "continent": "NA"},
    {"code": "BA", "name": "Bosnia and Herzegovina", "continent": "EU"},
    {"code": "BW", "name": "Botswana", "continent": "AF"},
    {"code": "BV", "name": "Bouvet Island", "continent": "AN"},
    {"code": "BR", "name": "Brazil", "continent": "SA"},
    {"code": "IO", "name": "British Indian Ocean Territory", "continent": "AS"},
    {"code": "BN", "name": "Brunei Darussalam", "continent": "AS"},
    {"code": "BG", "name": "Bulgaria", "continent": "EU"},
    {"code": "BF", "name": "Burkina Faso", "continent": "AF"},
    {"code": "BI", "name": "Burundi", "continent": "AF"},
    {"code": "CV", "name": "Cabo Verde", "continent": "AF"},
    {"code": "KH", "name": "Cambodia", "continent": "AS"},
    {"code": "CM", "name": "Cameroon", "continent": "AF"},
    {"code": "CA", "name": "Canada", "continent": "NA"},
    {"code": "KY", "name": "Cayman Islands", "continent": "NA"},
    {"code": "CF", "name": "Central African Republic", "continent": "AF"},
    {"code": "TD", "name": "Chad", "continent": "AF"},
    {"code": "CL", "name": "Chile", "continent": "SA"},
    {"code": "CN", "name": "China", "continent": "AS"},
    {"code": "CX", "name": "Christmas Island", "continent": "OC"},
    {"code": "CC", "name": "Cocos (Keeling) Islands", "continent": "AS"},
    {"code": "CO", "name": "Colombia", "continent": "SA"},
    {"code": "KM", "name": "Comoros", "continent": "AF"},
    {"code": "CG", "name": "Congo", "continent": "AF"},
    {"code": "CD", "name": "Congo, The Democratic Republic of the", "continent": "AF"},
    {"code": "CK", "name": "Cook Islands", "continent": "OC"},
    {"code": "CR", "name": "Costa Rica", "continent": "NA"},
    {"code": "HR", "name": "Croatia", "continent": "EU"},
    {"code": "CU", "name": "Cuba", "continent": "NA"},
    {"code": "CW", "name": "Cura\u00e7ao", "continent": "NA"},
    {"code": "CY", "name": "Cyprus", "continent": "EU"},
    {"code": "CZ", "name": "Czechia", "continent": "EU"},
    {"code": "CI", "name": "C\u00f4te d'Ivoire", "continent": "AF"},
    {"code": "DK", "name": "Denmark", "continent": "EU"},
    {"code": "DJ", "name": "Djibouti", "continent": "AF"},
    {"code": "DM", "name": "Dominica", "continent": "NA"},
    {"code": "DO", "name": "Dominican Republic", "continent": "NA"},
    {"code": "EC", "name": "Ecuador", "continent": "SA"},
    {"code": "EG", "name": "Egypt", "continent": "AF"},
    {"code": "SV", "name": "El Salvador", "continent": "NA"},
    {"code": "GQ", "name": "Equatorial Guinea", "continent": "AF"},
    {"code": "ER", "name": "Eritrea", "continent": "AF"},
    {"code": "EE", "name": "Estonia", "continent": "EU"},
    {"code": "SZ", "name": "Eswatini", "continent": "AF"},
    {"code": "ET", "name": "Ethiopia", "continent": "AF"},
    {"code": "FK", "name": "Falkland Islands (Malvinas)", "continent": "SA"},
    {"code": "FO", "name": "Faroe Islands", "continent": "EU"},
    {"code": "FJ", "name": "Fiji", "continent": "OC"},
    {"code": "FI", "name": "Finland", "continent": "EU"},
    {"code": "FR", "name": "France", "continent": "EU"},
    {"code": "GF", "name": "French Guiana", "continent": "SA"},
    {"code": "PF", "name": "French Polynesia", "continent": "OC"},
    {"code": "TF", "name": "French Southern Territories", "continent": "AN"},
    {"code": "GA", "name": "Gabon", "continent": "AF"},
    {"code": "GM", "name": "Gambia", "continent": "AF"},
    {"code": "GE", "name": "Georgia", "continent": "AS"},
    {"code": "DE", "name": "Germany", "continent": "EU"},
    {"code": "GH", "name": "Ghana", "continent": "AF"},
    {"code": "GI", "name": "Gibraltar", "continent": "EU"},
    {"code": "GR", "name": "Greece", "continent": "EU"},
    {"code": "GL", "name": "Greenland", "continent": "NA"},
    {"code": "GD", "name": "Grenada", "continent": "NA"},
    {"code": "GP", "name": "Guadeloupe", "continent": "NA"},
    {"code": "GU", "name": "Guam", "continent": "OC"},
    {"code": "GT", "name": "Guatemala", "continent": "NA"},
    {"code": "GG", "name": "Guernsey", "continent": "EU"},
    {"code": "GN", "name": "Guinea", "continent": "AF"},
    {"code": "GW", "name": "Guinea-Bissau", "continent": "AF"},
    {"code": "GY", "name": "Guyana", "continent": "SA"},
    {"code": "HT", "name": "Haiti", "continent": "NA"},
    {"code": "HM", "name": "Heard Island and McDonald Islands", "continent": "AN"},
    {"code": "VA", "name": "Holy See (Vatican City State)", "continent": "EU"},
    {"code": "HN", "name": "Honduras", "continent": "NA"},
    {"code": "HK", "name": "Hong Kong", "continent": "AS"},
    {"code": "HU", "name": "Hungary", "continent": "EU"},
    {"code": "IS", "name": "Iceland", "continent": "EU"},
    {"code": "IN", "name": "India", "continent": "AS"},
    {"code": "ID", "name": "Indonesia", "continent": "AS"},
    {"code": "IR", "name": "Iran, Islamic Republic of", "continent": "AS"},
    {"code": "IQ", "name": "Iraq", "continent": "AS"},
    {"code": "IE", "name": "Ireland", "continent": "EU"},
    {"code": "IM", "name": "Isle of Man", "continent": "EU"},
    {"code": "IL", "name": "Israel", "continent": "AS"},
    {"code": "IT", "name": "Italy", "continent": "EU"},
    {"code": "JM", "name": "Jamaica", "continent": "NA"},
    {"code": "JP", "name": "Japan", "continent": "AS"},
    {"code": "JE", "name": "Jersey", "continent": "EU"},
    {"code": "JO", "name": "Jordan", "continent": "AS"},
    {"code": "KZ", "name": "Kazakhstan", "continent": "AS"},
    {"code": "KE", "name": "Kenya", "continent": "AF"},
    {"code": "KI", "name": "Kiribati", "continent": "OC"},
    {"code": "KP", "name": "Korea, Democratic People's Republic of", "continent": "AS"},
    {"code": "KR", "name": "Korea, Republic of", "continent": "AS"},
    {"code": "KW", "name": "Kuwait", "continent": "AS"},
    {"code": "KG", "name": "Kyrgyzstan", "continent": "AS"},
    {"code": "LA", "name": "Lao People's Democratic Republic", "continent": "AS"},
    {"code": "LV", "name": "Latvia", "continent": "EU"},
    {"code": "LB", "name": "Lebanon", "continent": "AS"},
    {"code": "LS", "name": "Lesotho", "continent": "AF"},
    {"code": "LR", "name": "Liberia", "continent": "AF"},
    {"code": "LY", "name": "Libya", "continent": "AF"},
    {"code": "LI", "name": "Liechtenstein", "continent": "EU"},
    {"code": "LT", "name": "Lithuania", "continent": "EU"},
    {"code": "LU", "name": "Luxembourg", "continent": "EU"},
    {"code": "MO", "name": "Macao", "continent": "AS"},
    {"code": "MG", "name": "Madagascar", "continent": "AF"},
    {"code": "MW", "name": "Malawi", "continent": "AF"},
    {"code": "MY", "name": "Malaysia", "continent": "AS"},
    {"code": "MV", "name": "Maldives", "continent": "AS"},
    {"code": "ML", "name": "Mali", "continent": "AF"},
    {"code": "MT", "name": "Malta", "continent": "EU"},
    {"code": "MH", "name": "Marshall Islands", "continent": "OC"},
    {"code": "MQ", "name": "Martinique", "continent": "NA"},
    {"code": "MR", "name": "Mauritania", "continent": "AF"},
    {"code": "MU", "name": "Mauritius", "continent": "AF"},
    {"code": "YT", "name": "Mayotte", "continent": "AF"},
    {"code": "MX", "name": "Mexico", "continent": "NA"},
    {"code": "FM", "name": "Micronesia, Federated States of", "continent": "OC"},
    {"code": "MD", "name": "Moldova, Republic of", "continent": "EU"},
    {"code": "MC", "name": "Monaco", "continent": "EU"},
    {"code": "MN", "name": "Mongolia", "continent": "AS"},
    {"code": "ME", "name": "Montenegro", "continent": "EU"},
    {"code": "MS", "name": "Montserrat", "continent": "NA"},
    {"code": "MA", "name": "Morocco", "continent": "AF"},
    {"code": "MZ", "name": "Mozambique", "continent": "AF"},
    {"code": "MM", "name": "Myanmar", "continent": "AS"},
    {"code": "NA", "name": "Namibia", "continent": "AF"},
    {"code": "NR", "name": "Nauru", "continent": "OC"},
    {"code": "NP", "name": "Nepal", "continent": "AS"},
    {"code": "NL", "name": "Netherlands", "continent": "EU"},
    {"code": "NC", "name": "New Caledonia", "continent": "OC"},
    {"code": "NZ", "name": "New Zealand", "continent": "OC"},
    {"code": "NI", "name": "Nicaragua", "continent": "NA"},
    {"code": "NE", "name": "Niger", "continent": "AF"},
    {"code": "NG", "name": "Nigeria", "continent": "AF"},
    {"code": "NU", "name": "Niue", "continent": "OC"},
    {"code": "NF", "name": "Norfolk Island", "continent": "OC"},
    {"code": "MK", "name": "North Macedonia", "continent": "EU"},
    {"code": "MP", "name": "Northern Mariana Islands", "continent": "OC"},
    {"code": "NO", "name": "Norway", "continent": "EU"},
    {"code": "OM", "name": "Oman", "continent": "AS"},
    {"code": "PK", "name": "Pakistan", "continent": "AS"},
    {"code": "PW", "name": "Palau", "continent": "OC"},
    {"code": "PS", "name": "Palestine, State of", "continent": "AS"},
    {"code": "PA", "name": "Panama", "continent": "NA"},
    {"code": "PG", "name": "Papua New Guinea", "continent": "OC"},
    {"code": "PY", "name": "Paraguay", "continent": "SA"},
    {"code": "PE", "name": "Peru", "continent": "SA"},
    {"code": "PH", "name": "Philippines", "continent": "AS"},
    {"code": "PN", "name": "Pitcairn", "continent": "OC"},
    {"code": "PL", "name": "Poland", "continent": "EU"},
    {"code": "PT", "name": "Portugal", "continent": "EU"},
    {"code": "PR", "name": "Puerto Rico", "continent": "NA"},
    {"code": "QA", "name": "Qatar", "continent": "AS"},
    {"code": "RO", "name": "Romania", "continent": "EU"},
    {"code": "RU", "name": "Russian Federation", "continent": "EU"},
    {"code": "RW", "name": "Rwanda", "continent": "AF"},
    {"code": "RE", "name": "R\u00e9union", "continent": "AF"},
    {"code": "BL", "name": "Saint Barth\u00e9lemy", "continent": "NA"},
    {
        "code": "SH",
        "name": "Saint Helena, Ascension and Tristan da Cunha",
        "continent": "AF",
    },
    {"code": "KN", "name": "Saint Kitts and Nevis", "continent": "NA"},
    {"code": "LC", "name": "Saint Lucia", "continent": "NA"},
    {"code": "MF", "name": "Saint Martin (French part)", "continent": "NA"},
    {"code": "PM", "name": "Saint Pierre and Miquelon", "continent": "NA"},
    {"code": "VC", "name": "Saint Vincent and the Grenadines", "continent": "NA"},
    {"code": "WS", "name": "Samoa", "continent": "OC"},
    {"code": "SM", "name": "San Marino", "continent": "EU"},
    {"code": "ST", "name": "Sao Tome and Principe", "continent": "AF"},
    {"code": "SA", "name": "Saudi Arabia", "continent": "AS"},
    {"code": "SN", "name": "Senegal", "continent": "AF"},
    {"code": "RS", "name": "Serbia", "continent": "EU"},
    {"code": "SC", "name": "Seychelles", "continent": "AF"},
    {"code": "SL", "name": "Sierra Leone", "continent": "AF"},
    {"code": "SG", "name": "Singapore", "continent": "AS"},
    {"code": "SX", "name": "Sint Maarten (Dutch part)", "continent": "NA"},
    {"code": "SK", "name": "Slovakia", "continent": "EU"},
    {"code": "SI", "name": "Slovenia", "continent": "EU"},
    {"code": "SB", "name": "Solomon Islands", "continent": "OC"},
    {"code": "SO", "name": "Somalia", "continent": "AF"},
    {"code": "ZA", "name": "South Africa", "continent": "AF"},
    {
        "code": "GS",
        "name": "South Georgia and the South Sandwich Islands",
        "continent": "AN",
    },
    {"code": "SS", "name": "South Sudan", "continent": "AF"},
    {"code": "ES", "name": "Spain", "continent": "EU"},
    {"code": "LK", "name": "Sri Lanka", "continent": "AS"},
    {"code": "SD", "name": "Sudan", "continent": "AF"},
    {"code": "SR", "name": "Suriname", "continent": "SA"},
    {"code": "SJ", "name": "Svalbard and Jan Mayen", "continent": "EU"},
    {"code": "SE", "name": "Sweden", "continent": "EU"},
    {"code": "CH", "name": "Switzerland", "continent": "EU"},
    {"code": "SY", "name": "Syrian Arab Republic", "continent": "AS"},
    {"code": "TW", "name": "Taiwan, Province of China", "continent": "AS"},
    {"code": "TJ", "name": "Tajikistan", "continent": "AS"},
    {"code": "TZ", "name": "Tanzania, United Republic of", "continent": "AF"},
    {"code": "TH", "name": "Thailand", "continent": "AS"},
    {"code": "TL", "name": "Timor-Leste", "continent": "OC"},
    {"code": "TG", "name": "Togo", "continent": "AF"},
    {"code": "TK", "name": "Tokelau", "continent": "OC"},
    {"code": "TO", "name": "Tonga", "continent": "OC"},
    {"code": "TT", "name": "Trinidad and Tobago", "continent": "NA"},
    {"code": "TN", "name": "Tunisia", "continent": "AF"},
    {"code": "TM", "name": "Turkmenistan", "continent": "AS"},
    {"code": "TC", "name": "Turks and Caicos Islands", "continent": "NA"},
    {"code": "TV", "name": "Tuvalu", "continent": "OC"},
    {"code": "TR", "name": "T\u00fcrkiye", "continent": "AS"},
    {"code": "UG", "name": "Uganda", "continent": "AF"},
    {"code": "UA", "name": "Ukraine", "continent": "EU"},
    {"code": "AE", "name": "United Arab Emirates", "continent": "AS"},
    {"code": "GB", "name": "United Kingdom", "continent": "EU"},
    {"code": "US", "name": "United States", "continent": "NA"},
    {"code": "UM", "name": "United States Minor Outlying Islands", "continent": "OC"},
    {"code": "UY", "name": "Uruguay", "continent": "SA"},
    {"code": "UZ", "name": "Uzbekistan", "continent": "AS"},
    {"code": "VU", "name": "Vanuatu", "continent": "OC"},
    {"code": "VE", "name": "Venezuela, Bolivarian Republic of", "continent": "SA"},
    {"code": "VN", "name": "Viet Nam", "continent": "AS"},
    {"code": "VG", "name": "Virgin Islands, British", "continent": "NA"},
    {"code": "VI", "name": "Virgin Islands, U.S.", "continent": "NA"},
    {"code": "WF", "name": "Wallis and Futuna", "continent": "OC"},
    {"code": "EH", "name": "Western Sahara", "continent": "AF"},
    {"code": "YE", "name": "Yemen", "continent": "AS"},
    {"code": "ZM", "name": "Zambia", "continent": "AF"},
    {"code": "ZW", "name": "Zimbabwe", "continent": "AF"},
    {"code": "AX", "name": "\u00c5land Islands", "continent": "EU"},
]

CONTINENTS = [
    {"code": "AF", "name": "Africa"},
    {"code": "NA", "name": "North America"},
    {"code": "OC", "name": "Oceania"},
    {"code": "AN", "name": "Antarctica"},
    {"code": "AS", "name": "Asia"},
    {"code": "EU", "name": "Europe"},
    {"code": "SA", "name": "South America"},
]