from products.models import Product, Category, Brand

# Получаем категории и бренды
smartphones = Category.objects.get(slug='smartfony')
laptops = Category.objects.get(slug='noutbuki')
monitors = Category.objects.get(slug='monitory')
keyboards = Category.objects.get(slug='klaviatura')
mouse = Category.objects.get(slug='mysh')
headphones = Category.objects.get(slug='naushniki')
speakers = Category.objects.get(slug='kolonki')
tv = Category.objects.get(slug='televizor')
cameras = Category.objects.get(slug='fotoapparaty')
smartwatch = Category.objects.get(slug='smartchasy')
console = Category.objects.get(slug='igrovaya-konsol')

apple = Brand.objects.get(name='Apple')
samsung = Brand.objects.get(name='Samsung')
sony = Brand.objects.get(name='Sony')
lg = Brand.objects.get(name='LG')
dell = Brand.objects.get(name='Dell')
asus = Brand.objects.get(name='Asus')
logitech = Brand.objects.get(name='Logitech')
razer = Brand.objects.get(name='Razer')
canon = Brand.objects.get(name='Canon')
nikon = Brand.objects.get(name='Nikon')
xiaomi = Brand.objects.get(name='Xiaomi')
huawei = Brand.objects.get(name='Huawei')

products = []

# === СМАРТФОНЫ ===
products.append(Product(
    name='Samsung Galaxy S24 Ultra',
    price=129990,
    description='Флагманский смартфон Samsung с 6.8" Dynamic AMOLED дисплеем, процессором Snapdragon 8 Gen 3, камерой 200 МП и поддержкой S Pen. Корпус из титана, водозащита IP68, батарея 5000 мАч с быстрой зарядкой 45 Вт.',
    amount=45,
    category=smartphones,
    brand=samsung
))

products.append(Product(
    name='Xiaomi 14 Pro',
    price=89990,
    description='Премиальный смартфон с процессором Snapdragon 8 Gen 3, камерой Leica с тремя объективами 50 МП, 6.73" AMOLED дисплеем 120 Гц и быстрой зарядкой 120 Вт. 12 ГБ оперативной памяти и 512 ГБ встроенной.',
    amount=62,
    category=smartphones,
    brand=xiaomi
))

products.append(Product(
    name='Apple iPhone 15 Pro',
    price=119990,
    description='iPhone с титановым корпусом, процессором A17 Pro, тройной камерой с 48 МП основным модулем и 5-кратным оптическим зумом. Поддержка USB-C, Dynamic Island, всегда активный дисплей Super Retina XDR 6.1".',
    amount=38,
    category=smartphones,
    brand=apple
))

# === НОУТБУКИ ===
products.append(Product(
    name='ASUS ROG Strix G16',
    price=159990,
    description='Игровой ноутбук с процессором Intel Core i9-14900HX, видеокартой NVIDIA RTX 4070 8GB, 16" QHD дисплеем 240 Гц, 32 ГБ DDR5 RAM и SSD 1 ТБ. RGB подсветка клавиатуры, система охлаждения ROG Intelligent Cooling.',
    amount=18,
    category=laptops,
    brand=asus
))

products.append(Product(
    name='Dell XPS 15',
    price=189990,
    description='Премиальный ноутбук для работы и творчества. Intel Core i7-13700H, NVIDIA RTX 4050 6GB, 15.6" OLED 3.5K дисплей, 16 ГБ RAM, 512 ГБ SSD. Алюминиевый корпус, вес 1.86 кг, время работы до 13 часов.',
    amount=24,
    category=laptops,
    brand=dell
))

products.append(Product(
    name='Apple MacBook Air M3',
    price=139990,
    description='Ультратонкий ноутбук на чипе Apple M3 с 8-ядерным CPU и 10-ядерным GPU. Liquid Retina дисплей 13.6", до 18 часов автономной работы, бесшумная работа без вентилятора, 8 ГБ объединенной памяти, SSD 256 ГБ.',
    amount=41,
    category=laptops,
    brand=apple
))

