import pycountry

codigos_paises = ['US', 'GB', 'ES', 'RU', 'IE', 'SE', 'CA', 'JP', 'CH', 'PL',
                  'KP', 'AU', 'TR', 'BG', 'CN', 'SI', 'PT', 'RO', 'DE', 'BR', 'SG',
                  'KZ', 'GR', 'FI', 'NL', 'IL', 'FR', 'KR', 'SA', 'IM', 'NO', 'BE',
                  'IT', 'DK', 'AS', 'TH', 'HK', 'HU', 'AT', 'LB', 'FO', 'LI', 'ID',
                  'AR', 'NZ', 'CZ', 'AD', 'RS', 'GS', 'PH', 'RW', 'TW', 'LT', 'AQ',
                  'NE', 'MQ', 'AE', 'QA', 'SK', 'CL', 'IS', 'UA', 'DZ', 'FJ', 'HM',
                  'ZA', 'MD', 'AO', 'VA', 'VE', 'VN', 'CX', 'MX', 'VI', 'UM', 'MO',
                  'LV', 'BY', 'IR', 'CD', 'PW', 'CC', 'CK', 'KN', 'PK', 'AL', 'IN',
                  'AZ', 'FK', 'SY', 'EE', 'MY', 'CR', 'SV', 'PS', 'CO', 'MC', 'IQ',
                  'CU', 'OM', 'BT', 'LK', 'MT', 'BA', 'TT', 'GE', 'JE', 'MA', 'HR',
                  'LC', 'TN', 'KG', 'BD', 'BH', 'BS', 'JM', 'AW', 'TO', 'PA', 'JO',
                  'TC', 'CY', 'DJ', 'BQ', 'SZ', 'CG', 'GM', 'CI', 'MH', 'TD', 'UG',
                  'ZW', 'HN', 'DO', 'TM', 'NC', 'CF', 'NG', 'GT', 'AF', 'FM', 'TF',
                  'EG', 'MV', 'BW', 'PM', 'VC', 'PE', 'MP', 'AM', 'NP', 'WF', 'XK',
                  'VG', 'BZ', 'LR', 'ET', 'ME', 'MN', 'KW', 'BF', 'SB', 'LY', 'SM',
                  'NU', 'CW', 'LU', 'GL', 'MG', 'PN', 'GG', 'AX', 'BB', 'BM', 'UY',
                  'SC', 'NF', 'YE', 'SO', 'EH', 'MK', 'SJ', 'PR', 'GP', 'NI', 'GI',
                  'FX', 'KY', 'GY', 'PG', 'UZ', 'TL', 'NR', 'ZM', 'VU', 'KI', 'BL',
                  'GN', 'TG', 'BI', 'GD', 'TV', 'IO', 'TJ', 'GA', 'LA', 'HT', 'KE',
                  'ER', 'CV', 'GU', 'GH', 'EC', 'BO', 'SD', 'SX', 'TZ', 'AG', 'BV',
                  'DM', 'PY', 'SH', 'TK', 'KH', 'SS', 'SL', 'CM', 'MZ', 'RE', 'GW',
                  'SR', 'WS', 'MM', 'BN', 'ST', 'BJ', 'AI', 'MU', 'YU', 'GQ', 'YT',
                  'KM', 'PF', 'SN', 'MR', 'ML', 'NA', 'GF', 'MS', 'MF', 'LS', 'MW']

codigos_validos = 0

for codigo in codigos_paises:
    try:
        info_pais = pycountry.countries.get(alpha_2=codigo)

        if info_pais:
            # print(f"Código {codigo} é válido: {info_pais.name}")
            codigos_validos += 1
        else:
            print(f"Código {codigo} não é válido.")
    except Exception as e:
        print(f"Erro ao verificar código {codigo}: {e}")

print(f"Códigos válidos: {codigos_validos} de {len(codigos_paises)}")

# Código XK não é válido.
# Código FX não é válido.
# Código YU não é válido.
# Códigos válidos: 249 de 252
