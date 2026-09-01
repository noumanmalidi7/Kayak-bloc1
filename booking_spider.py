import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime, timedelta

# ---- Variables globales pour les dates (correction) ----
CHECKIN = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
CHECKOUT = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")

CITIES = [
    "Mont Saint Michel", "St Malo", "Bayeux", "Le Havre", "Rouen",
    "Paris", "Amiens", "Lille", "Strasbourg", "Chateau du Haut Koenigsbourg",
    "Colmar", "Eguisheim", "Besancon", "Dijon", "Annecy",
    "Grenoble", "Lyon", "Gorges du Verdon", "Bormes les Mimosas", "Cassis",
    "Marseille", "Aix en Provence", "Avignon", "Uzes", "Nimes",
    "Aigues Mortes", "Saintes Maries de la mer", "Collioure", "Carcassonne",
    "Ariege", "Toulouse", "Montauban", "Biarritz", "Bayonne", "La Rochelle"
]

class BookingSpider(scrapy.Spider):
    name = "booking"
    allowed_domains = ["booking.com"]

    start_urls = [
        f"https://www.booking.com/searchresults.html?ss={city}&checkin={CHECKIN}&checkout={CHECKOUT}"
        for city in CITIES
    ]

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS": 1,
        "COOKIES_ENABLED": True,
        "FEEDS": {"hotels.json": {"format": "json", "encoding": "utf8"}}
    }

    def parse(self, response):
        hotels = response.css('div[data-testid="property-card"]')
        if not hotels:
            hotels = response.css('div[data-testid="property-card-container"]')
        if not hotels:
            self.logger.warning(f"Aucun hôtel trouvé pour {response.url}")
            return

        for hotel in hotels:
            city = response.url.split("ss=")[-1].split("&")[0]

            name = hotel.css('div[data-testid="title"]::text').get()
            if not name:
                name = hotel.css('div.fcab3ed991.a23c043802::text').get()
            if name:
                name = name.strip()

            rating = hotel.css('[data-testid="review-score"]::text').get()
            if not rating:
                rating = hotel.css('div.f13857cc8c.e008572b71::text').get()
            if not rating:
                rating = "0.0"

            url = hotel.css('a[data-testid="title-link"]::attr(href)').get()
            if url and name:
                yield response.follow(url, self.parse_hotel_detail, meta={"name": name, "rating": rating, "city": city})

        next_page = response.css('a[data-testid="pagination-next"]::attr(href)').get()
        if not next_page:
            next_page = response.css("a.bui-pagination__link.pagenext::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_hotel_detail(self, response):
        name = response.meta.get("name", "Unknown")
        city = response.meta.get("city", "Unknown")
        rating = response.meta.get("rating", "0.0")
        url = response.url

        address = response.css('[data-testid="address"]::text').get()
        if not address:
            address = response.css('span.hp_address_subtitle::text').get()
        if address:
            address = address.strip()

        description = response.css('p[data-testid="property-description"]::text').get()
        if not description:
            description = response.css('div[data-testid="property-description"]::text').get()
        if description:
            description = description.strip()

        coordinates = response.css('a#hotel_address::attr(data-atlas-latlng)').get()
        if not coordinates:
            coordinates = response.css('button#hotel_address::attr(data-atlas-latlng)').get()
        latitude, longitude = None, None
        if coordinates:
            try:
                lat, lon = coordinates.split(",")
                latitude = float(lat.strip())
                longitude = float(lon.strip())
            except (ValueError, AttributeError):
                pass

        yield {
            "city": city.lower().replace("%20", "").replace("+", ""),
            "name": name,
            "url": url,
            "rating": float(rating) if rating else 0.0,
            "address": address,
            "description": description,
            "latitude": latitude,
            "longitude": longitude
        }

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(BookingSpider)
    process.start()