# === МОНИТОРЫ ===
products.append(Product(
    name='Samsung Odyssey G7',
    price=54990,
    description='Изогнутый игровой монитор 32" с разрешением QHD 2560x1440, частотой обновления 240 Гц, временем отклика 1 мс. Поддержка NVIDIA G-Sync и AMD FreeSync Premium Pro, HDR600, 1000R кривизна экрана.',
    amount=15,
    category=monitors,
    brand=samsung
))

products.append(Product(
    name='LG UltraGear 27GN950',
    price=69990,
    description='Профессиональный игровой монитор 27" 4K UHD IPS с частотой 144 Гц, HDR600, покрытием 98% DCI-P3. Nano IPS технология для точной цветопередачи, NVIDIA G-Sync Compatible, USB-C с подачей питания 60 Вт.',
    amount=22,
    category=monitors,
    brand=lg
))

products.append(Product(
    name='Dell UltraSharp U2723DE',
    price=49990,
    description='Профессиональный монитор для работы 27" QHD IPS с разрешением 2560x1440, покрытием цветового пространства 95% DCI-P3, USB-C хаб с подачей питания 90 Вт, встроенные динамики, регулировка по высоте и поворот.',
    amount=28,
    category=monitors,
    brand=dell
))

# === КЛАВИАТУРЫ ===
products.append(Product(
    name='Logitech MX Keys',
    price=12990,
    description='Беспроводная клавиатура премиум-класса с подсветкой клавиш, адаптирующейся к освещению. Низкопрофильные клавиши Perfect Stroke для комфортной печати, подключение до 3 устройств, USB-C зарядка, время работы до 10 дней с подсветкой.',
    amount=56,
    category=keyboards,
    brand=logitech
))

products.append(Product(
    name='Razer BlackWidow V4 Pro',
    price=24990,
    description='Механическая игровая клавиатура с переключателями Razer Green, RGB подсветкой Chroma, программируемыми макро-клавишами, магнитной подставкой для рук, колесом прокрутки и медиа-клавишами. Проводное подключение USB-C.',
    amount=34,
    category=keyboards,
    brand=razer
))

products.append(Product(
    name='Logitech G915 TKL',
    price=18990,
    description='Беспроводная механическая игровая клавиатура формата TKL с низкопрофильными переключателями GL Tactile, RGB подсветкой LIGHTSYNC, подключением через Bluetooth или USB-ресивер. Время работы до 40 часов, алюминиевый корпус.',
    amount=29,
    category=keyboards,
    brand=logitech
))

# === МЫШИ ===
products.append(Product(
    name='Logitech MX Master 3S',
    price=10990,
    description='Эргономичная беспроводная мышь для продуктивности с сенсором 8000 DPI, бесшумными кликами, колесом MagSpeed для быстрой прокрутки, 7 программируемыми кнопками, USB-C зарядкой и поддержкой работы до 70 дней на одном заряде.',
    amount=67,
    category=mouse,
    brand=logitech
))

products.append(Product(
    name='Razer DeathAdder V3 Pro',
    price=14990,
    description='Беспроводная игровая мышь с сенсором Focus Pro 30K DPI, оптическими переключателями Gen-3 на 90 млн кликов, весом 63 грамма, временем работы до 90 часов, поддержкой беспроводной зарядки HyperSpeed Wireless.',
    amount=48,
    category=mouse,
    brand=razer
))

products.append(Product(
    name='Logitech G502 HERO',
    price=7990,
    description='Проводная игровая мышь с сенсором HERO 25K, 11 программируемыми кнопками, системой настройки веса, RGB подсветкой LIGHTSYNC. Механический переключатель натяжения колеса прокрутки, эргономичная форма для правой руки.',
    amount=89,
    category=mouse,
    brand=logitech
))

