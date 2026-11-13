"""
Risk taxonomy for adverse-media screening, in English and Arabic.

Each category has
  weight : how serious the predicate offence is for an AML/sanctions program (0-100)
  en     : English regular expressions (matched case-insensitively on word boundaries)
  ar     : Arabic phrases (matched on normalised Arabic text, prefixes allowed)

Weights follow the usual financial-crime priority: terrorist financing and sanctions
breaches are the most serious (strict liability, criminal exposure), then money
laundering and organised crime, then bribery/corruption, then general fraud.
"""
from __future__ import annotations

CATEGORIES: dict[str, dict] = {
    "terrorism_financing": {
        "label": "Terrorism financing",
        "weight": 100,
        "en": [r"terror(ist|ism)? financ\w*", r"financ\w* (of )?terror\w*", r"terror(ist)? fund\w*",
               r"material support", r"terrorist organi[sz]ation", r"terror(ism|ist)\b",
               r"designated terrorist", r"jihadist"],
        "ar": ["تمويل الإرهاب", "تمويل الارهاب", "تمويل منظمات إرهابية", "منظمة إرهابية",
               "منظمة ارهابية", "الإرهاب", "الارهاب", "إرهابي", "ارهابي"],
    },
    "sanctions": {
        "label": "Sanctions / asset freeze",
        "weight": 90,
        "en": [r"sanction\w*", r"\bOFAC\b", r"\bSDN\b", r"blacklist\w*", r"asset freeze", r"frozen assets",
               r"assets? (were |was )?frozen", r"embargo\w*", r"export control\w*", r"sanctions? evasion",
               r"evad\w+ sanctions", r"designated by (the )?(US|U\.S\.|Treasury)", r"Treasury designat\w*",
               r"seiz\w* (of )?(his |her |its |their )?(assets|funds|property|properties)",
               r"(assets|funds|property) seiz\w*", r"confiscat\w*"],
        "ar": ["عقوبات", "العقوبات", "فرض عقوبات", "القائمة السوداء", "تجميد أصول", "تجميد الأصول",
               "تجميد أموال", "تجميد الأموال", "حظر", "الالتفاف على العقوبات", "التهرب من العقوبات",
               "وزارة الخزانة الأمريكية", "الخزانة الأمريكية", "حجز أموال", "حجز الأموال",
               "الحجز على أموال", "مصادرة أموال", "مصادرة الأموال", "مصادرة أملاك", "تجميد"],
    },
    "money_laundering": {
        "label": "Money laundering",
        "weight": 85,
        "en": [r"money[- ]launder\w*", r"launder\w*", r"\bAML\b (failure|violation|breach|lapse)\w*",
               r"anti-money laundering (failure|violation|breach|lapse|program)\w*", r"Bank Secrecy Act",
               r"\bBSA\b", r"illicit (funds|finance|financial flows|money)", r"dirty money",
               r"shell compan(y|ies)", r"structuring", r"proceeds of crime"],
        "ar": ["غسيل الأموال", "غسيل اموال", "غسل الأموال", "غسل اموال", "تبييض الأموال", "تبييض اموال",
               "تبييض", "أموال غير مشروعة", "اموال غير مشروعة", "شركات وهمية", "شركات واجهة",
               "عائدات الجريمة"],
    },
    "organized_crime": {
        "label": "Organised crime / trafficking",
        "weight": 80,
        "en": [r"organi[sz]ed crime", r"cartel\w*", r"\bmafia\b", r"drug trafficking", r"narcotics?",
               r"smuggl\w+", r"human trafficking", r"arms trafficking", r"weapons trafficking",
               r"racketeering", r"\bRICO\b", r"captagon", r"crime (syndicate|ring|boss)"],
        "ar": ["الجريمة المنظمة", "تهريب", "الاتجار بالمخدرات", "تجارة المخدرات", "مخدرات", "كبتاغون",
               "كبتاجون", "الاتجار بالبشر", "تهريب الأسلحة", "عصابة", "مافيا"],
    },
    "bribery_corruption": {
        "label": "Bribery / corruption",
        "weight": 75,
        "en": [r"brib\w+", r"kickback\w*", r"corrupt\w*", r"\bFCPA\b", r"\bgraft\b", r"cronyism",
               r"abuse of (power|office)", r"illicit enrichment", r"embezzl\w*", r"plunder\w*",
               r"stolen (state )?(assets|funds)", r"kleptocra\w*"],
        "ar": ["رشوة", "رشاوى", "رشى", "فساد", "الفساد", "الكسب غير المشروع", "استغلال النفوذ",
               "استغلال السلطة", "محسوبية", "نهب", "المال العام"],
    },
    "fraud": {
        "label": "Fraud",
        "weight": 70,
        "en": [r"fraud\w*", r"\bscam\w*", r"ponzi", r"misappropriat\w*", r"forg(ery|ed)",
               r"wire fraud", r"securities fraud", r"swindl\w*", r"false accounting", r"tax evasion",
               r"market manipulation", r"insider trading"],
        "ar": ["احتيال", "نصب", "اختلاس", "تزوير", "تلاعب", "غش", "تهرب ضريبي", "التهرب الضريبي"],
    },
}

