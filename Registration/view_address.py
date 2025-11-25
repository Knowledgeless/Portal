# app_name/api_views.py (or just put these functions in views.py)

from django.http import JsonResponse
# Replace this import with your actual source for geographical data
# e.g., from .data_loader import get_all_divisions, get_districts_by_division, get_upazilas_by_district

# --- PLACEHOLDER DATA (Replace with your database/JSON/utility functions) ---
# Assuming you have a list of all divisions available
DIVISION_LIST = ["Dhaka", "Chattogram", "Khulna", "Rajshahi", "Sylhet", "Barishal", "Rangpur", "Mymensingh"] 
# Assuming you have a data structure to look up districts/upazilas
GEOGRAPHY_DATA = {
  "Dhaka": {
    "Dhaka": [
      "Dhamrai",
      "Dohar",
      "Keraniganj",
      "Nawabganj",
      "Savar",
      "Dhaka Matropoliton"
    ],
    "Faridpur": [
      "Alfadanga",
      "Bhanga",
      "Boalmari",
      "Charbhadrasan",
      "Faridpur Sadar",
      "Madhukhali",
      "Nagarkanda",
      "Sadarpur",
      "Saltha"
    ],
    "Gazipur": [
      "Gazipur Sadar",
      "Kaliakair",
      "Kaliganj",
      "Kapasia",
      "Sreepur"
    ],
    "Gopalganj": [
      "Gopalganj Sadar",
      "Kashiani",
      "Kotalipara",
      "Muksudpur",
      "Tungipara"
    ],
    "Kishoreganj": [
      "Austagram",
      "Bajitpur",
      "Bhairab",
      "Hossainpur",
      "Itna",
      "Karimganj",
      "Katiadi",
      "Kishoreganj Sadar",
      "Kuliarchar",
      "Mithamain",
      "Nikli",
      "Pakundia",
      "Tarail"
    ],
    "Madaripur": [
      "Kalkini",
      "Madaripur Sadar",
      "Rajoir",
      "Shibchar"
    ],
    "Manikganj": [
      "Daulatpur",
      "Ghior",
      "Harirampur",
      "Manikganj Sadar",
      "Saturia",
      "Shibalaya",
      "Singair"
    ],
    "Munshiganj": [
      "Gazaria",
      "Lohajang",
      "Munshiganj Sadar",
      "Sirajdikhan",
      "Sreenagar",
      "Tongibari"
    ],
    "Narayanganj": [
      "Araihazar",
      "Bandar",
      "Narayanganj Sadar",
      "Rupganj",
      "Sonargaon"
    ],
    "Narsingdi": [
      "Belabo",
      "Manohardi",
      "Narsingdi Sadar",
      "Palash",
      "Raipura",
      "Shibpur"
    ],
    "Rajbari": [
      "Baliakandi",
      "Goalandaghat",
      "Pangsha",
      "Rajbari Sadar"
    ],
    "Shariatpur": [
      "Bhedarganj",
      "Damudya",
      "Gosairhat",
      "Jajira",
      "Naria",
      "Shariatpur Sadar"
    ],
    "Tangail": [
      "Basail",
      "Bhuapur",
      "Delduar",
      "Ghatail",
      "Gopalpur",
      "Kalihati",
      "Madhupur",
      "Mirzapur",
      "Nagarpur",
      "Shakhipur",
      "Tangail Sadar"
    ]
  },
  "Chattogram": {
    "Bandarban": [
      "Alikadam",
      "Bandarban Sadar",
      "Lama",
      "Naikhongchhari",
      "Rowangchhari",
      "Ruma",
      "Thanchi"
    ],
    "Brahmanbaria": [
      "Akhaura",
      "Banchharampur",
      "Ashuganj",
      "Brahmanbaria Sadar",
      "Kasba",
      "Nabinagar",
      "Nasirnagar",
      "Sarail",
      "Bijoynagar"
    ],
    "Chandpur": [
      "Chandpur Sadar",
      "Hajiganj",
      "Kachua",
      "Matlab Dakshin",
      "Matlab Uttar",
      "Shahrasti",
      "Haimchar",
      "Faridganj"
    ],
    "Chattogram": [
      "Anwara",
      "Banskhali",
      "Boalkhali",
      "Chandanaish",
      "Fatikchhari",
      "Hathazari",
      "Lohagara",
      "Mirsharai",
      "Patiya",
      "Rangunia",
      "Raozan",
      "Sandwip",
      "Satkania",
      "Sitakunda",
      "Karnafuli"
    ],
    "Cox's Bazar": [
      "Chakaria",
      "Cox's Bazar Sadar",
      "Kutubdia",
      "Maheshkhali",
      "Pekua",
      "Ramu",
      "Teknaf",
      "Ukhia",
      "Moheskhali"
    ],
    "Cumilla": [
      "Barura",
      "Brahmanpara",
      "Burichong",
      "Chandina",
      "Chauddagram",
      "Daudkandi",
      "Debidwar",
      "Homna",
      "Laksam",
      "Lalmai",
      "Meghna",
      "Muradnagar",
      "Nangalkot",
      "Titas",
      "Cumilla Sadar",
      "Cumilla Sadar Dakshin"
    ],
    "Feni": [
      "Chhagalnaiya",
      "Daganbhuiyan",
      "Feni Sadar",
      "Parshuram",
      "Sonagazi",
      "Fulgazi"
    ],
    "Khagrachhari": [
      "Dighinala",
      "Khagrachhari Sadar",
      "Lakshmichhari",
      "Mahalchhari",
      "Manikchhari",
      "Matiranga",
      "Panchhari",
      "Ramgarh"
    ],
    "Lakshmipur": [
      "Lakshmipur Sadar",
      "Ramganj",
      "Ramgati",
      "Raipur",
      "Komolnagar"
    ],
    "Noakhali": [
      "Begumganj",
      "Chatkhil",
      "Companiganj",
      "Hatiya",
      "Noakhali Sadar",
      "Senbagh",
      "Sonaimuri",
      "Subarnachar",
      "Kabirhat"
    ],
    "Rangamati": [
      "Bagaichhari",
      "Barkal",
      "Belaichhari",
      "Juraichhari",
      "Kaptai",
      "Kaukhali",
      "Langadu",
      "Naniarchar",
      "Rajasthali",
      "Rangamati Sadar"
    ]
  },
  "Khulna": {
    "Bagerhat": [
      "Bagerhat Sadar",
      "Chitalmari",
      "Fakirhat",
      "Kachua",
      "Mollahat",
      "Mongla",
      "Rampal",
      "Sarankhola",
      "Morrelganj"
    ],
    "Chuadanga": [
      "Alamdanga",
      "Chuadanga Sadar",
      "Damurhuda",
      "Jibannagar"
    ],
    "Jashore": [
      "Abhaynagar",
      "Bagherpara",
      "Chaugachha",
      "Jashore Sadar",
      "Jhikargachha",
      "Keshabpur",
      "Manirampur",
      "Sharsha"
    ],
    "Jhenaidah": [
      "Harinakunda",
      "Jhenaidah Sadar",
      "Kaliganj",
      "Kotchandpur",
      "Moheshpur",
      "Shailkupa"
    ],
    "Khulna": [
      "Batiaghata",
      "Dacope",
      "Dumuria",
      "Dighalia",
      "Koyra",
      "Khalishpur",
      "Khan Jahan Ali",
      "Khulna Sadar",
      "Paikgachha",
      "Phultala",
      "Rupsa",
      "Terokhada",
      "Sonadanga"
    ],
    "Kushtia": [
      "Bheramara",
      "Daulatpur",
      "Khoksa",
      "Kumarkhali",
      "Kushtia Sadar",
      "Mirpur"
    ],
    "Magura": [
      "Magura Sadar",
      "Mohammadpur",
      "Shalikha",
      "Sreepur"
    ],
    "Meherpur": [
      "Gangni",
      "Meherpur Sadar",
      "Mujibnagar"
    ],
    "Narail": [
      "Kalia",
      "Lohagara",
      "Narail Sadar"
    ],
    "Satkhira": [
      "Assasuni",
      "Debhata",
      "Kalaroa",
      "Kaliganj",
      "Satkhira Sadar",
      "Shyamnagar",
      "Tala"
    ]
  },
  "Rajshahi": {
    "Bogura": [
      "Adamdighi",
      "Bogura Sadar",
      "Dhunat",
      "Dhupchanchia",
      "Gabtali",
      "Kahaloo",
      "Nandigram",
      "Sariakandi",
      "Shajahanpur",
      "Sherpur",
      "Shibganj",
      "Sonatala"
    ],
    "Joypurhat": [
      "Akkelpur",
      "Joypurhat Sadar",
      "Kalai",
      "Khetlal",
      "Panchbibi"
    ],
    "Naogaon": [
      "Atrai",
      "Badalgachhi",
      "Dhamoirhat",
      "Manda",
      "Naogaon Sadar",
      "Niamatpur",
      "Patnitala",
      "Porsha",
      "Raninagar",
      "Sapahar"
    ],
    "Natore": [
      "Baraigram",
      "Bagatipara",
      "Lalpur",
      "Natore Sadar",
      "Singra",
      "Gurudaspur",
      "Naldanga"
    ],
    "Pabna": [
      "Atgharia",
      "Bera",
      "Bhangura",
      "Chatmohar",
      "Faridpur",
      "Ishwardi",
      "Pabna Sadar",
      "Santhia",
      "Sujanagar"
    ],
    "Rajshahi": [
      "Bagha",
      "Bagmara",
      "Charghat",
      "Durgapur",
      "Godagari",
      "Mohanpur",
      "Paba",
      "Putia",
      "Tanore"
    ],
    "Sirajganj": [
      "Belkuchi",
      "Chauhali",
      "Kamarkhanda",
      "Kazipur",
      "Raiganj",
      "Shahjadpur",
      "Sirajganj Sadar",
      "Tarash",
      "Ullahpara"
    ]
  },
  "Rangpur": {
    "Dinajpur": [
      "Birampur",
      "Birganj",
      "Biral",
      "Bochaganj",
      "Chirirbandar",
      "Phulbari",
      "Ghoraghat",
      "Hakimpur",
      "Kaharole",
      "Khansama",
      "Dinajpur Sadar",
      "Nawabganj",
      "Parbatipur"
    ],
    "Gaibandha": [
      "Phulchhari",
      "Gaibandha Sadar",
      "Gobindaganj",
      "Palashbari",
      "Sadullapur",
      "Saghata",
      "Sundarganj"
    ],
    "Kurigram": [
      "Bhurungamari",
      "Chilmari",
      "Phulbari",
      "Rajarhat",
      "Rou mari",
      "Kurigram Sadar",
      "Nageshwari",
      "Ulipur",
      "Char Rajibpur"
    ],
    "Lalmonirhat": [
      "Aditmari",
      "Kaliganj",
      "Hatibandha",
      "Lalmonirhat Sadar",
      "Patgram"
    ],
    "Nilphamari": [
      "Dimla",
      "Domar",
      "Jaldhaka",
      "Kishorganj",
      "Nilphamari Sadar",
      "Saidpur"
    ],
    "Panchagarh": [
      "Atwari",
      "Boda",
      "Debiganj",
      "Panchagarh Sadar",
      "Tetulia"
    ],
    "Rangpur": [
      "Badarganj",
      "Gangachara",
      "Kaunia",
      "Rangpur Sadar",
      "Mithapukur",
      "Pirgachha",
      "Pirganj",
      "Taraganj"
    ],
    "Thakurgaon": [
      "Baliadangi",
      "Haripur",
      "Pirganj",
      "Ranisankail",
      "Thakurgaon Sadar"
    ]
  },
  "Barishal": {
    "Barguna": [
      "Amtali",
      "Barguna Sadar",
      "Betagi",
      "Bamna",
      "Patharghata",
      "Taltali"
    ],
    "Barishal": [
      "Agailjhara",
      "Babuganj",
      "Bakerganj",
      "Banaripara",
      "Gaurnadi",
      "Hizla",
      "Barishal Sadar",
      "Mehendiganj",
      "Muladi",
      "Uzirpur"
    ],
    "Bhola": [
      "Bhola Sadar",
      "Borhanuddin",
      "Char Fasson",
      "Daulatkhan",
      "Lalmohan",
      "Manpura",
      "Tazumuddin"
    ],
    "Jhalokati": [
      "Jhalokati Sadar",
      "Kathalia",
      "Nalchity",
      "Rajapur"
    ],
    "Patuakhali": [
      "Baufal",
      "Dashmina",
      "Galachipa",
      "Kalapara",
      "Mirzaganj",
      "Patuakhali Sadar",
      "Dumki",
      "Rangabali"
    ],
    "Pirojpur": [
      "Bhandaria",
      "Kawkhali",
      "Mathbaria",
      "Nezamabad",
      "Pirojpur Sadar",
      "Sadar",
      "Zianagar",
      "Indurkani"
    ]
  },
  "Sylhet": {
    "Habiganj": [
      "Ajmiriganj",
      "Baniachang",
      "Bahubal",
      "Chunarughat",
      "Habiganj Sadar",
      "Lakhai",
      "Madhabpur",
      "Nabiganj",
      "Shaistaganj"
    ],
    "Moulvibazar": [
      "Barlekha",
      "Juri",
      "Kamalganj",
      "Kulaura",
      "Moulvibazar Sadar",
      "Rajnagar",
      "Sreemangal"
    ],
    "Sunamganj": [
      "Bishwamvarpur",
      "Chhatak",
      "Derai",
      "Dharampasha",
      "Dowarabazar",
      "Jagannathpur",
      "Jamalganj",
      "Lalpur",
      "Shantiganj",
      "Sunamganj Sadar",
      "Sullah",
      "Tahirpur"
    ],
    "Sylhet": [
      "Balaganj",
      "Beanibazar",
      "Bishwanath",
      "Companiganj",
      "Fenchuganj",
      "Golapganj",
      "Gowainghat",
      "Jaintiapur",
      "Kanaighat",
      "Sylhet Sadar",
      "Zakiganj",
      "South Surma",
      "Osmaninagar"
    ]
  },
  "Mymensingh": {
    "Jamalpur": [
      "Bakshiganj",
      "Dewanganj",
      "Islampur",
      "Jamalpur Sadar",
      "Madarganj",
      "Melandah",
      "Sarishabari"
    ],
    "Mymensingh": [
      "Bhaluka",
      "Dhobaura",
      "Fulbaria",
      "Gaffargaon",
      "Gauripur",
      "Haluaghat",
      "Iswarganj",
      "Muktagachha",
      "Mymensingh Sadar",
      "Nandail",
      "Phulpur",
      "Trishal",
      "Tarakanda"
    ],
    "Netrokona": [
      "Atpara",
      "Barhatta",
      "Durgapur",
      "Kalmakanda",
      "Kendua",
      "Khaliajuri",
      "Madan",
      "Mohanganj",
      "Netrokona Sadar",
      "Purbadhala"
    ],
    "Sherpur": [
      "Jhenaigati",
      "Nakla",
      "Nalitabari",
      "Sherpur Sadar",
      "Sreebardi"
    ]
  }
}
# --------------------------------------------------------------------------


def api_divisions(request):
    """Returns the list of all divisions."""
    # The JS expects {"divisions": [list of divisions]}
    return JsonResponse({"divisions": DIVISION_LIST})


def api_districts(request):
    """Returns districts filtered by the selected division."""
    division = request.GET.get('division')
    districts = []
    
    if division in GEOGRAPHY_DATA:
        districts = list(GEOGRAPHY_DATA[division].keys())
        
    # The JS expects {"districts": [list of districts]}
    return JsonResponse({"districts": districts})


def api_upazilas(request):
    """Returns upazilas filtered by the selected division and district."""
    division = request.GET.get('division')
    district = request.GET.get('district')
    upazilas = []
    
    if division in GEOGRAPHY_DATA and district in GEOGRAPHY_DATA[division]:
        upazilas = GEOGRAPHY_DATA[division][district]
        
    # The JS expects {"upazilas": [list of upazilas]}
    return JsonResponse({"upazilas": upazilas})