"""Names to randomize into data to avoid overfit to specific patient names."""
import random
from itertools import cycle, product
from typing import Iterable


LAST_NAMES = [
    "Jansen",
    "Muñoz",
    "Rajapaksa",
    "Somchai",
    "Tiu",
    "MacDonald",
    "Mendoza",
    "Iyambo",
    "Sankara",
    "Mwangi",
    "Greco",
    "Soto",
    "Oliveira",
    "Doyle",
    "Bui",
    "Okafor",
    "Visser",
    "Kobayashi",
    "Rodrigues",
    "Ndiaye",
    "Martins",
    "Yang",
    "Faye",
    "Jiménez",
    "Okongo",
    "Sánchez",
    "O'Neill",
    "Oyono",
    "Biko",
    "Bemba",
    "Qureshi",
    "Mogale",
    "Dang",
    "Colombo",
    "Thaksin",
    "Ngugi",
    "Schmidt",
    "Adichie",
    "Kato",
    "Cho",
    "Gallagher",
    "Edwards",
    "Pizarro",
    "Sousa",
    "Selassie",
    "Guerrero",
    "Boon",
    "Zárate",
    "Hussain",
    "Weber",
    "Domínguez",
    "Balboa",
    "MacKenzie",
    "Ubane",
    "Larsen",
    "Kenyatta",
    "Delgado",
    "Meyer",
    "Pérez",
    "Cordero",
    "Yamamoto",
    "Li",
    "Amadou",
    "Schäfer",
    "Bautista",
    "Olsen",
    "Yekini",
    "Fernando",
    "McCarthy",
    "Huang",
    "Fernández",
    "Sultana",
    "Reyes",
    "Ndlovu",
    "Hernández",
    "Karlsson",
    "Russo",
    "Kidane",
    "Gunawardena",
    "Chirwa",
    "Romano",
    "Gomes",
    "Patel",
    "Nunes",
    "Bouteflika",
    "Gallegos",
    "Fitzgerald",
    "Valencia",
    "De Vries",
    "Watanabe",
    "Mendes",
    "Zhou",
    "Hughes",
    "Le",
    "Gupta",
    "Fischer",
    "Lumumba",
    "Nguyen",
    "Smith",
    "Salah",
    "Ahmed",
    "Tanaka",
    "Van Dijk",
    "Jung",
    "Abate",
    "Quintero",
    "O'Connell",
    "De la Paz",
    "Sevilla",
    "Martínez",
    "Osei",
    "Silva",
    "Uwimana",
    "Pereira",
    "Cortés",
    "Traoré",
    "Djibo",
    "Wagner",
    "Palacios",
    "Ito",
    "Zhang",
    "Ibarra",
    "Rossi",
    "Miah",
    "Chowdhury",
    "Islam",
    "Sawadogo",
    "Kim",
    "Hansen",
    "Moyo",
    "Burgos",
    "Mohammed",
    "Raja",
    "Petit",
    "Mba",
    "Davies",
    "El-Ghazali",
    "Barros",
    "Becker",
    "Wong",
    "Esposito",
    "Sharma",
    "Fuentes",
    "Wilson",
    "Vargas",
    "Choi",
    "Johansson",
    "Vimbai",
    "Haile",
    "Salazar",
    "Go",
    "Eriksson",
    "Aguilar",
    "van der Merwe",
    "Tshisekedi",
    "Taylor",
    "Iglesias",
    "Sang",
    "Anderson",
    "Ricci",
    "San Miguel",
    "El Amrani",
    "Brown",
    "Sato",
    "Romero",
    "Johnson",
    "Davis",
    "Kumar",
    "Barua",
    "Evans",
    "Costa",
    "Biya",
    "Schneider",
    "Khaled",
    "Sheik",
    "Nkunda",
    "González",
    "Takahashi",
    "Joshi",
    "Nakamura",
    "Espinosa",
    "Castro",
    "Nilsen",
    "Monteiro",
    "Pham",
    "De Jesús",
    "Abega",
    "Abubakar",
    "Kang",
    "Masuku",
    "Chikane",
    "Ferrari",
    "Robles",
    "Dube",
    "Morales",
    "Oviedo",
    "Haque",
    "Coulibaly",
    "Ferreira",
    "Mansour",
    "Lamine",
    "Wu",
    "Bernard",
    "Kaboré",
    "Hoffmann",
    "Omari",
    "Mahmood",
    "Konaté",
    "Lee",
    "M'Bow",
    "Andersson",
    "Ponce",
    "Anan",
    "Khan",
    "Álvarez",
    "Müller",
    "Ali",
    "Laroui",
    "Ortega",
    "Khumalo",
    "Gueye",
    "Wambugu",
    "Jesus",
    "Diop",
    "Cepeda",
    "Adebayo",
    "Ekpo",
    "Sow",
    "Arboleda",
    "Jayasinghe",
    "Shah",
    "García",
    "Makonnen",
    "De Jong",
    "Maalouf",
    "Mandela",
    "Lima",
    "León",
    "Adeola",
    "Xaba",
    "Hoang",
    "Chávez",
    "Andrade",
    "Martín",
    "Wanjiku",
    "Navarro",
    "Gómez",
    "Nkosi",
    "Chen",
    "Ngouabi",
    "Ocampo",
    "López",
    "Morris",
    "El-Sayed",
    "Leroy",
    "Aragón",
    "Quezada",
    "Janssen",
    "Ribeiro",
    "Ruiz",
    "Vieira",
    "Tshabalala",
    "Achebe",
    "Williams",
    "Miller",
    "Liu",
    "Phan",
    "Huynh",
    "El Fassi",
    "Iqbal",
    "Wickramasinghe",
    "Cardoso",
    "O'Brien",
    "Moreno",
    "Nyerere",
    "N'Dour",
    "Suzuki",
    "Roberts",
    "Quenum",
    "Toledo",
    "Sithole",
    "Tesfaye",
    "Smit",
    "Wang",
    "Thomas",
    "Morgan",
    "Díaz",
    "Dubois",
    "Mensah",
    "O'Reilly",
    "Nkrumah",
    "Carvalho",
    "Alonso",
    "Murillo",
    "Del Rosario",
    "Jones",
    "Meijer",
    "Peralta",
    "Radebe",
    "Bah",
    "Tran",
    "Ture",
    "Torres",
    "Fofana",
    "Van den Berg",
    "Medina",
    "Singh",
    "Marino",
    "Santos",
    "Almeida",
    "Durand",
    "Lim",
    "Wamah",
    "Yoon",
    "Marques",
    "Haddad",
    "Cáceres",
    "Enyia",
    "Rehman",
    "De Silva",
    "Bandara",
    "Jalloh",
    "Keita",
    "Mosquera",
    "Yattara",
    "Garrido",
    "Nilsson",
    "Srisai",
    "Begum",
    "Zhao",
    "Das",
    "Angel",
    "Sen",
    "Kabila",
    "Perera",
    "Bianchi",
    "Vo",
    "Martin",
    "Toure",
    "Souza",
    "Robert",
    "Rodríguez",
    "Zamora",
    "Diarra",
    "Chai",
    "Lopes",
    "Garcia",
    "Rahman",
    "Escobar",
    "Senanayake",
    "Bakker",
    "Nguema",
    "De la Cruz",
    "Kaur",
    "Eboué",
    "Gutiérrez",
    "Park",
    "Vu",
    "Serrano",
    "Poku",
    "Richard",
    "Griffiths",
    "Jang",
    "Zerbo",
    "Prasert",
    "Pedersen",
    "Kham",
    "Pacheco",
    "Cruz",
    "Vega",
    "Moreau",
    "Ben Ali",
    "Malik",
]


