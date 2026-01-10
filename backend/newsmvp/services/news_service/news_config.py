rss_channels = [
    # "BBC",
    # "CNN",
    # "The New York Times",
    # "The Washington Post", # треба вибрати яку саме rss читати, бо у urls посилання на загальний сайт з rss
    "Ukrainian Pravda",
    "Economic Pravda",
    "UNIAN",
    "New Voice",
    "UkrInform",
]

rss_urls = {
    # "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    # "CNN": "http://rss.cnn.com/rss/edition.rss",
    # "The New York Times": "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/topic/destination/ukraine/rss.xml",
    # "The Washington Post": "https://www.washingtonpost.com/discussions/2018/10/12/washington-post-rss-feeds/",
    "Ukrainian Pravda": "https://www.pravda.com.ua/rss/",
    "Economic Pravda": "https://epravda.com.ua/rss/",
    "UNIAN": "https://rss.unian.net/site/news_ukr.rss",
    "New Voice": "https://nv.ua/ukr/rss/all.xml",
    "UkrInform": "https://www.ukrinform.ua/rss/block-lastnews",
}

news_verification = {
    -1: "fake",
    0: "not confirmed",
    1: "true",
}

types = [
    "unknown",
    "politics",
    "war",
    "economics",
    "medicine",
    "technology",
    "culture",
    "science",
    "education",
    "show business",
    "sport",
]

types_desc = {
    "unknown": "Загальні новини без конкретної категорії, різне",
    "politics": "Політика, державне управління, вибори, парламент, законопроєкти, уряд, партії, дипломатія, дебати, реформи, державні установи, зовнішня політика.",
    "war": "Війна, бойові дії, фронт, армія, збройні сили, оборона, обстріли, військова техніка, наступ, деокупація, стратегія, безпека, солдати.",
    "economics": "Економіка, фінанси, бізнес, ринок, інфляція, курс валют, ВВП, інвестиції, банки, податки, бюджет, торгівля, акції, промисловість.",
    "medicine": "Медицина, охорона здоров'я, лікарі, віруси, вакцинація, симптоми, лікування, фармацевтика, лікарні, хірургія, дослідження хвороб, здоров'я.",
    "technology": "Технології, ІТ, розробка, штучний інтелект, смартфони, гаджети, програмне забезпечення, цифровізація, стартапи, інтернет, кібербезпека.",
    "culture": "Культура, мистецтво, література, музеї, виставки, кіно, театр, архітектура, традиції, спадщина, історія, релігія, фестивалі.",
    "science": "Наука, дослідження, космос, фізика, біологія, археологія, винаходи, лабораторії, наукові відкриття, теорії, експерименти, гранти.",
    "education": "Освіта, навчання, НМТ, університети, школи, студенти, вчителі, курси, онлайн-освіта, атестація, дипломи, академічна сфера, саморозвиток.",
    "show business": "Шоу-бізнес, зірки, знаменитості, музика, концерти, премії, мода, світське життя, телебачення, стрімінг, популярність, інстаграм-блогери.",
    "sport": "Спорт, змагання, чемпіонат, турнір, матч, гра, рахунок, атлети, футболісти, тренування, олімпіада, кубок, ліга, стадіон, трансфер, збірна, призове місце, фізична культура, бокс, теніс, баскетбол.",
}

types_new = {}
