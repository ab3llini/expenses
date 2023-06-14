from enum import Enum


class ExpenseCategory(str, Enum):
    BAR_AND_RESTAURANTS = "Bar e ristoranti"
    HOME_AND_FAMILY = "Casa e famiglia"
    TRAVEL_AND_TRANSPORTATION = "Viaggi e trasporti"
    OTHER_EXPENSES = "Altre spese"
    LEISURE = "Tempo libero"
    HEALTH_AND_WELLNESS = "Salute e benessere"
    WORK = "Lavoro"
    MISC_INCOME = "Entrate varie"
    SHOPPING = "Shopping"
    TAXES_SERVICES_FEES = "Tasse, servizi e commissioni"
    REFUNDS = "Rimborsi"
    TRANSFERS = "Trasferimenti"


class ExpenseSubcategory(str, Enum):
    BAR = "Bar"
    GROCERIES = "Alimentari"
    TELEPASS_AND_TOLLS = "Telepass e Pedaggi"
    PIZZERIAS_AND_RESTAURANTS = "Pizzerie e Ristoranti"
    SUBSCRIPTIONS = "Abbonamenti"
    FUEL = "Carburante"
    CASH_WITHDRAWAL = "Prelievo contanti"
    RENT = "Affitto"
    HOTELS = "Hotel"
    PROFESSIONAL_SERVICES = "Attività professionali"
    SPORTING_EVENTS = "Eventi sportivi"
    WELLNESS_AND_RELAXATION = "Benessere e Relax"
    BILLS = "Bollette"
    GIFTS_AND_DONATIONS = "Regali e Donazioni"
    MISCELLANEOUS = "Varie"
    CINEMA = "Cinema"
    UNDEFINED = "-"
    MEDICAL_EXPENSES = "Spese mediche"
    INTERNET = "Internet"
    MUSIC_AND_MOVIES = "Musica e film"
    ACCESSORIES = "Accessori"
    TAXES_AND_FEES = "Tasse e Tributi"
    TOBACCO = "Tabacchi"
    BANK_FEES_AND_INTEREST = "Commissioni e interessi bancari"
    RENTAL = "Noleggio"
    TAKEOUT_FOOD = "Cibo da asporto"
    TAXI = "Taxi"
    MAINTENANCE = "Manutenzione"
    BOOKS = "Libri"
    SPORTING_GOODS = "Articoli sportivi"
    BULLETINS = "Bollettini"
    PHARMACY = "Farmacia"
    CLOTHING = "Abbigliamento"
    INSURANCE = "Assicurazioni"
    AIRPLANES = "Aerei"
    GYM = "Palestra"
    PARKING_AND_TICKETS = "Parcheggi e Biglietti"
    LEGAL_FEES = "Spese legali"
    SPORTS_AND_HOBBIES = "Sport e Hobbies"
    TRAINS = "Treni"
    FURNITURE = "Arredamento"
    VACATION = "Vacanze"
    ELECTRONICS = "Elettronica"
    VIDEOGAMES = "Videogames"
    MAINTENANCE_AND_RENOVATIONS = "Manutenzione e Ristrutturazioni"


class PaymentType(str, Enum):
    POS = "Pagamento POS"
    ONLINE = "Pagamenti Online"
    SELF_WITHDRAWAL = "Prelievo Sportello Self"
    BANK_TRANSFER = "Bonifico"
    PERMANENT_DEBIT = "Ordine permanente di addebito"
    INSTANT_TRANSFER = "Bonifico istantaneo"
    REVERSAL = "Storno"
    FEES = "Commissioni"
    WITHDRAWAL = "Prelievo"
    PAGOPA = "PagoPA"
    SUBSCRIPTION = "Canone"
    STAMP_DUTY = "Imposta di bollo"
    CBILL = "Cbill"


class Granularity(str, Enum):
    MONTH = "Month"
    WEEK = "Week"


class CategoryLevel(str, Enum):
    Large = "category"
    Small = "subcategory"


class CashFlow(str, Enum):
    Expense = "expense"
    Earning = "earning"