FIRST_NAMES = [
    "Sasha",
    "Tony",
    "Lan",
    "Jian",
    "Chen",
    "Shun",
    "Oni",
    "Payam",
    "Rui",
    "Marian",
    "Nomusa",
    "Tai",
    "Noa",
    "Skye",
    "Parker",
    "Gacoki",
    "Akira",
    "Reese",
    "Sade",
    "Esi",
    "Tien",
    "Ibai",
    "Elia",
    "Ode",
    "Kendall",
    "Rio",
    "Casey",
    "Rahim",
    "Ping",
    "Thanh",
    "Shahin",
    "Ning",
    "Quinn",
    "Mar",
    "Nhat",
    "Emilia",
    "Lei",
    "Ade",
    "River",
    "Milan",
    "Zarin",
    "Onyeka",
    "Taylor",
    "Naledi",
    "Teo",
    "Jie",
    "Qi",
    "Finley",
    "Hikaru",
    "Nuria",
    "Zhen",
    "Dale",
    "Jaime",
    "Kato",
    "Sefu",
    "Parviz",
    "Kwame",
    "Kali",
    "Yan",
    "Jahi",
    "Kanene",
    "Moji",
    "Sen",
    "Ime",
    "Di",
    "Phoenix",
    "Yi",
    "Drew",
    "Tao",
    "Ki",
    "Dara",
    "Shayan",
    "Sage",
    "Gabi",
    "Sang",
    "Maysan",
    "Yong",
    "Peyton",
    "Kesi",
    "Kojo",
    "Ryun",
    "Jia",
    "Emeka",
    "Bobby",
    "Keji",
    "Micah",
    "Adrian",
    "Beau",
    "Eshe",
    "Yin",
    "Darian",
    "Guadalupe",
    "Jamie",
    "Rai",
    "Park",
    "Rei",
    "Rami",
    "Simin",
    "Sanaz",
    "Bao",
    "Jesse",
    "Binta",
    "Camila",
    "Huong",
    "Quan",
    "Kelly",
    "Rhys",
    "Obi",
    "Nader",
    "Shani",
    "Senwe",
    "Themba",
    "Wei",
    "Eden",
    "Vidal",
    "Reagan",
    "Khari",
    "Lu",
    "Li",
    "Yeong",
    "Si",
    "Morgan",
    "Maite",
    "Nabil",
    "Alejandro",
    "Hyun",
    "Amani",
    "Zhi",
    "Munashe",
    "Nuru",
    "Jamal",
    "Nam",
    "Jahan",
    "Eir",
    "Chike",
    "Lethabo",
    "Rethabile",
    "Nneka",
    "Trung",
    "Avery",
    "Zi",
    "Myeong",
    "Kei",
    "Gathii",
    "Dao",
    "Azar",
    "Luz",
    "Dada",
    "Ngoc",
    "Hai",
    "Raza",
    "Yen",
    "Dalmar",
    "Nur",
    "Ata",
    "Rory",
    "Cruz",
    "Dike",
    "Lekan",
    "Sun",
    "Andrea",
    "Phong",
    "Diyar",
    "Palesa",
    "Pat",
    "Naim",
    "Ling",
    "Jin",
    "Nari",
    "Sora",
    "Afolabi",
    "Bahar",
    "Abi",
    "Kamari",
    "Samir",
    "Vega",
    "Tafadzwa",
    "Eli",
    "Haneul",
    "Hieu",
    "Delfín",
    "Kai",
    "Isi",
    "Tian",
    "Ladan",
    "Nahal",
    "Sydney",
    "Chacha",
    "Jelani",
    "Idi",
    "Talal",
    "Emery",
    "Pilar",
    "Kang",
    "Guan",
    "Tamir",
    "Yao",
    "Paz",
    "Ryu",
    "Huan",
    "Jun",
    "Fu",
    "Daryl",
    "Jabari",
    "Lin",
    "Nia",
    "Kiano",
    "Carmen",
    "Lee",
    "Dayo",
    "Mika",
    "Zo",
    "Zixi",
    "Jing",
    "Asa",
    "Minh",
    "Uriel",
    "Tuan",
    "Xuan",
    "Mudiwa",
    "Mandla",
    "Shirin",
    "Dakota",
    "Iniko",
    "Skyler",
    "Bongani",
    "Rayan",
    "Sibongile",
    "Hayden",
    "Folami",
    "Lien",
    "Ariel",
    "Freyja",
    "Dakarai",
    "Fen",
    "Hin",
    "An",
    "Sami",
    "Udo",
    "Efia",
    "Chidi",
    "Karam",
    "Olufemi",
    "Tandi",
    "Ige",
    "Jalal",
    "Kamal",
    "Corey",
    "Zola",
    "Frankie",
    "Nkosana",
    "Rana",
    "Dana",
    "Juliana",
    "Kim",
    "Aoi",
    "Yun",
    "Ola",
    "Yu",
    "Reza",
    "Hadi",
    "Sol",
    "Luca",
    "Noel",
    "Reyes",
    "Danladi",
    "Simba",
    "Kainda",
    "Milán",
    "Saad",
    "Nyah",
    "Fabiana",
    "Bailey",
    "Dani",
    "Saman",
    "Kellan",
    "Noelle",
    "Luka",
    "Genesis",
    "Shan",
    "Gael",
    "Sam",
    "Robin",
    "Imani",
    "Blair",
    "Suki",
    "Cai",
    "Miren",
    "Iman",
    "Opeyemi",
    "Kioni",
    "Makena",
    "Dumisani",
    "Haru",
    "Ife",
    "Femi",
    "Halima",
    "Montserrat",
    "Charlie",
    "Ming",
    "Nahid",
    "Tendai",
    "Ellis",
    "Faris",
    "Amadi",
    "Kito",
    "Jordan",
    "Kwasi",
    "Alex",
    "Fran",
    "Hadiya",
    "Lynn",
    "Laleh",
    "Tahir",
    "Soraya",
    "Yuan",
    "Yuri",
    "Wen",
    "Roshan",
    "Hoa",
    "Sidney",
    "Oakley",
    "Alexi",
    "Shannon",
    "Chris",
    "Rowan",
    "Jules",
    "Max",
    "Harley",
    "Uzoma",
    "Taiwo",
    "Thulani",
    "Ekundayo",
    "Lempi",
    "Riley",
    "Anan",
    "Okello",
    "Nkiru",
    "Ren",
    "Asha",
    "Shadi",
    "Yue",
    "Eui",
    "Angel",
    "Nini",
    "London",
    "Chi",
    "Cameron",
    "Kimoni",
    "Hani",
    "Amal",
    "Soo",
    "Masego",
    "Habib",
    "Bjørn",
    "Nan",
    "Leslie",
]


FIRST_AND_LAST_NAME_PAIRS = list(product(FIRST_NAMES, LAST_NAMES))


def get_names() -> Iterable[tuple[str, str]]:
    shuffled = list(FIRST_AND_LAST_NAME_PAIRS)
    random.shuffle(shuffled)
    return cycle(shuffled)