# === НАУШНИКИ ===
products.append(Product(
    name='Sony WH-1000XM5',
    price=34990,
    description='Беспроводные наушники с лучшей в классе активной шумоподавлением, 8 микрофонами для четких звонков, временем работы до 30 часов, быстрой зарядкой USB-C, поддержкой Hi-Res Audio и LDAC, адаптивным звуком.',
    amount=52,
    category=headphones,
    brand=sony
))

products.append(Product(
    name='Apple AirPods Max',
    price=64990,
    description='Полноразмерные беспроводные наушники с активным шумоподавлением, пространственным звуком с динамическим отслеживанием головы, чипом Apple H1, алюминиевыми чашками, тканевой оголовьем, временем работы до 20 часов.',
    amount=31,
    category=headphones,
    brand=apple
))

products.append(Product(
    name='Razer BlackShark V2 Pro',
    price=19990,
    description='Беспроводная игровая гарнитура с технологией THX Spatial Audio для 7.1 объемного звука, 50-мм драйверами Razer TriForce Titanium, съемным микрофоном HyperClear, временем работы до 24 часов, весом 320 грамм.',
    amount=43,
    category=headphones,
    brand=razer
))

# === КОЛОНКИ ===
products.append(Product(
    name='Logitech Z906',
    price=29990,
    description='Акустическая система 5.1 мощностью 500 Вт с поддержкой Dolby Digital и DTS, сабвуфером 165 Вт, пультом управления. Подключение через оптический, коаксиальный вход, 6-канальный прямой и RCA. Сертификация THX для кинотеатрального звука.',
    amount=19,
    category=speakers,
    brand=logitech
))

products.append(Product(
    name='Sony SRS-XB43',
    price=24990,
    description='Портативная Bluetooth колонка с мощным басом EXTRA BASS, LED подсветкой, водозащитой IP67, временем работы до 24 часов, функцией Party Connect для связи до 100 колонок, USB-зарядкой устройств, голосовым управлением.',
    amount=36,
    category=speakers,
    brand=sony
))

products.append(Product(
    name='Razer Nommo Chroma',
    price=16990,
    description='Игровая акустическая система 2.0 с RGB подсветкой Chroma, автоматической регулировкой уровня звука, 3-дюймовыми драйверами и портами для наушников. Басовая регулировка, мощность 30 Вт, USB и AUX подключение.',
    amount=27,
    category=speakers,
    brand=razer
))

# === ТЕЛЕВИЗОРЫ ===
products.append(Product(
    name='Samsung QN95C Neo QLED 65"',
    price=249990,
    description='Премиальный 4K телевизор с технологией Quantum Mini LED, процессором Neural Quantum 4K, частотой 120 Гц для игр, Quantum HDR 2000, объемным звуком Dolby Atmos, One Connect Box, тонкий дизайн Infinity Screen.',
    amount=12,
    category=tv,
    brand=samsung
))

products.append(Product(
    name='LG OLED C3 55"',
    price=159990,
    description='OLED телевизор 4K с процессором α9 Gen6 AI, идеальным черным цветом, временем отклика 0.1 мс для геймеров, поддержкой HDMI 2.1, VRR, ALLM, Dolby Vision IQ, Dolby Atmos, webOS 23, Magic Remote в комплекте.',
    amount=18,
    category=tv,
    brand=lg
))

products.append(Product(
    name='Sony Bravia XR A80L 65"',
    price=199990,
    description='OLED телевизор с когнитивным процессором XR, технологией Acoustic Surface Audio+ для звука из экрана, поддержкой HDMI 2.1 для PS5, Dolby Vision, Google TV, голосовым управлением Алиса и Google Assistant.',
    amount=15,
    category=tv,
    brand=sony
))