# Legal / procedural stage of the story. A conviction weighs more than a rumour.
STAGES = {
    "conviction_or_penalty": {
        "label": "Conviction / penalty / designation",
        "multiplier": 1.00,
        "en": [r"convicted", r"sentenced", r"pleaded guilty", r"pleads guilty", r"plead guilty",
               r"found guilty", r"\bfined\b", r"\bfine of\b", r"penalt(y|ies)", r"settle(d|ment)",
               r"forfeit\w*", r"designat(ed|es|ion)", r"sanctioned", r"imposes? sanctions",
               r"jailed", r"prison", r"uph(e|o)ld\w*", r"sanctions? list"],
        "ar": ["أدين", "ادين", "إدانة", "ادانة", "حكم", "الحكم", "غرامة", "سجن", "السجن", "مصادرة",
               "فرض عقوبات", "فرضت عقوبات"],
    },
    "charged": {
        "label": "Charged / arrested / sued",
        "multiplier": 0.85,
        "en": [r"charged", r"indict\w*", r"arrest\w*", r"prosecut\w*", r"extradit\w*", r"\bsued\b",
               r"lawsuit", r"seiz(ed|ure)", r"raid\w*", r"detained"],
        "ar": ["اتهام", "متهم", "اعتقال", "القبض", "توقيف", "ملاحقة", "محاكمة", "دعوى", "مداهمة",
               "احتجاز"],
    },
    "allegation": {
        "label": "Allegation / investigation",
        "multiplier": 0.65,
        "en": [r"alleg\w*", r"accus\w*", r"investigat\w*", r"\bprobe\w*", r"suspect\w*", r"reportedly",
               r"leaked", r"claims?"],
        "ar": ["تحقيق", "مزاعم", "يشتبه", "اتهامات", "تسريب", "مسربة", "مسرّبة", "يزعم"],
    },
}

# Words suggesting the story is exculpatory (acquittal, delisting). Reduces severity
# but the article is kept: an analyst still needs to see it.
MITIGATING = {
    "en": [r"acquit\w*", r"cleared of", r"charges (were )?dropped", r"dismissed", r"delist\w*",
           r"sanctions (were )?lifted", r"lift\w* sanctions", r"pardon\w*", r"not guilty", r"overturn\w*",
           r"remov\w+ from (the )?(sanctions )?list"],
    "ar": ["تبرئة", "براءة", "رفع العقوبات", "إلغاء العقوبات", "شطب", "عفو", "إسقاط التهم"],
}

# Words that negate a mitigating phrase: "court REFUSES to lift sanctions" is adverse,
# not exculpatory.
NEGATORS = {
    "en": [r"refus\w*", r"reject\w*", r"uph(e|o)ld\w*", r"den(y|ies|ied)\b", r"\bloses?\b", r"\blost\b",
           r"fail\w* to", r"\bkeeps?\b", r"\bremains?\b", r"\bnot\b", r"\bno\b"],
    "ar": ["رفض", "ترفض", "يرفض", "تخسر", "يخسر", "خسر", "إبقاء", "ابقاء", "تبقي", "يبقي", "لا ", "لن "],
}

# Short English risk terms used to build the boolean search string sent to the news sources.
SEARCH_TERMS_EN = ["sanctions", "laundering", "fraud", "bribery", "corruption", "terrorism",
                   "smuggling", "indicted", "convicted", "trafficking"]
SEARCH_TERMS_AR = ["عقوبات", "غسيل", "فساد", "رشوة", "احتيال", "إرهاب", "تهريب", "اتهام"]
