import json
from html.parser import HTMLParser
from xml.etree import ElementTree as ET

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

from .models import Photo, SiteSettings
from .seo import site_origin


class Head(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.meta, self.links, self.json_ld = [], [], []
        self.reading_json = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta":
            self.meta.append(attrs)
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self.reading_json = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.reading_json = False

    def handle_data(self, data):
        if self.reading_json:
            self.json_ld.append(json.loads(data))

    def canonical(self):
        return next(item["href"] for item in self.links if item.get("rel") == "canonical")

    def robots(self):
        return [item["content"] for item in self.meta if item.get("name") == "robots"]


@override_settings(SITE_URL="https://haus-flora.example", SEO_INDEXABLE=False)
class SearchLaunchTests(TestCase):
    fixtures = ["property_photos"]

    def test_preview_cannot_advertise_indexable_pages(self):
        for path in ("/de/", "/en/", "/de/umgebung/", "/en/galerie/area/"):
            head = Head(self.client.get(path).content.decode())
            self.assertEqual(head.robots(), ["noindex, follow"])
        sitemap = self.client.get("/sitemap.xml")
        self.assertEqual(len(ET.fromstring(sitemap.content)), 0)
        self.assertEqual(sitemap["X-Robots-Tag"], "noindex")
        robots = self.client.get("/robots.txt").content.decode()
        self.assertNotIn("Sitemap:", robots)
        self.assertNotIn("Disallow: /\n", robots)  # noindex must remain crawlable

    @override_settings(SEO_INDEXABLE=True)
    def test_public_sitemap_urls_match_indexable_canonical_language_pairs(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/xml"))
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [n.text for n in ET.fromstring(response.content).findall("s:url/s:loc", ns)]
        self.assertEqual(len(urls), 10)
        self.assertEqual(len(urls), len(set(urls)))
        descriptions = set()
        for url in urls:
            self.assertNotIn("?", url)
            path = url.removeprefix("https://haus-flora.example")
            page = self.client.get(path)
            self.assertEqual(page.status_code, 200)
            head = Head(page.content.decode())
            self.assertEqual(head.canonical(), url)
            self.assertEqual(head.robots(), ["index, follow, max-image-preview:large"])
            descriptions.add(next(x["content"] for x in head.meta if x.get("name") == "description"))
            alternates = {x["hreflang"]: x["href"] for x in head.links if x.get("rel") == "alternate"}
            self.assertEqual(set(alternates), {"de", "en", "x-default"})
            self.assertEqual(alternates["x-default"], alternates["de"])
            self.assertIn(url, alternates.values())
            other = "en" if path.startswith("/de/") else "de"
            partner = Head(self.client.get(alternates[other].removeprefix("https://haus-flora.example")).content.decode())
            self.assertEqual({x["hreflang"]: x["href"] for x in partner.links if x.get("rel") == "alternate"}, alternates)
        self.assertEqual(len(descriptions), 10)
        for path in ("/de/anfrage/danke/", "/en/impressum/", "/de/datenschutz/"):
            self.assertEqual(Head(self.client.get(path).content.decode()).robots(), ["noindex, follow"])
            self.assertNotIn("https://haus-flora.example" + path, urls)
        self.assertContains(self.client.get("/robots.txt"), "Sitemap: https://haus-flora.example/sitemap.xml")

    @override_settings(SEO_INDEXABLE=True)
    def test_filter_and_tracking_urls_do_not_create_search_duplicates(self):
        for path in ("/de/galerie/?category=outdoor", "/de/galerie/?utm_source=example"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 301)
            self.assertTrue(response["Location"].startswith("/de/#"))
        head = Head(self.client.get("/de/?utm_source=example").content.decode())
        self.assertEqual(head.canonical(), "https://haus-flora.example/de/")

    @override_settings(SEO_INDEXABLE=True)
    def test_structured_data_is_safe_and_contains_only_public_information(self):
        config = SiteSettings.load()
        config.property_address = '</script><script>alert("x")</script>'
        config.save()
        hidden_photo = Photo.objects.first()
        hidden_photo.is_active = False
        hidden_photo.save()
        html = self.client.get("/de/").content.decode()
        self.assertNotIn('</script><script>alert("x")</script>', html)
        graph = Head(html).json_ld[0]["@graph"]
        lodging = next(item for item in graph if item["@type"] == "LodgingBusiness")
        self.assertEqual(lodging["address"], config.property_address)
        self.assertNotIn("https://haus-flora.example" + hidden_photo.image.url, lodging["image"])
        self.assertEqual(lodging["containsPlace"]["occupancy"]["maxValue"], 4)
        self.assertNotIn("aggregateRating", lodging)
        self.assertNotIn("geo", lodging)
        self.assertNotIn("offers", lodging)
        self.assertNotIn("telephone", lodging)

    @override_settings(SEO_INDEXABLE=True, SITE_URL="")
    def test_indexing_requires_the_real_origin(self):
        with self.assertRaises(ImproperlyConfigured):
            site_origin()