# === ФОТОАППАРАТЫ ===
products.append(Product(
    name='Canon EOS R6 Mark II',
    price=279990,
    description='Полнокадровая беззеркальная камера 24.2 МП с процессором DIGIC X, видео 6K RAW, стабилизацией IBIS на 8 ступеней, автофокусом Dual Pixel II с распознаванием людей, животных и транспорта, съемкой до 40 fps, 4K 60p.',
    amount=8,
    category=cameras,
    brand=canon
))

products.append(Product(
    name='Nikon Z8',
    price=449990,
    description='Гибридная профессиональная камера 45.7 МП с процессором EXPEED 7, видео 8K 60p RAW, стабилизацией на 6 ступеней, 493-точечным автофокусом с AI, съемкой 20 fps RAW, защитой от влаги и пыли, двумя слотами CFexpress.',
    amount=6,
    category=cameras,
    brand=nikon
))

products.append(Product(
    name='Sony Alpha 7 IV',
    price=299990,
    description='Универсальная полнокадровая камера 33 МП с процессором BIONZ XR, видео 4K 60p 10-bit, стабилизацией на 5.5 ступеней, 759-точечным фазовым автофокусом с Eye AF для людей и животных, съемкой 10 fps, поворотным экраном.',
    amount=11,
    category=cameras,
    brand=sony
))

# === СМАРТ-ЧАСЫ ===
products.append(Product(
    name='Apple Watch Series 9',
    price=44990,
    description='Умные часы с чипом S9, всегда активным Retina дисплеем, датчиками здоровья (ЭКГ, SpO2, температура), отслеживанием активности и сна, водозащитой WR50, быстрой зарядкой USB-C, watchOS 10, управление двойным касанием.',
    amount=58,
    category=smartwatch,
    brand=apple
))

products.append(Product(
    name='Samsung Galaxy Watch6 Classic',
    price=34990,
    description='Смарт-часы премиум-класса с вращающейся лункой, AMOLED дисплеем, датчиками здоровья Samsung BioActive (ЭКГ, давление, состав тела), GPS, NFC для Samsung Pay, Wear OS, время работы до 40 часов, водозащита IP68.',
    amount=42,
    category=smartwatch,
    brand=samsung
))

products.append(Product(
    name='Huawei Watch GT 4',
    price=24990,
    description='Элегантные смарт-часы с AMOLED дисплеем, временем работы до 14 дней, более 100 спортивными режимами, мониторингом здоровья 24/7, GPS, Bluetooth звонками, водозащитой 5 ATM, сменными ремешками, HarmonyOS.',
    amount=51,
    category=smartwatch,
    brand=huawei
))

# === ИГРОВЫЕ КОНСОЛИ ===
products.append(Product(
    name='Sony PlayStation 5 Slim',
    price=54990,
    description='Игровая консоль нового поколения с SSD 1 ТБ, поддержкой 4K 120 fps, ray tracing, 3D звуком Tempest, DualSense контроллером с тактильной отдачей и адаптивными триггерами, эксклюзивными играми PlayStation Studios.',
    amount=32,
    category=console,
    brand=sony
))

products.append(Product(
    name='Sony PlayStation 5 Digital Edition',
    price=44990,
    description='Цифровая версия PS5 без дисковода для игр. Полная мощность PlayStation 5 с SSD 825 ГБ, поддержкой 4K HDR, ray tracing, 3D Audio, контроллером DualSense, доступом к PlayStation Plus и цифровому магазину PlayStation Store.',
    amount=28,
    category=console,
    brand=sony
))

products.append(Product(
    name='Sony PlayStation 5 Pro',
    price=74990,
    description='Усовершенствованная версия PS5 с улучшенным GPU для 4K 60fps с ray tracing, SSD 2 ТБ, поддержкой PlayStation VR2, технологией AMD FSR для апскейлинга, улучшенной системой охлаждения, DualSense Edge контроллером в комплекте.',
    amount=15,
    category=console,
    brand=sony
))

print(f"Создаю {len(products)} товаров...")
for product in products:
    product.save()
    print(f"✓ {product.name}")

print(f"\nГотово! Создано {len(products)} товаров.")
